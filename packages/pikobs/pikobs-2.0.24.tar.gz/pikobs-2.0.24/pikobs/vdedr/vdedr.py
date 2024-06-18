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
                        FONCTION, 
                       # id_stn,
                       # vcoord, 
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
    print (existing_db_filename)
    match = re.search(pattern, existing_db_filename)

    if match:
        date = match.group(1)
       
    else:
        print("No 10 digits found in the string.")
    
    # Connect to the new database
  
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
  
    
    query = """
           CREATE TABLE IF NOT EXISTS serie_cardio ( 
            DATE INTEGER,
            sumx FLOAT, 
            sumy FLOAT,
            sumz FLOAT,
            sumx2 FLOAT,
            sumy2 float,
            sumz2 float,
            sumStat float,
            Ntot INTEGER,
            vcoord float,
            varno INTEGER,
            id_stn  TEXT
        );
    """
   # print (query)
    new_db_cursor.execute(query)

    query=f"""INSERT INTO serie_cardio (

            DATE,
            sumx, 
            sumy,
            sumz,
            sumx2,
            sumy2,
            sumz2,
            sumStat,
            Ntot,
            vcoord,
            varno,
            id_stn
        )
    
    
             SELECT 
                 isodatetime({date}) ,  
                 sum(oma),
                 sum({FONCTION}),
                 sum(obsvalue),
                 sum(oma*oma),
                 sum({FONCTION}*{FONCTION}),
                 sum(obsvalue*obsvalue),
                 sum( {STATB} ),
                 count(*),
                 vcoord,
                 varno,
                 id_stn
            FROM 
                 header
             NATURAL JOIN 
                 data
             WHERE 
                 VARNO = {int(varno)}
                 and obsvalue is not null
              --   AND ID_STN LIKE 'id_stn'
              --   AND vcoord IN (vcoord)
                 {flag_criteria}
                 {LATLONCRIT}
                 {VCOCRIT}
             GROUP BY 
                 VCOORD, ID_STN, vcoord """
    #print (query)
    new_db_cursor.execute(query)

    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")
    new_db_conn.commit()




    # Commit changes and detach the existing database
    #new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()

def create_data_list_cardio(datestart1, 
                            dateend1,
                            family,
                            pathin, 
                            name,
                            pathwork,
                            fonction, 
                            flag_criteria,
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
  #  print (flag_criteria)
    
    #flag_criteria = generate_flag_criteria(flag_criteria)

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
       # print ( "file_path_name", file_path_name)
        conn = sqlite3.connect(file_path_name)
        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        channel ='all'
        id_stn ='all'
        #  Create a new dictionary and append it to the list
        data_dict = {'family': family,
                          'filein': f'{pathin}/{filename}',
                          'db_new': f'{pathwork}/vdedr_{name}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db',
                          'region': region_seleccionada,
                          'flag_criteria': flag_criteria,
                          'fonction': fonction,
                          'varno':  varno,
                          'vcoord': channel,
                          'id_stn': id_stn}
        data_list_cardio.append(data_dict)
        conn.close()

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list_cardio





def create_data_list_plot(datestart1,
                          dateend1, 
                          family, 
                          pathwork, 
                          fonction, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          channel,
                          files_in,
                          names_in):
    data_list_plot = []
    filedb_control = f'{pathwork}/vdedr_{names_in[0]}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db'
    filedb_experience = f'{pathwork}/vdedr_{names_in[1]}_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db'
 
    conn = sqlite3.connect(filedb_control)
    cursor = conn.cursor()

    if id_stn=='alone':
        query = "SELECT DISTINCT id_stn, varno  FROM serie_cardio;"
        cursor.execute(query)
        id_stns = cursor.fetchall()
    else:
        id_stns = 'all'

    for idstn, varno in id_stns:
       #if id_stn=='alone':
        #  criter =f'where id_stn = "{idstn[0]}"'
       
       #elif id_stn=='all':

       #  criter =' '

      # query = f"SELECT DISTINCT chan, varno  FROM serie_cardio {criter} ORDER BY chan ASC;"
      # cursor.execute(query)
      # vcoords = cursor.fetchall()
       #for vcoord, varno in vcoords:
           data_dict_plot = {
            'files_in': [filedb_control,filedb_experience],
            'names_in': names_in,
            'id_stn': idstn,
            'varno': varno}
           data_list_plot.append(data_dict_plot)
    return data_list_plot


def make_cardio( files_in,
                 names_in,
                 pathwork, 
                 datestart,
                 dateend,
                 region, 
                 family, 
                 flag_criteria, 
                 fonction, 
                 id_stn,
                 channel,
                 plot_type,
                 plot_title,
                 n_cpu):


   pikobs.delete_create_folder(pathwork)
   for file_in, name_in in zip(files_in,names_in):
       
       

       data_list_cardio = create_data_list_cardio(datestart,
                                           dateend, 
                                           family, 
                                           file_in,
                                           name_in,
                                           pathwork,
                                           fonction, 
                                           flag_criteria, 
                                           region)
       
       import time
       import dask
       t0 = time.time()
       #n_cpu=1
       if n_cpu==1:
        for  data_ in data_list_cardio:  
            print ("Serie")
            create_serie_cardio(data_['family'], 
                                data_['db_new'], 
                                data_['filein'],
                                data_['region'],
                                data_['flag_criteria'],
                                data_['fonction'],
                                data_['varno'])
    
    
    
    
       else:
        print (f'in Paralle = {len(data_list_cardio)}')
        with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                           n_workers=n_cpu, 
                                           silence_logs=40) as client:
            delayed_funcs = [dask.delayed(create_serie_cardio)(data_['family'], 
                                              data_['db_new'], 
                                              data_['filein'],
                                              data_['region'],
                                              data_['flag_criteria'],
                                              data_['fonction'],
                                              data_['varno'])for data_ in data_list_cardio]
            results = dask.compute(*delayed_funcs)
        
       tn= time.time()
       print ('Total time:',tn-t0 ) 
   data_list_plot = create_data_list_plot(datestart,
                                dateend, 
                                family, 
                                pathwork,
                                fonction, 
                                flag_criteria, 
                                region,
                                id_stn,
                                channel,
                                files_in,
                                names_in)



  # exit()   
   os.makedirs(f'{pathwork}/vdedr')
   #print (data_list_plot )
   n_cpu=1
   if n_cpu==1: 
      print (f'Serie= {len(data_list_plot)}')
      for  data_ in data_list_plot:  
          mode='bias'
          pikobs.vdedr_plot(pathwork,
                            datestart,
                            dateend,
                            fonction,
                            flag_criteria,
                            family,
                            region,
                            plot_title,
                            plot_type, 
                            data_['files_in'],
                            data_['names_in'],
                            data_['id_stn'], 
                            data_['varno'],
                            mode)
   else:
      print (f'in Paralle = {len(data_list_plot)}')
      with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(pikobs.vdedr_plot)(
                           pathwork,
                             datestart,
                             dateend,
                             fonction,
                             flag_criteria,
                             family,
                             plot_title,
                             plot_type, 
                             data_['id_stn'], 
                             data_['varno'])for data_ in data_list_plot]

        results = dask.compute(*delayed_funcs)

 



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
    parser.add_argument('--fonction', default='undefined', type=str, help="Function")
    parser.add_argument('--id_stn', default='all', type=str, help="id_stn") 
    parser.add_argument('--channel', default='all', type=str, help="channel") 
    parser.add_argument('--plot_type', default='classic', type=str, help="channel")
    parser.add_argument('--plot_title', default='Plot', type=str, help="channel")

    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()
    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.path_control_files == 'undefined':
        raise ValueError('You must specify --path_control_files')
    elif args.control_name == 'undefined':
        raise ValueError('You must specify --control_name')
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


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_cardio (files_in,
                          names_in,
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.fonction,
                          args.id_stn,
                          args.channel,
                          args.plot_type,
                          args.plot_title,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()




