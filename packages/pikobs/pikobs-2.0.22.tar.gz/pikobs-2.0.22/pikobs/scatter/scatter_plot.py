#!/usr/bin/env python3

#Auteur : Pierre Koclas, May 2021
import os
import sys
import csv
from math import floor,ceil,sqrt
import matplotlib as mpl
mpl.use('Agg')
#import pylab as plt
import matplotlib.pylab as plt
import numpy as np
import matplotlib.colorbar as cbar
import matplotlib.cm as cm
import datetime
import cartopy.crs as ccrs
import cartopy.feature
#from cartopy.mpl.ticker    import LongitudeFormatter,  LatitudeFormatter
import matplotlib.colors as colors
#import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import sqlite3
from matplotlib.collections import PatchCollection
from statistics import median
import pikobs
import optparse

def projectPpoly(PROJ,lat,lon,deltax,deltay,pc):
        X1,Y1  = PROJ.transform_point(lon - deltax,lat-deltay,pc )
        X2,Y2  = PROJ.transform_point(lon - deltax,lat+deltay,pc )
        X3,Y3  = PROJ.transform_point(lon + deltax,lat+deltay,pc )
        X4, Y4 = PROJ.transform_point(lon + deltax,lat-deltay,pc )
        Pt1=[ X1,Y1 ]
        Pt2=[ X2,Y2 ]
        Pt3=[ X3,Y3 ]
        Pt4=[ X4,Y4 ]
        Points4 = [ Pt1, Pt2,Pt3,Pt4 ]
           
        return Points4
def SURFLL(lat1,lat2,lon1,lon2):
#= (pi/180)R^2 |sin(lat1)-sin(lat2)| |lon1-lon2|
    R=6371.
    lat2=min(lat2,90.)
    surf=R*R*(np.pi/180.)*abs ( np.sin(lat2*np.pi/180.) - np.sin(lat1*np.pi/180.) ) *abs( lon2-lon1 )
   # if ( surf == 0.):
    # print (   ' surf=',lat1,lat2,lat2*np.pi/180.,lat1*np.pi/180.,np.sin(lat2*np.pi/180.) ,  np.sin(lat1*np.pi/180.) )
    return surf

def NPSURFLL(lat1, lat2, lon1, lon2):
    R = 6371.
    lat2 = np.minimum(lat2, 90.)
    surf = R**2 * (np.pi/180) * np.abs(np.sin(lat2*np.pi/180) - np.sin(lat1*np.pi/180)) * np.abs(lon2 - lon1)
  #  if np.any(surf == 0.):
    #    print('surf contiene valores cero')
    return surf
def SURFLL2(lat1, lat2, lon1, lon2):
    R = 6371.0
    lat2 = np.minimum(lat2, 90.0)
    surf = R * R * (np.pi / 180.0) * np.abs(np.sin(lat2 * np.pi / 180.0) - np.sin(lat1 * np.pi / 180.0)) * np.abs(lon2 - lon1)
    # Debugging print statements if surface is zero
    zero_surf_indices = (surf == 0.0)
    if np.any(zero_surf_indices):
        print('surf=', lat1[zero_surf_indices], lat2[zero_surf_indices], lat2[zero_surf_indices] * np.pi / 180.0,
              lat1[zero_surf_indices] * np.pi / 180.0,
              np.sin(lat2[zero_surf_indices] * np.pi / 180.0),
              np.sin(lat1[zero_surf_indices] * np.pi / 180.0))
    return surf
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y%m%d%H")
    d2 = datetime.datetime.strptime(d2, "%Y%m%d%H")
    return abs((d2 - d1).days)



import pikobs

def scatter_plot(
                   mode,
                   region,
                   family, 
                   id_stn, 
                   datestart,
                   dateend, 
                   Points,
                   boxsizex,
                   boxsizey, 
                   Proj, 
                   pathwork, 
                   flag_criteria, 
                   fonctions,
                   vcoord,
                   filesin,
                   namesin,
                   varno):

   selected_flags = pikobs.flag_criteria(flag_criteria)


   
   pointsize=0.5
   delta=float(boxsizex)/2.
   deltay=float(boxsizey)/2.
   deltax=float(boxsizex)/2.
   
   #=============================================================
   #============      LECTURE   ================================
   
   for fonction  in  fonctions:

       conn = sqlite3.connect(":memory:")
       cursor = conn.cursor()
       #cursor.execute("SELECT group_concat(distinct (varno))  FROM moyenne")
       #result_varno= cursor.fetchone()
       #varno  = result_varno[0]
       cursor.execute("PRAGMA TEMP_STORE=memory")
       query = f"ATTACH DATABASE '{filesin[0]}' AS db1"
       cursor.execute(query)
       FNAM, FNAMP, SUM, SUM2 = pikobs.type_boxes(fonction)
    
       if len(filesin)>1:
             create_table='boites1'
             info_name = f"{namesin[0]} VS {namesin[1]}"
       else:
             create_table='AVG'
             info_name = f"namesin[0]"

             
       query = f"""CREATE TEMPORARY TABLE {create_table} AS
                   SELECT boite, 
                          lat,
                          lon, 
                          varno, 
                          vcoord,
                          SUM({SUM})/SUM(CAST(N AS FLOAT)) AVG,
                          SQRT(SUM({SUM2})/SUM(CAST(N AS FLOAT)) - SUM({SUM})/SUM(CAST(N AS FLOAT))*SUM({SUM})/SUM(CAST(N AS FLOAT))) STD,
                          SUM(sumstat)/SUM(CAST(N AS FLOAT)) BCORR,
                          SUM(n) N
                   FROM db1.moyenne
                   
                   WHERE vcoord = {vcoord} and id_stn='{id_stn}' -- {selected_flags}
                   GROUP BY boite, lat, lon, varno;"""
       cursor.execute(query)

       if len(filesin)>1:
           query = f"ATTACH DATABASE '{filesin[1]}' AS db2"
           cursor.execute(query)
           query = f"""CREATE TEMPORARY TABLE boites2 AS
                       SELECT boite, lat, lon, varno, vcoord,
                              SUM({SUM})/SUM(CAST(N AS FLOAT)) AVG,
                              SQRT(SUM({SUM2})/SUM(CAST(N AS FLOAT)) - SUM({SUM})/SUM(CAST(N AS FLOAT))*SUM({SUM})/SUM(CAST(N AS FLOAT))) STD,
                              SUM(sumstat)/SUM(CAST(N AS FLOAT)) BCORR,
                              SUM(n) N
                       FROM db2.moyenne
                       WHERE  vcoord = {vcoord} and id_stn='{id_stn}'-- {selected_flags}
                       GROUP BY boite, lat, lon, varno;"""
           cursor.execute(query)

           query = f"""Create temporary table AVG as 
                       SELECT BOITES1.boite BOITE,
                              BOITES1.lat LAT,
                              BOITES1.lon LON,
                              BOITES1.vcoord VCOORD,
                              BOITES1.varno VARNO,
                              BOITES2.avg - BOITES1.avg AVG,
                              BOITES2.std - BOITES1.std STD, 
                              BOITES2.bcorr - BOITES1.bcorr BCORR ,  
                              BOITES2.N - BOITES1.N  N, BOITES1.N N1 ,BOITES2.N N2 
                      FROM BOITES1,BOITES2 
                      WHERE  BOITES1.boite=BOITES2.boite and BOITES1.VCOORD=BOITES2.VCOORD"""
           cursor.execute(query)

       query = f"""
        SELECT lat, lon, avg, std, N, N1, N2
        FROM AVG;
       """
       cursor.execute(query)
    
       cursor.execute(query)
       results = cursor.fetchall()    
       # Convertir a arrays numpy
       lat = np.array([row[0] for row in results])
       lon = np.array([row[1] for row in results])
       Bomp = np.array([row[2] for row in results])
       Somp = np.array([row[3] for row in results])
       nombre = np.array([row[4] for row in results])
       dens = nombre/NPSURFLL(lat-deltay,lat+deltay,lon-deltax,lon + deltax)


       index_none=np.where(Somp ==None)
       lat = np.delete(lat, index_none) 
       lon = np.delete(lon, index_none)
       Bomp = np.delete(Bomp, index_none)
       Somp = np.delete(Somp, index_none)
       nombre = np.delete(nombre, index_none)
    
       query = f"""select  
                  '{datestart}',
                  '{dateend}',
                  '{family}',
                  '{varno}' , 
                   avg(avg)  , 
                   avg(std) ,
                   sum(N) 
                   From  
                   AVG where vcoord in ({vcoord}) and varno = {varno} ;"""
       cursor.execute(query)
       results = cursor.fetchall()   
       debut  = np.array([row[0] for row in results])
       fin    = np.array([row[1] for row in results])
       familys = np.array([row[2] for row in results])
       varnos  = np.array([row[3] for row in results])
       Mu     = np.array([row[4] for row in results])
       Sigma  = np.array([row[5] for row in results])
       Nobs   = np.array([row[6] for row in results])
       # Close the connection

       conn.close()

       # Round Sigma to 3 decimal places
       Sigma = np.round(Sigma, 3)
       
       # Define variables
       vartyp = fonction
       PERIODE = f'From {datestart} To {dateend}'
       NDAYS = max(1, days_between(datestart, dateend))
       variable_name, units, vcoord_type = pikobs.type_varno(varnos[0])
       Nomvar = f"{variable_name} {units} \n {id_stn} Canal {int(vcoord)}"
       mode = 'MOYENNE'
       
       # Set OMP based on mode
       OMP = Somp if mode == 'SIGMA' else Bomp
       OMP = np.nan_to_num(OMP, nan=np.nan)  # Replace NaNs with specified value
       
       # Plot setup
       fig = plt.figure(figsize=(10, 10))
       Alpha = 1.0
       Ninterv = 10
       cmap = cm.get_cmap('seismic', lut=Ninterv)
       
       # Filter OMP for valid float values
       OMPm = [value for value in OMP if isinstance(value, float)]
       vmin, vmax = round(np.nanmin(OMPm)), round(np.nanmax(OMPm))
       norm = cm.colors.Normalize(vmin=vmin, vmax=vmax)
       y = np.linspace(vmin, vmax, Ninterv + 1)
       STRING1 = '%.0f'
       # Handle different variable types
       if vartyp == 'dens': 
          # Ninterv = 9
           OMP = dens / NDAYS
           vmax = max(OMP)
           if vmax  ==0:
              vmax=1
           cmap = cm.get_cmap('PuRd', lut=Ninterv)
           vmin = 0.
       
       elif vartyp in ['nobs', 'NOBSHDR']: 
           Ninterv = 9

           OMP = nombre
           ABSO = max(np.abs(nombre))
           vmin = -ABSO if min(nombre) < 0 else floor(min(nombre) / 100) * 100
           vmax = ABSO if min(nombre) < 0 else ceil(max(nombre) / 100) * 100
           cmap = cm.get_cmap('viridis_r', lut=Ninterv)
           Alpha = 0.5
           if vmin == vmax:
               vmin, vmax = -1.0, 1.0
       
       elif vartyp == 'obs':
           Ninterv = 9
           cmap = cm.get_cmap('RdYlBu_r', lut=Ninterv)
           SSIG = np.std(OMP)
           ABSO = 4.0 * SSIG
           Median = median(OMP)
           vmin, vmax = Median - ABSO, Median + ABSO
           if mode == 'SIGMA':
               vmin, vmax = floor(min(OMP)), ceil(max(OMP))
           if abs(vmin - vmax) < .01:
               vmin, vmax = -.5, .5
       
       elif vartyp in ['omp', 'oma', 'bcorr' ]:
           STRING1 = '$%.0f\sigma$'
           Ninterv = 9

           ABSO = max(np.abs(OMP))
           vmin, vmax = -ABSO, ABSO
           cmap = cm.get_cmap('seismic', lut=Ninterv)
           if mode == 'MOYENNE':
               SSIG = np.std(OMP)
             #  ABSO = 4.0 * SSIG
               Median = 0 #median(OMP) 
               vmin, vmax = Median - ABSO, Median + ABSO
               if abs(vmin - vmax) < .01:
                   vmin, vmax = -.5, .5
                   OMP = [0.0] * len(OMP)
           if mode == 'SIGMA':
               vmin, vmax = min(OMP), max(OMP)
               cmap = cm.get_cmap('RdYlBu_r', lut=Ninterv)
       
       # Adjust if vmin and vmax are too close
       if abs(vmin - vmax) < .01 and vartyp != 'dens':
           vmin, vmax = -.5, .5
       # Normalize and create color map
       norm = cm.colors.Normalize(vmin=vmin, vmax=vmax)
       y = np.linspace(vmin, vmax, Ninterv + 1)
       m = cm.ScalarMappable(norm=norm, cmap=cmap)
       Colors = [m.to_rgba(x) for x in y]
       hexv = [colors.rgb2hex(c) for c in Colors]
       inds = np.digitize(OMP, y)
       
       # Plotting setup
       nombres = 0
       left, bottom = 0.92, 0.15
       ax, fig, LATPOS, PROJ, pc = pikobs.type_projection(Proj)
       ONMAP = 0
       POINTS = 'OFF'
       patch_list = []
       
       # Loop through data points and plot
       for i in range(len(nombre)):
           x1, y1 = PROJ.transform_point(lon[i], lat[i], pc)
           point = PROJ.transform_point(lon[i], lat[i], src_crs=pc)
           fig_coords = ax.transData.transform(point)
           ax_coords = ax.transAxes.inverted().transform(fig_coords)
           xx, yy = ax_coords
           mask = (xx >= -0.01) & (xx <= 1.01) & (yy >= -0.01) & (yy <= 1.01)
           if mask:
               ONMAP += nombre[i]
               if POINTS == 'ON':
                   plt.text(point[0], point[1], int(floor(nombre[i])), color="k", fontsize=17, zorder=5, ha='center', va='center', weight='bold')
               else:
                   points4 = projectPpoly(PROJ, lat[i], lon[i], deltax, deltay, pc)
                   col = Colors[inds[i] - 1]
                   poly = plt.Polygon(points4, fc=col, zorder=4, ec='k', lw=0.2, alpha=1.0)
                   ax.add_patch(poly)
       
       # Add map features
       ax.coastlines()
       ax.add_feature(cartopy.feature.LAND, zorder=1, edgecolor='#C0C0C0', facecolor='#C0C0C0')
       ax.add_feature(cartopy.feature.OCEAN, zorder=0, edgecolor='#7f7f7f', facecolor='#00bce3')
       ax.add_feature(cartopy.feature.BORDERS)
       
       # Add gridlines
       gl = ax.gridlines(color='b', linestyle=(0, (1, 1)), xlocs=range(-180, 190, 10), ylocs=LATPOS, draw_labels=False, zorder=7)
       
       # Add colorbar
       ax3 = fig.add_axes([left, bottom, .02, 0.70])
       y = [round(yi, 6) for yi in y]
       cb2 = cbar.ColorbarBase(ax3, cmap=cmap, norm=norm, orientation='vertical', drawedges=True, extend='neither', ticks=y, boundaries=y, alpha=Alpha)
       
       # Add text and labels
       ax.text(0.00, 1.05, namesin[0], fontsize=11, color='b', transform=ax.transAxes)
 
       if len(filesin)>1:

           ax.text(0.00 + 0.07, 1.05, " VS ", fontsize=11, color='k', transform=ax.transAxes)
           ax.text(0.00 + 0.1, 1.05, namesin[1], fontsize=11, color='r', transform=ax.transAxes)
       
       ax.text(0.00 + 20, 1.05, vartyp, fontsize=11, color='k', transform=ax.transAxes)
       ax.text(0.00, 1.02, PERIODE, fontsize=11, color='#3366FF', transform=ax.transAxes)
       ax.text(0.45, 1.05, Nomvar, fontsize=11, color='k', transform=ax.transAxes, fontweight='bold')
       
       props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
       if vartyp in ['dens', 'nobs']:
           textstr =  'Nobs=%.2i'%(ONMAP)
       else:
           textstr = '$\mu=%.6f\sigma=%.6f$\nNobs=%.2i'%(Mu, Sigma, ONMAP)
       ax.text(0.85, 1.08, textstr, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=props)
       
       # Save the plot
       plt.grid(True)
       plt.savefig(f'{pathwork}/scatter_plot/{fonction}_{id_stn}_{int(vcoord)}.png', format='png')
       plt.close(fig)
