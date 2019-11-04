import xarray as xa
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import lib.gpcalc as gpcalc
import sys as sys

if len(sys.argv) < 4:
    print(' syntax: python erai2icar.py [atm_file] [sfc_file] [outname]')
    sys.exit(1)
    
atm_nc = sys.argv[1]
sfc_nc = sys.argv[2]
outname = sys.argv[3]

try:
    atm_ds = xa.open_dataset('{:s}'.format(atm_nc))
except:
    print(' error opening {:s}!'.format(atm_nc))
    sys.exit(1)

try:
    sfc_ds = xa.open_dataset('{:s}'.format(sfc_nc))
except:
    print(' error opening {:s}!'.format(sfc_nc))
    sys.exit(1)
        
try:
    ml_df  = pd.read_csv('./data/model_level_erai.csv',index_col='n')
except:
    print(' error opening model level data!')
    sys.exit(1)


# test whether surface and atmospheric dataset coordinates match

if False in (sfc_ds.time == atm_ds.time).values:
    print(' time dimension not matching')
    
if False in (sfc_ds.longitude == atm_ds.longitude).values:
    print(' longitude not matching')
    
if False in (sfc_ds.latitude == atm_ds.latitude).values:
    print(' latitude not matching')


# this seems necessary since for ERAI I queried geopotential
# in _atm dataset. For the surface it's only defined at level 1.
if 'z' in atm_ds.data_vars:
    atm_ds['z'] = atm_ds.z.sel(level=1)

# merge both datasets into one
erai_ds = atm_ds.merge(sfc_ds)


gpcalc.set_data(erai_ds,ml_df,60)    # set the data required for geopotential calculations

# -
# create a dataset that contains the ak and bk coefficients of ERAI
# later needed to calculate pressure at each model level from surface pressure
# -
ab_ds = xa.Dataset(
    coords={
        'level'        : erai_ds.level
    },
    data_vars={
        'ak'     : (['level'],ml_df.loc[erai_ds.level.values,'a [Pa]'].values),
        'bk'     : (['level'],ml_df.loc[erai_ds.level.values,'b'].values),        
    }
)
erai_ds = erai_ds.merge(ab_ds)

Nt   = len(erai_ds.time)
Nlon = len(erai_ds.longitude)
Nlat = len(erai_ds.latitude)
Nlvl = len(erai_ds.level)

# first - calculate the pressure and geopotential (height) at every model level
# set pressure at level 0 (= top of the atmosphere) to nan. this shouldn't be a full level anymore
# and therefor we can't assign a pressure to it.

p           = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)  # pressure
ph          = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)  # geopotential height

print(' calculating pressure and geopotential at model levels...')

# loop thorough all vertical levels of the data and calculate geopotential height of each grid cell there
for n in range(0,Nlvl):
    lvl  = erai_ds.level.values[n]
    ak1  = ml_df.loc[lvl,'a [Pa]']  # coef. for half level above (lower pressure)
    bk1  = ml_df.loc[lvl,'b']
    
    #if n == gpcalc.lvlmax:
    ak0  = ml_df.loc[lvl+1,'a [Pa]']    # coef. for half level below (higher pressure)
    bk0  = ml_df.loc[lvl+1,'b']
    #else:
    #    ak0  = ml_df.loc[lvl,'a [Pa]']    # coef. for half level below (higher pressure)
    #    bk0  = ml_df.loc[lvl,'b']

    
    ps  = erai_ds.sp[:].values

    ph[:,n] = gpcalc.get_phi(lvl)/9.81   # get_phi calculates geopotential at full model level
    
    if lvl == 0:
        p[:,n] = ps*np.nan
    else:
        p[:,n] = 0.5*((ak0+bk0*ps)+(ak1+bk1*ps))

    print('  {:4n} {:4n} | {:10.4f} {:10.4f} | {:10.4f} {:10.4f} | {:10.1f}'.format(n,lvl,ak0,bk0,ak1,bk1,p[0,n-1,0,0]))

print(p.shape)
print(Nlvl)

erai_ds['p'] = (['time','level','latitude','longitude'],p)
erai_ds['ph'] = (['time','level','latitude','longitude'],ph)


# prepare the data arrays
west_east   = np.array(list(range(0,Nlon)))
south_north = np.array(list(range(0,Nlat)))
bottom_top  = (gpcalc.lvlmax-erai_ds.level.values)[::-1]                    # reverse order, 60 is lowest level in ERAI, for ICAR it should be 0

xlong       = np.zeros(Nt*Nlon*Nlat).reshape(Nt,Nlat,Nlon)
xlat        = np.zeros(Nt*Nlon*Nlat).reshape(Nt,Nlat,Nlon)
Time        = erai_ds.time.values

HGT         = np.zeros(Nt*Nlon*Nlat).reshape(Nt,Nlat,Nlon)             # elevation at surface
PH          = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # geopotential height
U           = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)
V           = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)
QVAPOR      = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)
QCLOUD      = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)
QICE        = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)

PHB         = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # not used
PB          = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # not used
TSK         = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # not used
TH          = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # potential temperature

# set values
U          = erai_ds.u[:,::-1,::-1,:].values
V          = erai_ds.v[:,::-1,::-1,:].values
P          = erai_ds.p[:,::-1,::-1,:].values
QVAPOR     = erai_ds.q[:,::-1,::-1,:].values/(1.0-erai_ds.q[:,::-1,::-1,:].values)
QCLOUD     = erai_ds.clwc[:,::-1,::-1,:].values/(1.0-erai_ds.clwc[:,::-1,::-1,:].values)
QICE       = erai_ds.ciwc[:,::-1,::-1,:].values/(1.0-erai_ds.ciwc[:,::-1,::-1,:].values)
PH         = erai_ds.ph[:,::-1,::-1,:].values
HGT        = erai_ds.z[:,::-1,:].values/9.81
TH         = erai_ds.t[:,::-1,::-1,:].values*((10.**5)/P)**(0.2854)

#print(p[:,:,::-1,:][0,:,0,0])
#print(erai_ds.p[:,:,::-1,:].values[0,:,0,0])
#print(erai_ds.p[:,::-1,::-1,:].values[0,:,0,0])

xlong[:,:] = erai_ds.longitude

for ny in range(Nlat):
    xlat[:,ny,:] = erai_ds.latitude[::-1].values[ny]
    
frc_ds = xa.Dataset(
    coords={
        'Time'        : Time,
        'bottom_top'  : bottom_top,
        'west_east'   : west_east,
        'south_north' : south_north
    },
    data_vars={
        'XLONG'    : (['Time','south_north','west_east'],xlong),
        'XLAT'     : (['Time','south_north','west_east'],xlat),
        
        'HGT'      : (['Time','south_north','west_east'],HGT),
        
        'U'        : (['Time','bottom_top','south_north','west_east'],U),
        'V'        : (['Time','bottom_top','south_north','west_east'],V),

        'TH'       : (['Time','bottom_top','south_north','west_east'],TH),   
        
        'P'        : (['Time','bottom_top','south_north','west_east'],P),
        'PB'        : (['Time','bottom_top','south_north','west_east'],PB),
        
        'PH'       : (['Time','bottom_top','south_north','west_east'],PH),
        'PHB'      : (['Time','bottom_top','south_north','west_east'],PHB),
        
        'QVAPOR'   : (['Time','bottom_top','south_north','west_east'],QVAPOR),
        'QCLOUD'   : (['Time','bottom_top','south_north','west_east'],QCLOUD),
        'QICE'     : (['Time','bottom_top','south_north','west_east'],QICE),
        
        'TSK'      : (['Time','bottom_top','south_north','west_east'],TSK),
    }
)

# copy the attributes of variables that have a correspondence in the erai dataset

varmap=[
    ['u','U'],
    ['v','V'],
    ['q','QVAPOR'],
    ['clwc','QCLOUD'],
    ['ciwc','QICE']
]

frc_ds['P'].attrs['units']         = 'Pa'
frc_ds['P'].attrs['long_name']     = 'pressure'
frc_ds['P'].attrs['standard_name'] = 'pressure'

frc_ds['HGT'].attrs['units']         = 'm'
frc_ds['HGT'].attrs['long_name']     = 'geopotential height of orography surface'
frc_ds['HGT'].attrs['standard_name'] = 'surface_geopotential_height'

frc_ds['PH'].attrs['units']         = 'm'
frc_ds['PH'].attrs['long_name']     = 'geopotential height of grid cell'
frc_ds['PH'].attrs['standard_name'] = 'geopotential_height'

frc_ds['TH'].attrs['units']         = 'K'
frc_ds['TH'].attrs['long_name']     = 'potential temperature'
frc_ds['TH'].attrs['standard_name'] = 'potential_temperature'

frc_ds['TSK'].attrs['units']         = ''
frc_ds['TSK'].attrs['long_name']     = 'unused variable'
frc_ds['TSK'].attrs['standard_name'] = ''

frc_ds['PB'].attrs['units']         = ''
frc_ds['PB'].attrs['long_name']     = 'unused variable'
frc_ds['PB'].attrs['standard_name'] = ''

frc_ds['PHB'].attrs['units']         = ''
frc_ds['PHB'].attrs['long_name']     = 'unused variable'
frc_ds['PHB'].attrs['standard_name'] = ''

frc_ds['Time'].encoding['units']         = 'hours since 1900-01-01 00:00:0.0'
frc_ds['Time'].encoding['dtype']         = 'f4'
frc_ds['Time'].encoding['calendar']      = 'gregorian'

for n in range(len(varmap)):
    row = varmap[n]
    eravar  = row[0]
    frcvar  = row[1]
    for key in erai_ds[eravar].attrs:
        val = erai_ds[eravar].attrs[key]
        frc_ds[frcvar].attrs[key] = val
        
        
frc_ds.to_netcdf('{:s}'.format(outname))
