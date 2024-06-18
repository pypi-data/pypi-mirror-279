#!/usr/bin/python3
import sqlite3
import pikobs
import re
import os
from  dask.distributed import Client
import numpy as np
import sqlite3
import os
import re
import sqlite3
from  datetime import datetime, timedelta


def create_serie_cardio(family, 
                        new_db_filename, 
                        existing_db_filename,
                        region_seleccionada,
                        selected_flags, 
                        id_stn,
                        channel, 
                        varno):
    """
    Create a new SQLite database with a 'moyenne' table and populate it with data from an existing database.

    Args:
    new_db_filename (str): Filename of the new database to be created.
    existing_db_filename (str): Filename of the existing database to be attached.
    region_seleccionada (str): Region selection criteria.
    selected_flags (str): Selected flags criteria.
    FONCTION (float): Value for sum_fonction column.

    Returns:
    None
    """

 
    pattern = r'(\d{10})'
    match = re.search(pattern, existing_db_filename)

    if match:
        date = match.group(1)
       
    else:
        print("No 10 digits found in the string.")
    
    # Connect to the new database
    if id_stn[0]=='all':
      criteria_id_stn = '    '
    else:
       # Paso 1: Añadir comillas simples alrededor de cada elemento
       elementos_con_comillas = [f"'{elemento}'" for elemento in id_stn]

       # Paso 2: Unir los elementos con comas
       resultado = f"({','.join(elementos_con_comillas)})"
       criteria_id_stn = f'and id_stn in {resultado}'
    if channel[0]=='all':
      criteria_vcoord = '    '
    else:
       resultado = f"({','.join(channel)})"
       criteria_vcoord = f'and vcoord in {resultado}    '

      
    new_db_conn = sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=999)
    new_db_cursor = new_db_conn.cursor()

    FAM, VCOORD, VCOCRIT, STATB, VCOORD, VCOTYP = pikobs.family(family)
    LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
    LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
    flag_criteria = pikobs.flag_criteria(selected_flags)

    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
    # load extension CMC 
    new_db_conn.enable_load_extension(True)
    extension_dir = f'{os.path.dirname(pikobs.__file__)}/extension/libudfsqlite-shared.so'
    new_db_conn.execute(f"SELECT load_extension('{extension_dir}')")
    # Create the 'moyenne' table in the new database if it doesn't exist
    new_db_cursor.execute("""
           CREATE TABLE IF NOT EXISTS serie_cardio ( 
            DATE INTEGER,
            Chan INTEGER,
            Nrej INTEGER,
            Nacc INTIGER,
            AvgOMP FLOAT, 
            AvgOMA FLOAT,
            StdOMP FLOAT,
            StdOMA FLOAT,
            NDATA  INTEGER,
            Nprofile INTEGER,
            AvgBCOR FLOAT,
            AvgOBS FLOAT,
            Ntot INTEGER,
            varno INTEGER,
            id_stn  TEXT
        );
    """)
    query=f"""INSERT INTO serie_cardio (

            DATE,
            Chan,
            Nrej,
            Nacc,
            AvgOMP, 
            AvgOMA,
            StdOMP,
            StdOMA,
            NDATA,
            Nprofile,
            AvgBCOR,
            AvgOBS,
            Ntot,
            varno,
            id_stn
        )
    
    
             SELECT 
                 isodatetime({date}) AS DATE,  
                 VCOORD As Chan, 
                 SUM(flag & 512=512) AS Nrej,
                 SUM(flag & 4096=4096) AS Nacc,
                 ROUND(AVG(OMP), 4) AS AvgOMP,
                 ROUND(AVG(OMA), 4) AS AvgOMA,
                 ROUND(STDDEV(OMP), 4) AS StdOMP,
                 ROUND(STDDEV(OMA), 4) AS StdOMA,
                 SUM(OMP IS NOT NULL) AS NDATA,
                 COUNT(DISTINCT id_obs) AS Nprofils,
                 ROUND(AVG(BIAS_CORR), 4) AS AvgBCOR,
                 ROUND(AVG(OBSVALUE), 4) AS AvgOBS,
                 (SELECT COUNT(*) FROM header h2 WHERE h2.ID_STN = header.ID_STN) AS Ntot,
                 varno AS varno,
                 id_stn AS id_stn
                 
            FROM 
                 header
             NATURAL JOIN 
                 data
             WHERE 
                 VARNO = {int(varno)}
                 {criteria_id_stn}
                 {criteria_vcoord}
                 {flag_criteria}
                 {LATLONCRIT}
                 {VCOCRIT}
             GROUP BY 
                 VCOORD, ID_STN
             HAVING 
                 SUM(OMP IS NOT NULL) >= 50;"""

    new_db_cursor.execute(query)
    # Commit changes and detach the existing database
    new_db_conn.commit()

    # Commit changes and detach the existing database
    new_db_cursor.execute("DETACH DATABASE db;")

    # Close the connections
    new_db_conn.close()

def create_data_list_cardio(datestart1, 
                            dateend1,
                            family,
                            pathin, 
                            pathwork,
                            flag_criteria,
                            id_stn,
                            channel,
                            region_seleccionada):
    
    data_list_cardio = []

    # Convert datestart and dateend to datetime objects
    datestart = datetime.strptime(datestart1, '%Y%m%d%H')
    dateend = datetime.strptime(dateend1, '%Y%m%d%H')

    # Initialize the current_date to datestart
    current_date = datestart

    # Define a timedelta of 6 hours
    delta = timedelta(hours=6)
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)

    element_array = np.array([float(x) for x in element.split(',')])
    for varno in element_array:
   #  print ("VCOORD", vcoord, element, type(element))
     # Iterate through the date range in 6-hour intervals
     while current_date <= dateend:
        # Format the current date as a string
        formatted_date = current_date.strftime('%Y%m%d%H')

        # Build the file name using the date and family
        filename = f'{formatted_date}_{family}'

        file_path_name = f'{pathin}/{filename}'
        conn = sqlite3.connect(file_path_name)
        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        #  Create a new dictionary and append it to the list
        data_dict = {'family': family,
                          'filein': f'{pathin}/{filename}',
                          'db_new': f'{pathwork}/cardio_{datestart1}_{dateend1}_{flag_criteria}_{family}.db',
                          'region': region_seleccionada,
                          'flag_criteria': flag_criteria,
                          'varno':  varno,
                          'vcoord': channel,
                          'id_stn': id_stn}
        data_list_cardio.append(data_dict)
        conn.close()

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list_cardio


def get_station_ids(cursor, id_stn):
    """Fetch all distinct station IDs if 'id_stn' is 'all', otherwise return the provided IDs."""
    if id_stn[0] == 'all':
        cursor.execute("SELECT DISTINCT id_stn FROM serie_cardio;")
        return [item[0] for item in cursor.fetchall()]
    return np.array(id_stn)

def fetch_channels_and_varno(cursor, idstn, channel):
    """Fetch channels and varno for a given station and channel criteria."""
    criter = f'WHERE id_stn = "{idstn}"'
    if channel[0] == 'all':
        query = f"SELECT DISTINCT chan, varno FROM serie_cardio {criter} ORDER BY chan ASC;"
        cursor.execute(query)
        return cursor.fetchall()
    else:
        channels_varno = []
        for chan in np.array(channel):
            query = f"SELECT DISTINCT chan, varno FROM serie_cardio {criter} AND chan={chan} ORDER BY chan ASC;"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                channels_varno.append(result)
        return channels_varno

def create_data_list_plot(datestart1, dateend1, family, pathin, pathwork, flag_criteria, region_seleccionada, id_stn, channel):
    """Create a list of data dictionaries for plotting based on the given criteria."""
    data_list_plot = []
    filedb = f'{pathwork}/cardio_{datestart1}_{dateend1}_{flag_criteria}_{family}.db'

    try:
        with sqlite3.connect(filedb) as conn:
            cursor = conn.cursor()
            id_stns = get_station_ids(cursor, id_stn)

            for idstn in id_stns:
                channels_varno = fetch_channels_and_varno(cursor, idstn, channel)
                for chan, varno in channels_varno:
                    data_dict_plot = {
                        'id_stn': idstn,
                        'vcoord': chan,
                        'varno': varno
                    }
                    data_list_plot.append(data_dict_plot)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return data_list_plot

def make_cardio(path_experience_files,
                experience_names,      
                pathwork, 
                datestart,
                dateend,
                regions, 
                familys, 
                flag_criteria, 
                id_stn,
                channel,
                plot_type,
                plot_title,
                n_cpu):
   pikobs.delete_create_folder(pathwork)

   for family in familys:
     for region in regions:
       print ("##> Family:", family, "Region:", region)
       data_list_cardio = create_data_list_cardio(datestart,
                                           dateend, 
                                           family, 
                                           path_experience_files, 
                                           pathwork,
                                           flag_criteria, 
                                           id_stn,
                                           channel,
                                           region)
       
       import time
       import dask
       t0 = time.time()
       if n_cpu==1:
        print (f"Serie = {len(data_list_cardio)} files")
        for  data_ in data_list_cardio:  
            create_serie_cardio(data_['family'], 
                                data_['db_new'], 
                                data_['filein'],
                                data_['region'],
                                data_['flag_criteria'],
                                data_['id_stn'],
                                data_['vcoord'],
                                data_['varno'])




       else:
        print (f'Number of files used in calculating statistics = {len(data_list_cardio)}')
        with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(create_serie_cardio)(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['id_stn'],
                                              data_['vcoord'],
                                              data_['varno'])for data_ in data_list_cardio]
            results = dask.compute(*delayed_funcs)
        
       tn= time.time()
       print ('Total time for statistics:',tn-t0 )  
       data_list_plot = create_data_list_plot(datestart,
                                    dateend, 
                                    family, 
                                    path_experience_files, 
                                    pathwork,
                                    flag_criteria, 
                                    region,
                                    id_stn,
                                    channel)



       os.makedirs(f'{pathwork}/plots_{family}')
       t0 = time.time()
       if len(data_list_plot)==0:
          raise ValueError('You must specify best selectoion od id_stn and channel plot==0')

       if n_cpu==1: 
          print (f'serie= {len(data_list_plot)} files')
          for  data_ in data_list_plot:  
              pikobs.cardio_plot(pathwork,
                                 datestart,
                                 dateend,
                                 flag_criteria,
                                 family,
                                 plot_title,
                                 plot_type, 
                                 data_['vcoord'],
                                 data_['id_stn'], 
                                 data_['varno'],
                                 region)
       else:
          print (f'number of plot in paralle = {len(data_list_plot)}')
          with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(pikobs.cardio_plot)(
                               pathwork,
                                 datestart,
                                 dateend,
                                 flag_criteria,
                                 family,
                                 plot_title,
                                 plot_type, 
                                 data_['vcoord'],
                                 data_['id_stn'], 
                                 data_['varno'],
                                 region)for data_ in data_list_plot]

            results = dask.compute(*delayed_funcs)
       tn= time.time()
       print ('total time for plotting:',tn-t0 )  

 



def arg_call():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_experience_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--experience_name', default='undefined', type=str, help="experience's name")
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', nargs="+", default='undefined', type=str, help="Region")
    parser.add_argument('--family', nargs="+", default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--id_stn',nargs="+", default='all', type=str, help="id_stn") 
    parser.add_argument('--channel',nargs="+",  default='all', type=str, help="channel") 
    parser.add_argument('--plot_type', default='wide', type=str, help="channel")
    parser.add_argument('--plot_title', default='plot', type=str, help="channel")
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of cpus")

    args = parser.parse_args()
    print ( "Inputs in cardiogram calculation")
    print ("----------------------------------------")

    for arg in vars(args):
      
       print (f'--{arg} {getattr(args, arg)}')
    print ("----------------------------------------")
    # check if each argument is 'undefined'
    if args.path_experience_files == 'undefined':
        raise ValueError('You must specify --path_experience_files')
    if args.experience_name == 'undefined':      
        raise ValueError('You must specify -experience_name')
    if args.pathwork  == 'undefined':
        raise ValueError('You must specify --pathwork')
    if args.datestart == 'undefined':
        raise ValueError('You must specify --datestart')
    if args.dateend == 'undefined':
        raise ValueError('You must specify --dateend')
    if args.region == 'undefined':
        raise ValueError('You must specify --region')
    if args.family == 'undefined':
        raise ValueError('You must specify --family')
    if args.flags_criteria == 'undefined':
        raise ValueError('You must specify --flags_criteria')
   # if args.fonction == 'undefined':
   #     raise ValueError('You must specify --fonction')

    #Call your function with the arguments
    sys.exit(make_cardio (args.path_experience_files,
                          args.experience_name,
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.id_stn,
                          args.channel,
                          args.plot_type,
                          args.plot_title,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()
