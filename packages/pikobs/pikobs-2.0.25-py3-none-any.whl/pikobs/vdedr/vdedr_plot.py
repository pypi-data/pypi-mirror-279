#!/usr/bin/python3
###############################################################################
#
#                              plots_profils.py 
#
# Purpose: Graphs of radiance statistics 
#
# Author: Sylvain Heilliette, Pierre Koclas and David Lobon  2020
#
# Modifications:
#     -2020  David Lobon 
#        - various updates
# Syntax:
#
#    plots_profils.py 
#  
#         
###############################################################################
import sys
import csv
import math
import matplotlib as mpl
mpl.use('Agg')
import pylab
import sqlite3
import numpy as np
ROUGE = '#FF9999'
ROUGEPUR = '#FF0000'
VERT = '#009900'
BLEU = '#1569C7'
NOIR = '#000000'
COULEURS = [BLEU, ROUGEPUR, ROUGE, VERT, NOIR]

#===============================================================================
GRAPHE_NOMVAR = {'11215':'U COMPONENT OF WIND (10M)',
                 '11216':'V COMPONENT OF WIND (10M)',
                 '12004':'DRY BULB TEMPERATURE AT 2M',
                 '10051':'PRESSURE REDUCED TO MEAN SEA LEVEL',
                 '10004':'PRESSURE', '12203':'DEW POINT DEPRESSION (2M)',
                 '12001':'TEMPERATURE/DRY BULB', 
                 '11003':'U COMPONENT OF WIND',
                 '11004':'V COMPONENT OF WIND',
                 '12192':'DEW POINT DEPRESSION',
                 '12163':'BRIGHTNESS TEMPERATURE',
                 '15036':'ATMOSPHERIC REFRACTIVITY',
                 '11001':'WIND DIRECTION',
                 '11002':'WIND SPEED',
                 '11011':'WIND DIRECTION AT 10M', 
                 '11012':'WIND SPEED AT 10M'}
#==============================================================================
#

def read_bias_csv(filename):
    """ Function to read data from csv file """
    hdl = open (filename.strip(), 'r') # Open file for reading
    reader = csv.DictReader(hdl, delimiter = ",")
    Niveaux = []
    Bomp = []
    Bcor = []
    Nomb = []
    for row in reader:
        ilev = round(float(row['Chan']))
        bias = float(row['AvgOMP'])
        bcor = float(row['BiasCor'])
        nobs = int(row['Ntot'])
        if nobs > 2 and \
                math.fabs(bias + 99.9) > 0.000001 and \
                math.fabs(bcor + 99.9) > 0.000001 :
            Niveaux.append( ilev )
            Bomp.append( bias )
            Bcor.append( bcor )
            Nomb.append( nobs )
    hdl.close()
    return Niveaux, Bomp, Bcor, Nomb
def read_delta_err_csv(filename):
    """ Function to read data from csv file """
    hdl = open (filename.strip(), 'r') # Open file for reading
    reader = csv.DictReader(hdl, delimiter = ",")
    Niveaux = []
    Bomp = []
    Somp = []
    Nomb = []
    for row in reader:
        ilev = round(float(row['Chan']))
        bias = float(row['AvgOMP'])
        std = float(row['StdOMP'])
        nobs = int(row['Ntot'])
        if nobs > 2 and \
                math.fabs(bias + 99.9) > 0.000001 and \
                math.fabs(std + 99.9) > 0.000001 :
            Niveaux.append( ilev )
            Bomp.append( bias )
            Somp.append( std )
            Nomb.append( nobs )
    hdl.close()
    return Niveaux, Bomp, Somp, Nomb

def read_delta_err_oma_csv(filename):
    """ Function to read data from csv file """
    hdl = open (filename.strip(), 'r') # Open file for reading
    reader = csv.DictReader(hdl, delimiter = ",")
    Niveaux = []
    Bomp = []
    Somp = []
    Nomb = []
    for row in reader:
        ilev = round(float(row['Chan']))
        bias = float(row['AvgOMA'])
        std = float(row['StdOMA'])
        nobs = int(row['Ntot'])
        if nobs > 2 and \
                math.fabs(bias + 99.9) > 0.000001 and \
                math.fabs(std + 99.9) > 0.000001 :
            Niveaux.append( ilev )
            Bomp.append( bias )
            Somp.append( std )
            Nomb.append( nobs )
    hdl.close()
    return Niveaux, Bomp, Somp, Nomb


def usage(arg):
    print ("Usage:", arg[0])
    print ("vcoord_type file1 famille region varno platform label1 debut fin type file2 label2")

def vdedr_plot (pathwork,datestart, dateend, fonction,flag_type, family,region, fig_title, plot_type,files_in,names_in ,id_stn, varno,mode):
    
 #   LARG = []
  #  n=1
  #  for arg in sys.argv:
  #      LARG.append(arg)
   #     print (arg,n)
  #      n=n+1
  ##  if (len(LARG) != 14):
  #      usage(LARG)
  #      sys.exit(-1)
  #  
   # files = []
    
    vcoord_type =  'CANAL'# LARG[1]
    files = files_in
    famille = family
    region  = region
    varno = varno
    platf = id_stn
    label = names_in[0]
    debut = datestart
    fin = dateend
    fonction = fonction
    mode = mode
    print (" varno= ", varno)
    if varno  in GRAPHE_NOMVAR :
        Nom = GRAPHE_NOMVAR[varno]
    else:
        Nom = varno
    print (' LE NOM est :', Nom)
    
    
    #files.append(LARG[11])
    label2 = names_in[1]
    
   # print (LARG)
    print (' region = ', region)
    PERIODE = 'From  ' + debut + '   to  ' + fin
    
    #
    #==============================================================================
    order = True
    if ( vcoord_type == 'PRESSION'):
        SIGN = -1
    #   order = False
        vcoord_type_e = 'Pressure'
    elif ( vcoord_type == 'HAUTEUR'):
        SIGN = -1
        vcoord_type_e = 'Height'
    elif ( vcoord_type == 'CANAL'):
        SIGN = -1
        vcoord_type_e = 'Channel'
    else:
        SIGN= -1
        vcoord_type_e = vcoord_type
    
    
    #=================================
    fig = pylab.figure(figsize=(8, 10))
    #=================================
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)
    
    filenumb = 0
    TITRE = 'VERIFS'
    lvl = []
    numb = []
    
    # Conectarse a la base de datos SQLite
    def read_sqlite(file):
        conn = sqlite3.connect(file)
        cursor = conn.cursor()
      #  print (files[0])
        # Ejecutar una consulta SQL
        query =f"""SELECT vcoord AS vcoord,        
                          sum(sumx)/sum(Ntot) AS AvgOMP,
                          sum(sumy)/sum(Ntot) AS AvgOMA , 
                          sqrt( sum(sumx2)/sum(Ntot) -sum(sumx)/sum(Ntot)*sum(sumx)/sum(Ntot)) AS StdOMP, 
                          sqrt( sum(sumy2)/sum(Ntot) -sum(sumy)/sum(Ntot)*sum(sumy)/sum(Ntot)) AS StdOMA,
                          sum(Ntot) AS Ntot,
                          sum(sumStat)/sum(Ntot) AS BiasCor
                   FROM serie_cardio 
                   WHERE id_stn='{id_stn}' 
                   GROUP BY id_stn, vcoord;"""
      #  print (query)
        cursor.execute(query)
    
        # Obtener los resultados de la consulta
        results = cursor.fetchall()
    
        # Cerrar la conexión a la base de datos
        conn.close()
        vcoord = [result[0] for result in results]
        AvgOMP = [result[1] for result in results]
        AvgOMA = [result[2] for result in results]
        StdOMP = [result[3] for result in results]
    
        StdOMA = [result[4] for result in results]
        Ntot   = [result[5] for result in results]
        BiasCor= [result[6] for result in results]
        return vcoord, AvgOMP, AvgOMA, StdOMP, StdOMA, Ntot, BiasCor
   
    
    # Print the list of results
   # print(results_list)        
   #a# exit()
    #Niveau = []
    vcoord1, AvgOMP1, AvgOMA1, StdOMP1, StdOMA1, Ntot1, BiasCor1 = read_sqlite(files[0])
    vcoord2, AvgOMP2, AvgOMA2, StdOMP2, StdOMA2, Ntot2, BiasCor2 = read_sqlite(files[1])
    for mode in ['bias',"delta_err","delta_err_oma"]:
        if (mode=="bias"):
          lvl1 = vcoord1
          Bomp1 = AvgOMP1
          Bcor1 = BiasCor1
          Nomb1 = Ntot1
    
          lvl2 = vcoord2
          Bomp2 = AvgOMP2
          Bcor2 = BiasCor2
          Nomb2 = Ntot2
    
         # lvl1, Bomp1, Bcor1, Nomb1 = read_bias_csv(files[0])
         # lvl2, Bomp2, Bcor2, Nomb2 = read_bias_csv(files[1])
        if (mode=="delta_err"):
           lvl1= vcoord1
           Bomp1 = AvgOMP1
           Somp1 = StdOMP1
           Nomb1 = Ntot1
          
           lvl2= vcoord2
           Bomp2 = AvgOMP2
           Somp2 = StdOMP2
           Nomb2 = Ntot2
    
          #lvl1, Bomp1, Somp1, Nomb1 = read_delta_err_csv(files[0])
          #lvl2, Bomp2, Somp2, Nomb2 = read_delta_err_csv(files[1])
        if (mode=="delta_err_oma"):
    
           lvl1= vcoord1
           Bomp1 = AvgOMA1
           Somp1 = StdOMA1
           Nomb1 = Ntot1
          
           lvl2= vcoord2
           Bomp2 = AvgOMA2
           Somp2 = StdOMA2
           Nomb2 = Ntot2
          #lvl1, Bomp1, Somp1, Nomb1 = read_delta_err_oma_csv(files[0])
         # lvl2, Bomp2, Somp2, Nomb2 = read_delta_err_oma_csv(files[1])
        lset1 = set( lvl1 )
        lset2 = set( lvl2 )
        
        common_levels = lset1 & lset2
        
        lvlm = sorted(list(common_levels), reverse = order)
        if (mode=="bias"):
          delta_residual = [] 
          delta_raw = []
        if (mode=="delta_err"):
          delta_sigma = [] 
          delta_N = []
        if (mode=="delta_err_oma"):
          delta_sigma = [] 
          delta_N = []
        
        n1 = []
        n2 = []
        idlev = range(0,len(lvlm))
        
        for lev in lvlm:
            pos1 = lvl1.index(lev)
            pos2 = lvl2.index(lev)
            if (mode=="bias"):
              delta_residual.append( Bomp2[pos2] - Bomp1[pos1]  )
              delta_raw.append( Bomp2[pos2] - Bcor2[pos2] - Bomp1[pos1] + Bcor1[pos1])
            if (mode=="delta_err"):
              delta_sigma.append( 100.0 * (Somp2[pos2] - Somp1[pos1]) / Somp1[pos1] )
              delta_N.append( 100.0 * (Nomb2[pos2] - Nomb1[pos1]) / Nomb1[pos1] )
            if (mode=="delta_err_oma"):
              delta_sigma.append( 100.0 * (Somp2[pos2] - Somp1[pos1]) / Somp1[pos1] )
              delta_N.append( 100.0 * (Nomb2[pos2] - Nomb1[pos1]) / Nomb1[pos1] )
          
            n1.append(Nomb1[pos1])
            n2.append(Nomb2[pos2])
        #========================GRAPHIQUE==============================================
        if (mode=="bias"):
          ax.plot(delta_residual, idlev, linestyle = '-', marker = 'o', \
                    color = COULEURS[2], markersize = 4 )
          ax.plot(delta_raw, idlev, linestyle = '-', marker = 'p', \
                    color = COULEURS[3], markersize = 4 ) 
        if (mode=="delta_err"):
          ax.plot(delta_sigma, idlev, linestyle = '-', marker = 'o', \
                    color = COULEURS[2], markersize = 4 )
          ax.plot(delta_N, idlev, linestyle = '-', marker = 'p', \
                    color = COULEURS[3], markersize = 4 ) 
        if (mode=="delta_err_oma"):
          ax.plot(delta_sigma, idlev, linestyle = '-', marker = 'o', \
                    color = COULEURS[2], markersize = 4 )
          ax.plot(delta_N, idlev, linestyle = '-', marker = 'p', \
                    color = COULEURS[3], markersize = 4 ) 
        
        
        #===============================================================================
        
        #======TICK MARKS=ET LABEL===============================
        xlim = pylab.get(pylab.gca(), 'xlim')
        if varno  in GRAPHE_NOMVAR :
            Nom2 = GRAPHE_NOMVAR[varno]
        else:
            Nom2 = varno
        ylim = (min(idlev), max(idlev) )
            
        yticks = map(str, idlev)
        ax.set_yticks(idlev)
        
        yticks = map(str, lvlm)
        ax.set_yticklabels(yticks, fontsize = 6)
        
         
        pylab.setp(pylab.gca(), ylim = ylim[::SIGN])
                
        ax.set_ylabel(vcoord_type_e, color = NOIR, bbox = dict(facecolor=ROUGE), \
                          fontsize = 16)
        #========================================================
        
        #=NOMBRE DE NONNEES ==================================================
        datapt = []
        for y in  range(0, len(lvlm) ):
            datapt.append(( xlim[1], idlev[y] ) )
        display_to_ax = ax.transAxes.inverted().transform
        data_to_display = ax.transData.transform
        
        if ( len(datapt) > 0):
            ax_pts = display_to_ax(data_to_display(datapt))
            for y in  range(0, len(lvlm) ):
                ix, iy = ax_pts[y]
                pylab.text(ix + .01 , iy, n1[y], fontsize = 6, \
                               color = COULEURS[0], transform = ax.transAxes )
                pylab.text(ix + .07 , iy, n2[y], fontsize = 6, \
                               color = COULEURS[1], transform = ax.transAxes )
        #====================================================================
        #----------------------------------------------------------------------
        famille1 = famille + " " + platf
        REGION1 = region
        LABEL1 = label
        LABEL2 = label2
        if (mode=="bias"):
          legendlist = [' residual bias ', ' raw bias ']
        if (mode=="delta_err"):
          legendlist = ['% sigma ', '% Nobs ']
        if (mode=="delta_err_oma"):
          legendlist = ['% sigma ', '% Nobs ']
        l1 = pylab.legend(legendlist, columnspacing=1, fancybox=True, ncol=2, \
                              shadow = False, loc = (0.50, +1.00), prop = {'size':12})
        ltext = pylab.gca().get_legend().get_texts()
        print(ltext)
        pylab.setp(ltext[0], fontsize = 10, color = 'k')
        #----------------------------------------------------------------------
        bbox_props = dict(facecolor = BLEU, boxstyle = 'round')
        pylab.text(-.03, -0.05, f"{famille1}  {Nom} {fonction}", \
                         fontsize = 10, bbox = bbox_props, transform = ax.transAxes)
        pylab.text(.00, 1.05, REGION1, fontsize = 10, \
                        bbox = dict(facecolor = BLEU, boxstyle = 'round'), \
                        transform = ax.transAxes)
        pylab.text(.25, 1.05, PERIODE, fontsize = 10, \
                        bbox = dict(facecolor = BLEU, boxstyle = 'round'), \
                        transform = ax.transAxes)
        pylab.text(.70, 1.05, LABEL2 + ' - ' + LABEL1, fontsize = 10, \
                        bbox = dict(facecolor = BLEU, boxstyle = 'round'), \
                        transform = ax.transAxes)
        
        #==========================================================
        #pylab.show()
        pylab.savefig(f'{pathwork}/vdedr/{varno}_{id_stn}_{mode}.png', format = 'png', dpi = 100)
        #==========================================================
