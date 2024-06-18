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


def create_timeserie_table(family, 
                           new_db_filename,
                           existing_db_filename, 
                           region_seleccionada, 
                           selected_flags, 
                           FONCTION, 
                           boxsizex, 
                           boxsizey,
                           varno):
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
    print (existing_db_filename)
    # Attach the existing database
    new_db_cursor.execute(f"ATTACH DATABASE '{existing_db_filename}' AS db;")
    # load extension CMC
    new_db_conn.enable_load_extension(True)
    extension_dir = f'{os.path.dirname(pikobs.__file__)}/extension/libudfsqlite-shared.so'
    new_db_conn.execute(f"SELECT load_extension('{extension_dir}')")
   
    # Create the 'moyenne' table in the new database if it doesn't exist
    new_db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS timeserie (
            DATE INTEGER, 
            varno INTEGER,
            Nrej INTEGER,
            Nacc INTIGER,
            SUMx FLOAT,
            SUMx2 FLOAT,
            N INTEGER, 
            id_stn TEXT, 
            vcoord FLOAT,
            flag INTERGER
        );
    """)

    # Execute the data insertion from the existing database
    query = f"""
    INSERT INTO timeserie (
         DATE, 
         varno,
         Nrej,
         Nacc,
         SUMx,
         SUMx2,
         N, 
         id_stn, 
         vcoord,
         flag

    )
    SELECT
        isodatetime({date}) AS DATE, 
        varno AS VARNO,
        SUM(flag & 512=512) AS Nrej,
        SUM(flag & 4096=4096) AS Nacc,
        SUM(OMP) / (count(*))  AS SUMx,
        SQRT( SUM(OMP * OMP) / (count(*)) -  (SUM(OMP) / (count(*) )) * (SUM(OMP) / (count(*) )) ) AS SUMx2,
        --SUM(OMP) AS SUMx,
        --SUM(OMP*OMP) AS SUMx2,
        count(*) AS N,
        id_stn  AS id_stn,
        vcoord AS vcoord,
        flag AS flag

    FROM
        db.header
    NATURAL JOIN
        db.DATA
    WHERE
        VARNO = {int(varno)}
        AND obsvalue IS NOT NULL
        --   AND ID_STN LIKE 'id_stn'
        --   AND vcoord IN (vcoord)
    
        {flag_criteria}
        {LATLONCRIT}
    --    {VCOCRIT}
    GROUP BY
        DATE
  --  HAVING 
--     SUM(OMP IS NOT NULL) >= 50;
    """
    print (query)
    new_db_cursor.execute(query)

    # Commit changes and detach the existing database
    new_db_conn.commit()
    new_db_cursor.execute("DETACH DATABASE db;")


    # Close the connections
    new_db_conn.close()
from datetime import datetime, timedelta

def create_data_list(datestart1, dateend1, family, pathin, pathwork, boxsizex, boxsizey, fonction, flag_criteria, region_seleccionada):
    data_list = []
    #print (datestart1, dateend1, family, pathin, pathwork, boxsizex, boxsizey, fonction, flag_criteria, region_seleccionada)
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
            'db_new': f'{pathwork}/timeserie_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db',
            'region': region_seleccionada,
            'flag_criteria': flag_criteria,
            'fonction': fonction,
            'boxsizex': boxsizex,
            'boxsizey': boxsizey,
            'varno'   : varno
        }
        data_list.append(data_dict)

        # Update the current_date in the loop by adding 6 hours
        current_date += delta

    return data_list

def create_data_list_plot(datestart1,
                          dateend1, 
                          family, 
                          pathin, 
                          pathwork, 
                          boxsizex, 
                          boxsizey, 
                          fonction, 
                          flag_criteria, 
                          region_seleccionada, 
                          id_stn, 
                          channel):
    data_list_plot = []
    filedb = f'{pathwork}/timeserie_{datestart1}_{dateend1}_{fonction}_{flag_criteria}_{family}.db'
    conn = sqlite3.connect(filedb)
    cursor = conn.cursor()
    #print ('david',id_stn,'alone',id_stn=='alone')
    if id_stn=='alone':
        #print (7)
        query = "SELECT DISTINCT id_stn FROM timeserie;"
        cursor.execute(query)
        id_stns = cursor.fetchall()
    else:
        #print (9)
        id_stns = ['all']

    for idstn in id_stns:
       
       #print (idstn)   
       if id_stn=='alone':
          criter =f'where id_stn = "{idstn[0]}"'
       
       elif id_stn=='all':

         criter =' '

       
       if channel =='alone':

          query = f"SELECT DISTINCT vcoord, varno FROM timeserie {criter} ORDER BY vcoord ASC;"
          #print (query)
          cursor.execute(query)
          vcoords = cursor.fetchall()
       elif channel =='all':
          
          query = f"SELECT DISTINCT 'all', varno FROM timeserie;"
          #print (query)
          cursor.execute(query)
          vcoords = cursor.fetchall()
          print ('++2', vcoords)


        
       for vcoord, varno in vcoords:
           print ('++',vcoord, varno)

           data_dict_plot = {
            'id_stn': idstn,
            'vcoord': vcoord,
            'varno': varno}
           data_list_plot.append(data_dict_plot)
    return data_list_plot


def make_scatter(pathin,
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
   data_list = create_data_list(datestart,
                                dateend, 
                                family, 
                                pathin, 
                                pathwork,
                                boxsizex,
                                boxsizey, 
                                fonction, 
                                flag_criteria, 
                                region)
   
   import time
   import dask
   t0 = time.time()
   print (n_cpu)
   if n_cpu==1:
    for  data_ in data_list:  
        print ("Serie")
        create_timeserie_table(data_['family'], 
                               data_['db_new'], 
                               data_['filein'],
                               data_['region'],
                               data_['flag_criteria'],
                               data_['fonction'],
                               data_['boxsizex'],
                               data_['boxsizey'],
                               data_['varno'])
        




   else:
    print (f'in Paralle = {len(data_list)}')
    with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(create_timeserie_table)(data_['family'], 
                                          data_['db_new'], 
                                          data_['filein'],
                                          data_['region'],
                                          data_['flag_criteria'],
                                          data_['fonction'],
                                          data_['boxsizex'],
                                          data_['boxsizey'],
                                          data_['varno'])for data_ in data_list]
        results = dask.compute(*delayed_funcs)
    
   tn= time.time()
   print ('Total time:',tn-t0 )  
   data_list_plot = create_data_list_plot(datestart,
                                dateend, 
                                family, 
                                pathin, 
                                pathwork,
                                boxsizex,
                                boxsizey, 
                                fonction, 
                                flag_criteria, 
                                region,
                                id_stn,
                                channel)
   print  ('.......' ,data_list_plot )                           
   os.makedirs(f'{pathwork}/timeserie')
   n_cpu = 1
   fig_title = ''
   if n_cpu==1:
    for  data_ in data_list_plot:  
        print ("Serie")
        pikobs.timeserie_plot(
                           pathwork,
              datestart,
              dateend,
              fonction,
              flag_criteria,
              family,
              region,
              fig_title,
              data_['vcoord'], 
              data_['id_stn'], 
              data_['varno'])  
   else:
      print (f'in Paralle = {len(data_list_plot)}')
      with dask.distributed.Client(processes=True, threads_per_worker=1, 
                                       n_workers=n_cpu, 
                                       silence_logs=40) as client:
        delayed_funcs = [dask.delayed(pikobs.scatter_plot)(
                           mode, 
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
                           data_['vcoord'])for data_ in data_list_plot]

        results = dask.compute(*delayed_funcs)

 



def arg_call():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument('--pathin', default='undefined', type=str, help="Directory where input sqlite files are located")
    parser.add_argument('--pathwork', default='undefined', type=str, help="Working directory")
    parser.add_argument('--datestart', default='undefined', type=str, help="Start date")
    parser.add_argument('--dateend', default='undefined', type=str, help="End date")
    parser.add_argument('--region', default='undefined', type=str, help="Region")
    parser.add_argument('--family', default='undefined', type=str, help="Family")
    parser.add_argument('--flags_criteria', default='undefined', type=str, help="Flags criteria")
    parser.add_argument('--fonction', default='undefined', type=str, help="Function")
    parser.add_argument('--boxsizex', default=-1, type=int, help="Box size in X direction")
    parser.add_argument('--boxsizey', default=-1, type=int, help="Box size in Y direction")
    parser.add_argument('--Proj', default='cyl', type=str, help="Projection type (cyl, OrthoN, OrthoS, robinson, Europe, Canada, AmeriqueNord, Npolar, Spolar, reg)")
    parser.add_argument('--mode', default='SIGMA', type=str, help="Mode")
    parser.add_argument('--Points', default='OFF', type=str, help="Points")
    parser.add_argument('--id_stn', default='all', type=str, help="id_stn") 
    parser.add_argument('--channel', default='all', type=str, help="channel")
    parser.add_argument('--n_cpus', default=1, type=int, help="Number of CPUs")

    args = parser.parse_args()
    for arg in vars(args):
       print (f'--{arg} {getattr(args, arg)}')
    # Check if each argument is 'undefined'
    if args.pathin == 'undefined':
        raise ValueError('You must specify --pathin')
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
    if args.boxsizex == -1:
        raise ValueError('You must specify --boxsizex')
    if args.boxsizey == -1:
        raise ValueError('You must specify --boxsizey')


    # Comment
    # Proj='cyl' // Proj=='OrthoN'// Proj=='OrthoS'// Proj=='robinson' // Proj=='Europe' // Proj=='Canada' // Proj=='AmeriqueNord' // Proj=='Npolar' //  Proj=='Spolar' // Proj == 'reg'
  

    #print("in")
    # Call your function with the arguments
    sys.exit(make_scatter(args.pathin,
                          args.pathwork,
                          args.datestart,
                          args.dateend,
                          args.region,
                          args.family,
                          args.flags_criteria,
                          args.fonction,
                          args.boxsizex,
                          args.boxsizey,
                          args.Proj,
                          args.mode,
                          args.Points,
                          args.id_stn,
                          args.channel,
                          args.n_cpus))

if __name__ == '__main__':
    args = arg_call()




