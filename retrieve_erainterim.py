import sys
import string
from datetime import datetime, timedelta
from ecmwfapi import ECMWFDataServer
    
server = ECMWFDataServer()

strArea = sys.argv[1] #"-7/-79/-11/-75"
date = sys.argv[2] #["2010-02-15/to/2010-02-18"]
outfile = sys.argv[3]

# add one day before and one day after requested period to reanalysis data
# first: split the string at /
# date usually (must) be in format: %Y-%m-%d/to/%Y-%m-%d
date_array	= date.split("/")
date_start	= datetime.strptime(date_array[0],"%Y-%m-%d")
date_end	= datetime.strptime(date_array[2],"%Y-%m-%d")

date_start_new 	= date_start
date_end_new	= date_end + timedelta(days=1)

date_start_string 	= str(date_start_new.year)+"-"+str(date_start_new.month).zfill(2)+"-"+str(date_start_new.day).zfill(2)
date_end_string 	= str(date_end_new.year)+"-"+str(date_end_new.month).zfill(2)+"-"+str(date_end_new.day).zfill(2)
date_string = date_start_string+"/to/"+date_end_string


print(sys.argv[0]+" started...")
print(sys.argv[0]+": region "+strArea)
print(sys.argv[0]+": dates  "+date_string)

#for date in strDates:

# liquid cloud water and ice water: "246.128/247.128"
# specific rain water content 75.128
# specific snow water content 76.128

server.retrieve({
      'class'     : "ei",
      'dataset'   : "interim",
      'date'      : date_string,
      'expver'    : "1",
      'grid'      : "0.75/0.75",
      'levelist'  : "all",
      'levtype'   : "ml",
      'param'     : "75.128/76.128/129.128/130.128/131.128/132.128/133.128/135.128/155.128/52.162/156.128/246.128/247.128",
      'step'      : "0",
      'stream'    : "oper",
      'target'    : "CHANGEME",
      'time'      : "00/06/12/18",
      'type'      : "an",
      'area'      : strArea,
      'format'    : "netcdf",
      'target'    : outfile+"_atm.nc"
})

server.retrieve({
      'class'     : "ei",
      'dataset'   : "interim",
      'date'      : date_string,
      'expver'    : "1",
      'grid'      : "0.75/0.75",
      'levtype'   : "sfc",
      'param'     : "134.128",
      'stream'    : "oper",
      'step'      : "0",
      'time'      : "00:00:00/06:00:00/12:00:00/18:00:00",
      'area'      : strArea,
      'format'    : "netcdf",
	  'target'	  : outfile+'_sfc.nc'
})

# old request for surface variables:
'''
      'class'     : "ei",
      'dataset'   : "interim",
      'date'      : date,
      'expver'    : "1",
      'grid'      : "0.75/0.75",
      'levtype'   : "sfc",
      #'param'     : "50.128/142.128/134.128/143.128/165.128/166.128/167.128/186.128/187.128/188.128/228.128",  
      'param'	  : "50.128/142.128/143.128/228.128",
      'stream'    : "oper",
      'step'      : "3/6/9/12", #"0"
      'time'      : "00:00:00/12:00:00", #"00:00:00/06:00:00/12:00:00/18:00:00",
      'area'      : strArea,
      'format'    : "netcdf",
      'target'    : outfile+"_sfc.nc"
'''



print(sys.argv[0]+" finished")
