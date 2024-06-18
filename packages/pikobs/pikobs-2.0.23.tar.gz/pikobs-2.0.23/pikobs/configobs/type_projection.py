import cartopy.crs as ccrs
import pylab as plt

def type_projection(Proj):   
   pc = ccrs.PlateCarree()
   if Proj=='cyl':
    PROJ = ccrs.PlateCarree()
    fig = plt.figure(figsize=(14,7))
    ax = plt.axes(projection=PROJ)
   
    ax.set_extent([-180, 180, -90, 90], crs=PROJ)
    LATPOS=[-90,-60,-30,00,30,60,90]
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   elif Proj=='OrthoN':
    PROJ= ccrs.Orthographic(central_latitude=90.0, central_longitude=-80.0)
    fig = plt.figure(figsize=(14,14))
    ax = plt.axes(projection=PROJ)
   
    ax.set_global()
    ax.coastlines(resolution='110m')
   
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   elif Proj=='OrthoS':
    PROJ= ccrs.Orthographic(central_latitude=-90.0, central_longitude=-80.0)
    fig = plt.figure(figsize=(14,14))
    ax = plt.axes(projection=PROJ)
   
    ax.set_global()
    ax.coastlines(resolution='110m')
   
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
    #=================================================================================
   elif Proj=='robinson':
    PROJ = ccrs.Robinson()
    fig = plt.figure(figsize=(14,7))
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-180, 180, -90, 90], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
    ax.coastlines(resolution='110m')
   
   elif Proj=='Europe':
    PROJ=ccrs.NorthPolarStereo( central_longitude=-105.0)
    fig = plt.figure(figsize=[13, 13])
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-50,  53, 42, 90], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   
   
   elif Proj=='Canada':
    PROJ=ccrs.NorthPolarStereo( central_longitude=-105.0)
    fig = plt.figure(figsize=[13, 7])
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-150,  -53, 42, 90], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   
   elif Proj=='AmeriqueNord':
    PROJ=ccrs.NorthPolarStereo( central_longitude=-105.0)
    fig = plt.figure(figsize=[13, 7])
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-140,  -40, 20, 90], pc )
    ax.set_extent([-170,  -40, 20, 90], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   
   elif Proj=='Npolar':
    PROJ=ccrs.NorthPolarStereo( central_longitude=-90.5)
    fig = plt.figure(figsize=[14, 14])
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-180, 180, 00, 90], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
    ax.coastlines(resolution='110m')
   elif Proj=='Spolar':
    PROJ=ccrs.SouthPolarStereo( central_longitude=-86)
    fig = plt.figure(figsize=[14, 14])
    ax = plt.subplot(1, 1, 1, projection=PROJ)
   
    ax.set_extent([-180, 180, -90, 00], pc )
    LATPOS=[-90,-80,-60,-50,-40,-30,00,30,40,50,60,80,90]
    LATPOS=range(-90, 91, 10)
   elif Proj == 'reg':
     Size_mapx=10
     Size_mapy=10
     pole_latitude=31.758
     pole_longitude=178.008 -90.
     llcrnrlat = -7.74911
     llcrnrlon = -128.80635
     urcrnrlat = 57.88194
     urcrnrlon =39.378404
     central_rotated_longitude=-90. -1.991605
     PROJ = ccrs.RotatedPole(pole_longitude=pole_longitude ,  pole_latitude=pole_latitude,
                          central_rotated_longitude=central_rotated_longitude)
     fig=plt.figure(1,figsize=( Size_mapx,Size_mapy))
     ax = fig.add_subplot(1, 1, 1, projection=PROJ)
   
     mapExtent=[llcrnrlon , urcrnrlon,llcrnrlat,urcrnrlat]
     ax.set_extent(mapExtent)
     xs, ys, zs = PROJ.transform_points(pc,
                                    np.array([llcrnrlon, urcrnrlon]),
                                    np.array([llcrnrlat, urcrnrlat])).T
    # print (  ' Xlims=', xs )
   #  print (  ' Ylims=', ys )
   
     ax.set_xlim(xs)
     ax.set_ylim(ys)
     LATPOS=[-60,-30,00,10.,20.,30.,40.,50.,60.,70.,80.,90.]
   return ax, fig, LATPOS, PROJ, pc
 #  print (  ' HEURE5 Nombre=', datetime.datetime.now().time() )
