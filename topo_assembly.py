import sys
import os 

from netCDF4 	     import Dataset
from numpy   	     import arange
from def_fields_icar import *
from utilities       import *

# settings for topography assemble
sealevelzero = True    # if elevations smaller then zero occur, these are set to zero


# names of the ETOPO1 Bedrock variables
strHRelev         = 'Band1'
strHRlat          = 'lat'
strHRlon          = 'lon'

workingdir = os.getcwd()
inputfileterrain = sys.argv[1]
outputfileterrain = sys.argv[2]

print "-----------------------------------------------------------------------------------------------------"
print "*working directory: "+workingdir
print ""
print "*terrain files: "
print " input     "+inputfileterrain
print " output    "+outputfileterrain
print ""
inp = Dataset(workingdir+"/"+inputfileterrain,'r')
out = Dataset(workingdir+"/"+outputfileterrain,'w',format='NETCDF4')

print "working on terrain data...",
lat_var  = inp.variables[strHRlat]
lon_var  = inp.variables[strHRlon]
elev_var = inp.variables[strHRelev]

lat  = lat_var[:]
lon  = lon_var[:]
elev = elev_var[:]

timedummy = [0]

nTimeInput = len(timedummy) 
nLatInput  = len(inp.dimensions[strHRlat])
nLonInput  = len(inp.dimensions[strHRlon])

out.createDimension(ICARFIELDS.dimtime ,None)
out.createDimension(ICARFIELDS.dimlon  ,nLonInput)
out.createDimension(ICARFIELDS.dimlat  ,nLatInput)
out.createDimension(ICARFIELDS.dimlonu ,nLonInput+1)
out.createDimension(ICARFIELDS.dimlatu, nLatInput)
out.createDimension(ICARFIELDS.dimlonv, nLonInput)
out.createDimension(ICARFIELDS.dimlatv, nLatInput+1)

time_out = out.createVariable(ICARFIELDS.vartime, ICARFIELDS.typtime, (ICARFIELDS.dimtime,))
lon_out  = out.createVariable(ICARFIELDS.varlon, ICARFIELDS.typlon,   (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
lat_out  = out.createVariable(ICARFIELDS.varlat, ICARFIELDS.typlat,   (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))

lon_outu = out.createVariable(ICARFIELDS.varlonu, ICARFIELDS.typlonu,   (ICARFIELDS.dimtime, ICARFIELDS.dimlatu, ICARFIELDS.dimlonu,))
lat_outu = out.createVariable(ICARFIELDS.varlatu, ICARFIELDS.typlatu,   (ICARFIELDS.dimtime, ICARFIELDS.dimlatu, ICARFIELDS.dimlonu,))

lon_outv = out.createVariable(ICARFIELDS.varlonv, ICARFIELDS.typlonv,   (ICARFIELDS.dimtime, ICARFIELDS.dimlatv, ICARFIELDS.dimlonv,))
lat_outv = out.createVariable(ICARFIELDS.varlatv, ICARFIELDS.typlatv,   (ICARFIELDS.dimtime, ICARFIELDS.dimlatv, ICARFIELDS.dimlonv,))

elev_out   = out.createVariable(ICARFIELDS.varhgt, ICARFIELDS.typhgt,   (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
lmask_out  = out.createVariable(ICARFIELDS.varlandmask, ICARFIELDS.typlandmask,   (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
vegfra_out = out.createVariable(ICARFIELDS.varvegfra, ICARFIELDS.typvegfra, (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
ivgtyp_out = out.createVariable(ICARFIELDS.varivgtyp, ICARFIELDS.typivgtyp, (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
isltyp_out = out.createVariable(ICARFIELDS.varisltyp, ICARFIELDS.typisltyp, (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))

smois_out  = out.createVariable(ICARFIELDS.varsmois, ICARFIELDS.typsmois, (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))
tslb_out   = out.createVariable(ICARFIELDS.vartslb,  ICARFIELDS.typtslb,  (ICARFIELDS.dimtime, ICARFIELDS.dimlat, ICARFIELDS.dimlon,))


lon_out.units  = 'degrees_north'
lat_out.units  = 'degrees_south'
elev_out.units = 'm'

# prepare the output data arrays
lat_output_data = prepare_array(nLatInput,nLonInput)
lon_output_data = prepare_array(nLatInput,nLonInput)

# fill the output data arrays
#for n in range(len(lat)):
#  lon_output_data[n,:] = lon
# this statement is equivalent to the two lines above
lon_output_data[:,:] = lon

for k in range(len(lat)):
  for n in range(len(lon)):
    lat_output_data[k,n] = lat[k] 

# fill netCDF variables with the data arrays
time_out[:] = timedummy

# fill xlongu, xlatu, xlongv and xlatv
dlon = lon[1]-lon[0]
dlat = lat[1]-lat[0]

lon0 = lon[0] - dlon/2
lat0 = lat[0] - dlat/2

for time in range(len(timedummy)):
  for n in range(nLonInput+1):
    lon_outu[time,:,n]=lon0 + n * dlon
    for k in range(nLatInput):
      lat_outu[time,k,n] = lat[k]

  for k in range(len(lat)+1):
    lon_outv[time,k,:] = lon
    for n in range(len(lon)):
      lat_outv[time,k,n] = lat0 + k*dlat


for time in range(len(timedummy)):
  lon_out[time,::] = lon_output_data
  lat_out[time,::] = lat_output_data
  
  if sealevelzero:
    for k in range(len(lat)):
      for l in range(len(lon)):
        if elev[k,l] < 0:
           elev_out[time,k,l] = 0
           lmask_out[time,k,l] = 2
        else:
           elev_out[time,k,l] = elev[k,l]
           lmask_out[time,k,l] = 1
  else:
    elev_out[time,::] = elev
    lmask_out[time,::] = 1     

print lon_outu
print lon_outu[:]

inp.close()
out.close()

print "[done]"
