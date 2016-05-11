import os
from netCDF4   import Dataset
from numpy     import arange
from bunch     import Bunch
from math      import log
from utilities import *

R=8.3144621 # J/mol/K
cp=29.19 # J/mol/K   =1.012 J/g/K
g=9.81 # m/s^2
M=0.02896 # kg/mol

def load(data,atmfile,sfcfile,efs):
   "this function imports atmospheric and surface data from an ERAI netCDF file"

   # data the specifies name and location of coordinate variable file (usually ERA-Interim_coordvars.nc)
   # see http://rda.ucar.edu/datasets/ds627.2/docs/Eta_coordinate/

   cvardir = os.path.dirname(os.path.realpath(__file__))+'/data'
   cvarfile = 'ERA-Interim_coordvars.nc'
   crdfile = cvardir+'/'+cvarfile

   # currently atmosphere and surface data must have the same resolution and time step   
   atm  = Dataset(atmfile,'r')
   sfc  = Dataset(sfcfile,'r')
   crd  = Dataset(crdfile,'r') # coordvars import from script dir
 
   data.lat   = atm.variables[efs.lat][:]
   data.lon   = atm.variables[efs.lon][:]
   data.time  = atm.variables[efs.time][:]
   data.lvl   = atm.variables[efs.lvl][:]
   data.q     = atm.variables[efs.q][:]
   data.u     = atm.variables[efs.u][:]
   data.v     = atm.variables[efs.v][:]
   data.z     = atm.variables[efs.z][:]  # geopotential at surface
   data.t     = atm.variables[efs.t][:]

   data.sp    = sfc.variables[efs.sp][:]

   # these variables are needed to calculate the pressure at each model level
   data.a_model_alt = crd.variables['a_model_alt'][:]
   data.b_model_alt = crd.variables['b_model_alt'][:]

   atm.close()
   sfc.close()
   crd.close()

   return


def convert(data):
   "this converts ERAI data to data useable with ICAR (eg. surface pressure to the pressure at all model levels)"
   
   nlvl  = len(data.lvl)
   ntime = len(data.time)
   nlat  = len(data.lat)
   nlon  = len(data.lon)

   dimsfc = ntime*nlat*nlon
   dimatm = ntime*nlvl*nlat*nlon

   data.p    = prepare_array(ntime,nlvl,nlat,nlon)
   data.hgt  = prepare_array(ntime,nlvl,nlat,nlon)
   data.tpot = prepare_array(ntime,nlvl,nlat,nlon)

   # calculate geopotential height of surface
   #data.hgt[:,0,::] = data.z[:,0,::]/g

   data.hgt[:,nlvl-1,::] = data.z[:,0,::]/g

   # calculate pressure and geopotential at all model levels
   for i in range(ntime):
     for j in range(nlat):
       for k in range(nlon):
         data.p[i,:,j,k]   = data.a_model_alt + data.b_model_alt * data.sp[i,j,k] 
         for l in range(nlvl-1,0,-1): # run through the model levels bottoim to top
	   Tlvl = (data.t[i,l-1,j,k] + data.t[i,l,j,k])/2
	   dz = - ( (R * Tlvl) / (M * g) ) * log( data.p[i,l-1,j,k] / data.p[i,l,j,k] )
	   data.hgt[i,l-1,j,k] = data.hgt[i,l,j,k] + dz
           #print str(Tlvl) + ' ' + str(dz)
	   #print 'lvl = '+ str(l)

   # calculate potential temperature
   pii=(100000.0/data.p)**(R/cp)
   data.tpot = data.t*pii  

   #print data.tpot[0,nlvl-1,0,0]
   #print pii[0,nlvl-1,0,0]
   #print data.t[0,nlvl-1,0,0]
 
   return