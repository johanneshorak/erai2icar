import sys
import os 
import import_erai
import export_erai

from netCDF4 	     import Dataset
from numpy   	     import arange
from bunch   	     import Bunch
from def_fields_icar import *

# names of the ERA INTERIM variables
ERAFIELDS       = Bunch()
ERAFIELDS.lvl   = 'level'
ERAFIELDS.t	= 't' 
ERAFIELDS.z	= 'z'
ERAFIELDS.u	= 'u'
ERAFIELDS.v	= 'v'
ERAFIELDS.q     = 'q'           # specific humidity
ERAFIELDS.lon  	= 'longitude'
ERAFIELDS.lat	= 'latitude'
ERAFIELDS.time	= 'time'
ERAFIELDS.sp   	= 'sp'		# surface pressure
ERAFIELDS.gh    = 'gh'          # geopotential height

workingdir = '' #os.getcwd()
scriptdir = os.path.dirname(os.path.realpath(__file__))

inputfileforcingAtm = sys.argv[1]
inputfileforcingSfc = sys.argv[2]
outputfileforcing   = sys.argv[3]

print "-----------------------------------------------------------------------------------------------------"
print "*working directory: "+workingdir
print ""
print "*forcing files: "
print " input atmosphere ... "+inputfileforcingAtm
print " input surface ...... "+inputfileforcingSfc
print " output ............. "+outputfileforcing
print ""
print "working on forcing data..."

data = Bunch()
import_erai.load(data,inputfileforcingAtm,inputfileforcingSfc,ERAFIELDS)
import_erai.convert(data)
export_erai.write(data,outputfileforcing,ICARFIELDS)
