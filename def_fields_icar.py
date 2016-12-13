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

ICARFIELDS.vartime = 'Time'
ICARFIELDS.typtime = 'f4'
ICARFIELDS.dsctime = 'time'
ICARFIELDS.unttime   = 'hours since 1900-01-01 00:00:0.0'
ICARFIELDS.caltime= 'gregorian'


ICARFIELDS.varlon  = 'XLONG'
ICARFIELDS.typlon  = 'f4'
ICARFIELDS.dsclon  = 'longitude'
ICARFIELDS.untlon  = 'degree'

ICARFIELDS.varlat = 'XLAT'
ICARFIELDS.typlat = 'f4'
ICARFIELDS.dsclat = 'latitude'
ICARFIELDS.untlat = 'degree'

ICARFIELDS.varlonu = 'XLONG_U'
ICARFIELDS.typlonu = 'f4'
ICARFIELDS.dsclonu = '?'
ICARFIELDS.untlonu = 'degree'

ICARFIELDS.varlatu = 'XLAT_U'
ICARFIELDS.typlatu = 'f4'
ICARFIELDS.dsclatu = '?'
ICARFIELDS.untlatu = 'degree'

ICARFIELDS.varlonv = 'XLONG_V'
ICARFIELDS.typlonv = 'f4'
ICARFIELDS.dsclonv = '?'
ICARFIELDS.untlonv = 'degree'

ICARFIELDS.varlatv = 'XLAT_V'
ICARFIELDS.typlatv = 'f4'
ICARFIELDS.dsclatv = '?'
ICARFIELDS.untlatv = 'degree'

ICARFIELDS.varu = 'U'           # x-wind component
ICARFIELDS.typu = 'f4'
ICARFIELDS.dscu = 'x-wind component'
ICARFIELDS.untu = 'm s**-1'

ICARFIELDS.varv = 'V'           # y-wind component
ICARFIELDS.typv = 'f4'
ICARFIELDS.dscv = 'y-wind component'
ICARFIELDS.untv = 'm s**-1'

ICARFIELDS.varqvapor = 'QVAPOR'
ICARFIELDS.typqvapor = 'f4'
ICARFIELDS.dscqvapor = 'specific humidity'
ICARFIELDS.untqvapor = '1'

ICARFIELDS.vargphb = 'PHB'      # geopotential height base
ICARFIELDS.typgphb = 'f4'
ICARFIELDS.dscgphb = 'geopotential height (base)'
ICARFIELDS.untgphb = 'm'

ICARFIELDS.vargphp = 'PH'       # geopotential height pertubation
ICARFIELDS.typgphp = 'f4'
ICARFIELDS.dscgphp = 'geopotential height (pertubation)'
ICARFIELDS.untgphp = 'm'

ICARFIELDS.varpt = 'T'          # potential temperature
ICARFIELDS.typpt = 'f4'
ICARFIELDS.dscpt = 'potential temperature'
ICARFIELDS.untpt = 'K'

ICARFIELDS.varpb = 'PB'         # pressure base
ICARFIELDS.typpb = 'f4'
ICARFIELDS.dscpb = 'pressure (base)'
ICARFIELDS.untpb = 'Pa'

ICARFIELDS.varpp = 'P'          # pressure pertubation
ICARFIELDS.typpp = 'f4'
ICARFIELDS.dscpp = 'pressure(pertubation)'
ICARFIELDS.untpp = 'Pa'

ICARFIELDS.varhgt = 'HGT'       # elevation
ICARFIELDS.typhgt = "f4"
ICARFIELDS.dschgt = 'orographic altitude'
ICARFIELDS.unthgt = 'm'

# These are not necessary for basic ICAR, are asked for anyways
# w. conv=0 lsm=0 pbl=0
ICARFIELDS.varlandmask = 'LANDMASK'
ICARFIELDS.typlandmask = 'f4'
ICARFIELDS.dsclandmask = 'landmask'
ICARFIELDS.untlandmask = '1'

ICARFIELDS.varvegfra = 'VEGFRA'
ICARFIELDS.typvegfra = 'f4'
ICARFIELDS.dscvegfra = '?'
ICARFIELDS.untvegfra = '1'

ICARFIELDS.varivgtyp = 'IVGTYP'
ICARFIELDS.typivgtyp = 'f4'
ICARFIELDS.dscivgtyp = '?'
ICARFIELDS.untivgtyp = ''

ICARFIELDS.varisltyp = 'ISLTYP'
ICARFIELDS.typisltyp = 'f4'
ICARFIELDS.dscisltyp = '?'
ICARFIELDS.untisltyp = ''

ICARFIELDS.vartslb   = 'TSLB'
ICARFIELDS.typtslb   = 'f4'
ICARFIELDS.dsctslb   = '?'
ICARFIELDS.unttslb   = ''

ICARFIELDS.varsmois = 'SMOIS'   # soil moisture
ICARFIELDS.typsmois = 'f4'
ICARFIELDS.dscsmois = 'soil moisture'
ICARFIELDS.untsmois = ''

ICARFIELDS.varqcloud = 'QCLOUD'
ICARFIELDS.typqcloud = 'f4'
ICARFIELDS.dscqcloud = '?'
ICARFIELDS.untqcloud = ''

ICARFIELDS.varqice   = 'QICE'
ICARFIELDS.typqice   = 'f4'
ICARFIELDS.dscqice   = '?'
ICARFIELDS.untqice	 = ''

ICARFIELDS.vartsk    = 'TSK'
ICARFIELDS.typtsk    = 'f4'
ICARFIELDS.dsctsk    = '?'
ICARFIELDS.unttsk	 = 's'

ICARFIELDS.varsp  = 'sp'	# surface pressure
ICARFIELDS.typsp	= 'f4'
ICARFIELDS.dscsp  = '?'
ICARFIELDS.untsp	= 'Pa'

ICARFIELDS.varlspf  = 'lspf'	# large scale precipitation fraction
ICARFIELDS.typlspf	= 'f4'
ICARFIELDS.dsclspf  = '?'
ICARFIELDS.untlspf	= '1'

ICARFIELDS.varlsp	= 'lsp'		# large scale precipitation
ICARFIELDS.typlsp	= 'f4'
ICARFIELDS.dsclsp   = '?'
ICARFIELDS.untlsp	= 's'

ICARFIELDS.varcp	= 'cp'		# convective precipitation
ICARFIELDS.typcp	= 'f4'
ICARFIELDS.dsccp    = '?'
ICARFIELDS.untcp	= 'm'

ICARFIELDS.varu10	= 'u10'		# 10 metre u wind component
ICARFIELDS.typu10	= 'f4'
ICARFIELDS.dscu10    = '?'
ICARFIELDS.untu10	= 'm s**-1'

ICARFIELDS.varv10	= 'v10'		# 10 metre v wind component
ICARFIELDS.typv10	= 'f4'
ICARFIELDS.dscv10    = '?'
ICARFIELDS.untv10 	= 'm s**-1'

ICARFIELDS.vart2m	= 't2m'		# 2 metre temperature
ICARFIELDS.typt2m	= 'f4'
ICARFIELDS.dsct2m    = '?'
ICARFIELDS.untt2m	= 'K'

ICARFIELDS.varlcc	= 'lcc'		# low cloud cover
ICARFIELDS.typlcc	= 'f4'
ICARFIELDS.dsclcc    = '?'
ICARFIELDS.untlcc	= '(0 - 1)'

ICARFIELDS.varmcc	= 'mcc'		# medium cloud cover
ICARFIELDS.typmcc	= 'f4'
ICARFIELDS.dscmcc    = '?'
ICARFIELDS.untmcc	= '(0 - 1)'

ICARFIELDS.varhcc	= 'hcc'		# high cloud cover
ICARFIELDS.typhcc	= 'f4'
ICARFIELDS.dschcc    = '?'
ICARFIELDS.unthcc	= '(0 - 1)'

ICARFIELDS.vartp	= 'tp'		# total precipitation
ICARFIELDS.typtp	= 'f4'
ICARFIELDS.dsctp    = '?'
ICARFIELDS.unttp	= 'm'
