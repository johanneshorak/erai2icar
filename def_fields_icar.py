from bunch import Bunch

# -------------------------------------------------------- #
# names of the ICAR variables                              #
#                                                          #
# the names and datatypes are basically based on the WRF   #
# preprocessor naming conventions. These are the names     #
# by which the imported quantities are exported again      #
#                                                          #
# -------------------------------------------------------- #
ICARFIELDS      = Bunch()

ICARFIELDS.dimtime = 'Time'
ICARFIELDS.dimlon  = 'west_east'
ICARFIELDS.dimlat  = 'south_north'
ICARFIELDS.dimlvl  = 'bottom_top'
ICARFIELDS.dimlonu = 'west_east u'
ICARFIELDS.dimlatu = 'south_north u'
ICARFIELDS.dimlonv = 'west_east v'
ICARFIELDS.dimlatv = 'south_north v'

ICARFIELDS.vartime = 'Times'
ICARFIELDS.typtime = 'S1'
ICARFIELDS.dsctime = 'time'

ICARFIELDS.varlon  = 'XLONG'
ICARFIELDS.typlon  = 'f4'
ICARFIELDS.dsclon  = 'longitude'

ICARFIELDS.varlat = 'XLAT'
ICARFIELDS.typlat = 'f4'
ICARFIELDS.dsclat = 'latitude'

ICARFIELDS.varlonu = 'XLONG_U'
ICARFIELDS.typlonu = 'f4'
ICARFIELDS.dsclonu = '?'

ICARFIELDS.varlatu = 'XLAT_U'
ICARFIELDS.typlatu = 'f4'
ICARFIELDS.dsclatu = '?'

ICARFIELDS.varlonv = 'XLONG_V'
ICARFIELDS.typlonv = 'f4'
ICARFIELDS.dsclonv = '?'

ICARFIELDS.varlatv = 'XLAT_V'
ICARFIELDS.typlatv = 'f4'
ICARFIELDS.dsclatv = '?'

ICARFIELDS.varu = 'U'           # x-wind component
ICARFIELDS.typu = 'f4'
ICARFIELDS.dscu = 'x-wind component'

ICARFIELDS.varv = 'V'           # y-wind component
ICARFIELDS.typv = 'f4'
ICARFIELDS.dscv = 'y-wind component'

ICARFIELDS.varqvapor = 'QVAPOR'
ICARFIELDS.typqvapor = 'f4'
ICARFIELDS.dscqvapor = 'specific humidity'

ICARFIELDS.vargphb = 'PHB'      # geopotential height base
ICARFIELDS.typgphb = 'f4'
ICARFIELDS.dscgphb = 'geopotential height (base)'

ICARFIELDS.vargphp = 'PH'       # geopotential height pertubation
ICARFIELDS.typgphp = 'f4'
ICARFIELDS.dscgphp = 'geopotential height (pertubation)'

ICARFIELDS.varpt = 'T'          # potential temperature
ICARFIELDS.typpt = 'f4'
ICARFIELDS.dscpt = 'potential temperature'

ICARFIELDS.varpb = 'PB'         # pressure base
ICARFIELDS.typpb = 'f4'
ICARFIELDS.dscpb = 'pressure (base)'

ICARFIELDS.varpp = 'P'          # pressure pertubation
ICARFIELDS.typpp = 'f4'
ICARFIELDS.dscpp = 'pressure(pertubation)'

ICARFIELDS.varhgt = 'HGT'       # elevation
ICARFIELDS.typhgt = "f4"
ICARFIELDS.dschgt = 'orographic altitude'

# These are not necessary for basic ICAR, are asked for anyways
# w. conv=0 lsm=0 pbl=0
ICARFIELDS.varlandmask = 'LANDMASK'
ICARFIELDS.typlandmask = 'f4'
ICARFIELDS.dsclandmask = 'landmask'

ICARFIELDS.varvegfra = 'VEGFRA'
ICARFIELDS.typvegfra = 'f4'
ICARFIELDS.dscvegfra = '?'

ICARFIELDS.varivgtyp = 'IVGTYP'
ICARFIELDS.typivgtyp = 'f4'
ICARFIELDS.dscivgtyp = '?'

ICARFIELDS.varisltyp = 'ISLTYP'
ICARFIELDS.typisltyp = 'f4'
ICARFIELDS.dscisltyp = '?'

ICARFIELDS.vartslb   = 'TSLB'
ICARFIELDS.typtslb   = 'f4'
ICARFIELDS.dsctslb   = '?'

ICARFIELDS.varsmois = 'SMOIS'   # soil moisture
ICARFIELDS.typsmois = 'f4'
ICARFIELDS.dscsmois = 'soil moisture'

ICARFIELDS.varqcloud = 'QCLOUD'
ICARFIELDS.typqcloud = 'f4'
ICARFIELDS.dscqcloud = '?'

ICARFIELDS.varqice   = 'QICE'
ICARFIELDS.typqice   = 'f4'
ICARFIELDS.dscqice   = '?'

ICARFIELDS.vartsk    = 'TSK'
ICARFIELDS.typtsk    = 'f4'
ICARFIELDS.dsctsk    = '?'
