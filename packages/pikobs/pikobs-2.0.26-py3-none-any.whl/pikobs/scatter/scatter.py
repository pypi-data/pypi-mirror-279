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


def create_and_populate_moyenne_table(family, new_db_filename, existing_db_filename, region_seleccionada, selected_flags, FONCTION, boxsizex, boxsizey):
    """
    Create a new SQLite database with a 'moyenne' table and populate it with data from an existing database.

    Args:
    new_db_filename (str): Filename of the new database to be created.
    existing_db_filename (str): Filename of the existing database to be attached.
    region_seleccionada (str): Region selection criteria.
    selected_flags (str): Selected flags criteria.
    FONCTION (float): Value for sum_fonction column.
    boxsizex (float): Value for boxsizex column.
    boxsizey (float): Value for boxsizey column.

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
  
    new_db_conn = sqlite3.connect(new_db_filename, uri=True, isolation_level=None, timeout=999)
    new_db_cursor = new_db_conn.cursor()
    FAM, VCOORD, VCOCRIT, STATB, element, VCOTYP = pikobs.family(family)
    LAT1, LAT2, LON1, LON2 = pikobs.regions(region_seleccionada)
    LATLONCRIT = pikobs.generate_latlon_criteria(LAT1, LAT2, LON1, LON2)
    flag_criteria = pikobs.flag_criteria(selected_flags)
    STNID = f"floor(360. / {boxsizex} ) * floor(lat / {boxsizey} ) + floor(MIN(179.99, lon) / {boxsizex}) "
    LAT = f"floor(lat / {boxsizey})  * {boxsizey} + {boxsizey} / 2."
    LON = f"floor(MIN(179.99, lon) / {boxsizex} ) * {boxsizex} + {boxsizex} / 2. "
    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")

    # Create the 'moyenne' table in the new database if it doesn't exist
    new_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS moyenne (
            Nrej INTEGER,
            Nacc INTEGER,
            Nprofile INTEGER,
            DATE INTEGER,
            lat FLOAT,
            lon FLOAT,
            boite INTEGER,
            id_stn TEXT,
            varno INTEGER,
            vcoord FLOAT,   -- INTEGER FLOAT canal
            sumx FLOAT,
            sumy FLOAT,
            sumz FLOAT,
            sumStat FLOAT,
            sumx2 FLOAT,
            sumy2 FLOAT,
            sumz2 FLOAT,
            sumStat2 FLOAT,
            n INTEGER,
            flag integer
        );
    """)

    # Execute the data insertion from the existing database
    sss = f"""
    INSERT INTO moyenne (
        DATE,
        lat,
        lon,
        boite, 
        varno, 
        vcoord, 
        sumx, 
        sumy, 
        sumz,
        sumStat,
        sumx2, 
        sumy2, 
        sumz2, 
        sumStat2,
        n,
        Nrej,
        Nacc,
        Nprofile,
        id_stn,
        flag

    )
    SELECT
        {date},
        {LAT},
        {LON},
        {STNID},
        VARNO,
        {VCOORD},
        sum(omp),
        sum(oma),
        sum(obsvalue), 
        sum(bias_corr),
        sum(omp*omp),
        sum(oma*oma),
        sum(obsvalue*obsvalue),
        sum(bias_corr*bias_corr),
        COUNT(*),
        sum(flag & 512=512),
        sum(flag & 4096-4094),
        count(distinct id_obs),
        id_stn,
        flag
        

    FROM
        db.header
    NATURAL JOIN
        db.DATA
    WHERE
        varno IN ({element})
        AND obsvalue IS NOT NULL
        {flag_criteria}
        {LATLONCRIT}
        {VCOCRIT}
    GROUP BY
        2, 3, 4, 5, 6, id_stn;
    """
    new_db_cursor.execute(sss)

    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")
    new_db_conn.commit()




    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()
from datetime import datetime, timedelta

def create_data_list(datestart1, dateend1, family, pathin, name, pathwork, boxsizex, boxsizey, fonction, flag_criteria, region_seleccionada):
    data_list = []
    #print (datestart1, dateend1, family, pathin, pathwork, boxsizex, boxsizey, fonction, flag_criteria, region_seleccionada)
    # Convert datestart and dateend to datetime objects
    datestart = datetime.strptime(datestart1, '%Y%m%d%H')
    dateend = datetime.strptime(dateend1, '%Y%m%d%H')

    # Initialize the current_date to datestart
    current_date = datestart

    # Define a timedelta of 6 hours
    delta = timedelta(hours=6)

    # Iterate through the date range in 6-hour intervals
    while current_date <= dateend:
        # Format the current date as a string
        formatted_date = current_date.strftime('%Y%m%d%H')

        # Build the file name using the date and family
        filename = f'{formatted_date}_{family}'
        # Create a new dictionary and append it to the list
        data_dict = {
            'family': family,
            'filein': f'{pathin}/{filename}',
            'db_new': f'{pathwork}/scatter_{name}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db',
            'region': region_seleccionada,
            'flag_criteria': flag_criteria,
            'fonction': fonction,
            'boxsizex': boxsizex,
            'boxsizey': boxsizey
        }
        data_list.append(data_dict)

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list

def create_data_list_plot(datestart1,
                          dateend1, 
                          family, 
                          namein, 
                          pathwork, 
                          boxsizex, 
                          boxsizey, 
                          fonction, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          channel):
    data_list_plot = []

    filea = f'{pathwork}/scatter_{namein[0]}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db'
    namea = namein[0]
    fileset = [filea]
    nameset = [namein[0]]
    print (f'file Experience {namein[0]}: ',filea)

    if len(namein)>1:
       fileb = f'{pathwork}/scatter_{namein[1]}_{datestart1}_{dateend1}_bx{boxsizex}_by{boxsizey}_{flag_criteria}_{family}.db'
       fileset = [filea,fileb]
       nameset = [namein[0], namein[1]] 
       print (f'file Experience {namein[1]}: ',fileb)

    conn = sqlite3.connect(filea)
    cursor = conn.cursor()
    if id_stn=='one_per_plot':
        query = "SELECT DISTINCT id_stn FROM moyenne;"
        cursor.execute(query)
        id_stns = cursor.fetchall()
    else:
        id_stns = 'all'

    for idstn in id_stns:
       
       if id_stn=='one_per_plot':
          criter =f'where id_stn = "{idstn[0]}"'
       
       elif id_stn=='all':

         criter =' '

       query = f"SELECT DISTINCT vcoord, varno FROM moyenne {criter} ORDER BY vcoord ASC;"
       cursor.execute(query)
       vcoords = cursor.fetchall()
       for vcoord, varno in vcoords:
           #print (idstn[0],vcoord[0])
           data_dict_plot = {
            'id_stn': idstn[0],
            'vcoord': vcoord,
            'files_in':fileset,
            'varno':varno}
           data_list_plot.append(data_dict_plot)

    return data_list_plot


def make_scatter(files_in,
                 names_in,  
                 pathwork, 
                 datestart,
                 dateend,
                 region, 
                 family, 
                 flag_criteria, 
                 fonction, 
                 boxsizex, 
                 boxsizey, 
                 Proj, # Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
                 mode,
                 Points,
                 id_stn,
                 channel,
                 n_cpu):

 
   pikobs.delete_create_folder(pathwork)
   for file_in, name_in in zip(files_in, names_in):

       data_list = create_data_list(datestart,
                                    dateend, 
                                    family, 
                                    file_in,
                                    name_in,
                                    pathwork,
                                    boxsizex,
                                    boxsizey, 
                                    fonction, 
                                    flag_criteria, 
                                    region)
       
       import time
       import dask
       t0 = time.time()
       if n_cpu==1:
        for  data_ in data_list:  
            print ("Serie")
            create_and_populate_moyenne_table(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['fonction'],
                                              data_['boxsizex'],
                                              data_['boxsizey'])
            
    
    
    
    
       else:
        print (f'in Paralle files for {name_in} = {len(data_list)}')
        with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(create_and_populate_moyenne_table)(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['fonction'],
                                              data_['boxsizex'],
                                              data_['boxsizey'] )for data_ in data_list]
            results = dask.compute(*delayed_funcs)
        
   print ('Total time for Sqlite calculation:',time.time() - t0)  
   data_list_plot = create_data_list_plot(datestart,
                                          dateend, 
                                          family, 
                                          names_in,
                                          pathwork,
                                          boxsizex,
                                          boxsizey, 
                                          fonction, 
                                          flag_criteria, 
                                          region,
                                          id_stn,
                                          channel)
   os.makedirs(f'{pathwork}/scatter_plot')
   t0 = time.time()
   #n_cpu=1
   if n_cpu==1:
    for  data_ in data_list_plot:  
        print ("Serie")
        pikobs.scatter_plot(mode, 
                            region,
                            family, 
                            data_['id_stn'], 
                            datestart,
                            dateend, 
                            Points, 
                            boxsizex,
                            boxsizey,
                            Proj, 
                            pathwork,
                            flag_criteria, 
                            fonction,
                            data_['vcoord'],
                            data_['files_in'],
                            names_in, data_['varno'])
   else:
      print (f'in Paralle plots = {len(data_list_plot)}')
      with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(pikobs.scatter_plot)(mode, 
                                                           region,
                                                           family, 
                                                           data_['id_stn'],
                                                           datestart,
                                                           dateend, 
                                                           Points, 
                                                           boxsizex,
                                                           boxsizey,
                                                           Proj, 
                                                           pathwork,
                                                           flag_criteria, 
                                                           fonction,
                                                           data_['vcoord'],
                                                           data_['files_in'],
                                                           names_in, data_['varno'])for data_ in data_list_plot]

        results = dask.compute(*delayed_funcs)
   print ('Total time:',time.time() - t0 )  
   print (f'check: {pathwork}')
 



def arg_call():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_control_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--control_name', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--path_experience_files', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--experience_name', default='undefined', type=str, help="Directory where input sqlite files are located")
  

    
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', default='undefined', type=str, help="Region")
    parser.add_argument('--family', default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--fonction', nargs="+", default='undefined', type=str, help="Function")
    parser.add_argument('--boxsizex', default='undefined', type=int, help="Box size in X direction")
    parser.add_argument('--boxsizey', default='undefined', type=int, help="Box size in Y direction")
    parser.add_argument('--projection', default='cyl', type=str, help="Projection type (cyl, OrthoN, OrthoS, robinson, Europe, Canada, AmeriqueNord, Npolar, Spolar, reg)")
    parser.add_argument('--mode', default='SIGMA', type=str, help="Mode")
    parser.add_argument('--Points', default='OFF', type=str, help="Points")
    parser.add_argument('--id_stn', default='one_per_plot', type=str, help="id_stn") 
    parser.add_argument('--channel', default='one_per_plot', type=str, help="channel")
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()
    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.path_control_files == 'undefined':
        files_in = [args.path_experience_files]
        names_in = [args.experience_name]
    else:    
        if args.path_experience_files == 'undefined':
            raise ValueError('You must specify --path_experience_files')
        if args.experience_name == 'undefined':
            raise ValueError('You must specify --experience_name')
        else:

            files_in = [args.path_control_files, args.path_experience_files]
            names_in = [args.control_name, args.experience_name]
    
    if args.pathwork == 'undefined':
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
    if args.fonction == 'undefined':
        raise ValueError('You must specify --fonction')
    if args.boxsizex == 'undefined':
        raise ValueError('You must specify --boxsizex')
    if args.boxsizey == 'undefined':
        raise ValueError('You must specify --boxsizey')


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_scatter(files_in,
                          names_in,    
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.fonction,
                          args.boxsizex,
                          args.boxsizey,
                          args.projection,
                          args.mode,
                          args.Points,
                          args.id_stn,
                          args.channel,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()




