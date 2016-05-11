import os
from netCDF4   import Dataset
from numpy     import arange
from numpy     import flipud
from bunch     import Bunch
from utilities import * 

R=8.3144621 # J/mol/K
cp=29.19 # J/mol/K   =1.012 J/g/K
g=9.81 # m/s^2


def write(data,outfile,ifld): 
   ""
   
   out = Dataset(outfile,'w',format='NETCDF4')

   ntim = len(data.time)
   nlon = len(data.lon)
   nlat = len(data.lat)
   nlvl = len(data.lvl)

   out.createDimension(ifld.dimtime, None)
   out.createDimension(ifld.dimlvl,  nlvl)
   out.createDimension(ifld.dimlat,  nlat)
   out.createDimension(ifld.dimlon,  nlon)
   # out.createDimension(ifld.varlatu, nlat)

   otime  = out.createVariable(ifld.vartime,  ifld.typtime,  (ifld.dimtime,))
   olon   = out.createVariable(ifld.varlon,   ifld.typlon,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   olat   = out.createVariable(ifld.varlat,   ifld.typlat,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))

   # olonu  = out.createVariable(ifld.varlonu,   ifld.typlon,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   # olatu  = out.createVariable(ifld.varlatu,   ifld.typlat,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   # olonv  = out.createVariable(ifld.varlonv,   ifld.typlon,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   # olatv  = out.createVariable(ifld.varlatv,   ifld.typlat,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))

   ou     = out.createVariable(ifld.varu,     ifld.typu,     (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   ov     = out.createVariable(ifld.varv,     ifld.typv,     (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   #osmois = out.createVariable(ifld.varsmois, ifld.typsmois, (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   ogphp  = out.createVariable(ifld.vargphp,  ifld.typgphp,  (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   opt    = out.createVariable(ifld.varpt,    ifld.typpt,    (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   opb    = out.createVariable(ifld.varpb,    ifld.typpb,    (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   opp    = out.createVariable(ifld.varpp,    ifld.typpp,    (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))

   ohgt   = out.createVariable(ifld.varhgt,   ifld.typhgt,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ogphb  = out.createVariable(ifld.vargphb,  ifld.typgphb,  (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))

   oqvapor= out.createVariable(ifld.varqvapor,ifld.typqvapor,(ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   oqcloud= out.createVariable(ifld.varqcloud,ifld.typqcloud,(ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   oqice  = out.createVariable(ifld.varqice,  ifld.typqice, (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   qtsk   = out.createVariable(ifld.vartsk,   ifld.typtsk, (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))

   otime[:]    = data.time

   #londata = arange(nlat*nlon)*0.0
   #londata.shape = (nlat,nlon)

   londata = prepare_array(nlat,nlon)
   latdata = prepare_array(nlat,nlon)
   udata   = prepare_array(ntim,nlat,nlon)
   vdata   = prepare_array(ntim,nlat,nlon)

   londata[:,:] = data.lon

   for k in range(nlat):
     for n in range(nlon):
       latdata[nlat-k-1,n] = data.lat[k]
   
   for n in range(ntim):
     olon[n,::] = londata 
     olat[n,::] = latdata
     # olonu[n,::] = londata
     # olatu[n,::] = latdata
     ohgt[n,::] = flipud(data.z[n,0,::]/g)

     for k in range(nlvl):
       ou[n,nlvl-k-1,::]     = flipud(data.u[n,k,::])
       ov[n,nlvl-k-1,::]     = flipud(data.v[n,k,::])
       oqvapor[n,nlvl-k-1,::]= flipud(data.q[n,k,::])
       ogphp[n,nlvl-k-1,::]  = flipud(data.hgt[n,k,::])
       ogphb[n,nlvl-k-1,::]  = 0
       opt[n,nlvl-k-1,::]    = flipud(data.tpot[n,k,::])
       opp[n,nlvl-k-1,::]    = flipud(data.p[n,k,::])
       
   out.close()
   
   return
