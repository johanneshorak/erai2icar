import sys
from ecmwfapi import ECMWFDataServer
    
server = ECMWFDataServer()

strArea = sys.argv[1] #"-7/-79/-11/-75"
date = sys.argv[2] #["2010-02-15/2010-02-18"]
outfile = sys.argv[3]

print sys.argv[0]+" started..."
print sys.argv[0]+": region "+strArea
print sys.argv[0]+": dates  "+date

#for date in strDates:
server.retrieve({
      'class'     : "ei",
      'dataset'   : "interim",
      'date'      : date,
      'expver'    : "1",
      'grid'      : "0.75/0.75",
      'levelist'  : "all",
      'levtype'   : "ml",
      'param'     : "129.128/130.128/131.128/132.128/133.128/52.162/156.128",
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
      'date'      : date,
      'expver'    : "1",
      'grid'      : "0.75/0.75",
      'levtype'   : "sfc",
      'param'     : "134.128",
      'stream'    : "oper",
      'step'      : "0",
      'time'      : "00:00:00/06:00:00/12:00:00/18:00:00",
      'area'      : strArea,
      'format'    : "netcdf",
      'target'    : outfile+"_sfc.nc"
})


print sys.argv[0]+" finished"
