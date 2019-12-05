import xarray as xa
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import lib.gpcalc as gpcalc
import lib.atmosphere as atm
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
west_east   = list(range(0,Nlon))
south_north = list(range(0,Nlat))
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

N_arr       = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # Brunt-Väisälä frequency of forcing data grid cell
N2_arr      = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # N2_arr = N_arr**2
N2True_arr  = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # True N2 without ICAR adjustments
Nmoist      = np.zeros(Nt*Nlvl*Nlon*Nlat).reshape(Nt,Nlvl,Nlat,Nlon)   # Indicates whether moist or dry N was used in cell
#=======================================================================
#= set values in forcing
#=======================================================================
U          = erai_ds.u[:,::-1,::-1,:].values
V          = erai_ds.v[:,::-1,::-1,:].values
P          = erai_ds.p[:,::-1,::-1,:].values
QVAPOR     = erai_ds.q[:,::-1,::-1,:].values/(1.0-erai_ds.q[:,::-1,::-1,:].values)
QCLOUD     = erai_ds.clwc[:,::-1,::-1,:].values/(1.0-erai_ds.clwc[:,::-1,::-1,:].values)
QICE       = erai_ds.ciwc[:,::-1,::-1,:].values/(1.0-erai_ds.ciwc[:,::-1,::-1,:].values)
PH         = erai_ds.ph[:,::-1,::-1,:].values
HGT        = erai_ds.z[:,::-1,:].values/9.81
TH         = erai_ds.t[:,::-1,::-1,:].values*((10.**5)/P)**(0.2854)

#=======================================================================
#= calculate Brunt-Väisälä frequency
#=======================================================================
TABS = atm.t_from_tpot(tpot=TH,p=P)         # needed for calcuations

# these are some settings that tailor the N field for the use with ICAR
# e.g. ICAR enforces min/max values of N and decides, based on a threshold
# whether to calculate the moist or dry Brunt-Väisälä frequency.
N2_min = 1*10**-7      # minimum N allowed
N2_max = 6*10**-4      # maximum N allowed
moist_th = 10**-7     # threshold of when to calculate moist N

# this would have to consider snow and ice as well, but ERAI doesn't calculate those.
MRMOISTURE = QCLOUD+QICE

print('calculating brunt-vaisala frequency...')
# calculation loop
for nt in range(Nt):
    if nt%10 == 0:
        print('  timestep {:n}/{:n}'.format(nt,Nt))
        
    for nx in range(Nlon):
        for ny in range(Nlat):
            z_arr  = PH[nt,:,ny,nx]
            th_arr = TH[nt,:,ny,nx]
                    
            # decide whether to calculate dry or moist stability:
            mrmoisture_arr = MRMOISTURE[nt,:,ny,nx]
            
            N2_col  = np.zeros(Nlvl)
            N2m_col = np.zeros(Nlvl)
            
            N2_col[:-1] = atm.calc_dry_stability_squared(
                    th_top = th_arr[1:],
                    th_bot = th_arr[:-1],
                    z_top  = z_arr[1:],
                    z_bot  = z_arr[:-1]
                )
            
            if len(mrmoisture_arr[mrmoisture_arr <  moist_th] > 0):
                N2m_col[:-1] = atm.calc_moist_stability_squared(
                    t_top   = TABS[nt,1:,ny,nx],
                    t_bot   = TABS[nt,:-1,ny,nx],
                    mrv_top = QVAPOR[nt,1:,ny,nx],
                    mrv_bot = QVAPOR[nt,:-1,ny,nx],
                    mrc     = 0.5*(QCLOUD[nt,1:,ny,nx]+QCLOUD[nt,:-1,ny,nx]),
                    z_top   = z_arr[1:],
                    z_bot   = z_arr[:-1]
                )    
            
            # since we can't calculate a value for the topmost level,
            # we assign the one from the second topmost level to it
            N2_col[-1]  = N2_col[-2]
            N2m_col[-1] = N2m_col[-2]
            
            # Save the unmodified N2 values to an array. Whether moist/dry
            # N2 is chosen will depend on the moisture threshold moist_th
            # The modifications for ICAR are saved to a different array
            # further below.
            N2True_arr[nt,:,ny,nx][mrmoisture_arr <  moist_th] = N2_col[mrmoisture_arr <  moist_th]
            N2True_arr[nt,:,ny,nx][mrmoisture_arr >= moist_th] = N2m_col[mrmoisture_arr >= moist_th]
            
            # save whether moist or dry N was used in grid cell
            Nmoist[nt,:,ny,nx][mrmoisture_arr <  moist_th] = 0
            Nmoist[nt,:,ny,nx][mrmoisture_arr >= moist_th] = 1
            
            # replace N2 values < 0 or smaller then N2_min with N2_min
            N2_col[ (N2_col  < 0) | (N2_col  < N2_min)] = N2_min
            N2m_col[(N2m_col < 0) | (N2m_col < N2_min)] = N2_min
            
            # replace N2 values > N2_max with N2_max
            N2_col[ N2_col  > N2_max] = N2_max
            N2m_col[N2m_col > N2_max] = N2_max
            
            # Now save the modified for ICAR N2 to an array. SetN2 to N2 if moisture is
            # below threshold, or to N2m if moisture is above the threshold.
            N2_arr[nt,:,ny,nx][mrmoisture_arr <  moist_th] = N2_col[mrmoisture_arr <  moist_th]
            N2_arr[nt,:,ny,nx][mrmoisture_arr >= moist_th] = N2m_col[mrmoisture_arr >= moist_th]

#=======================================================================
#= Brunt-Väisälä calculations are done
#=======================================================================
logN2_out = np.log(N2_arr) # ICAR stores N as log(N**2) - so this is why we take the natural log here

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
        
        'logN2ICAR': (['Time','bottom_top','south_north','west_east'],logN2_out),
        'logN2EARI': (['Time','bottom_top','south_north','west_east'],N2True_arr),
        'Nmethod'  : (['Time','bottom_top','south_north','west_east'],Nmoist),
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

frc_ds['logN2ICAR'].attrs['units']         = 'log s**-2'
frc_ds['logN2ICAR'].attrs['long_name']     = 'natural log of the squared Brunt Vaisala frequency with modifactions for ICAR'
frc_ds['logN2ICAR'].attrs['standard_name'] = 'natural log of the squared Brunt Vaisala frequency'

frc_ds['logN2EARI'].attrs['units']         = 's**-2'
frc_ds['logN2EARI'].attrs['long_name']     = 'squared Brunt Vaisala frequency calculated from ERAI data'
frc_ds['logN2EARI'].attrs['standard_name'] = 'squared Brunt Vaisala frequency'

frc_ds['Nmethod'].attrs['units']         = '1'
frc_ds['Nmethod'].attrs['desc']          = 'dry N ... 0, moist N ... 1'
frc_ds['Nmethod'].attrs['long_name']     = 'N calculation method'
frc_ds['Nmethod'].attrs['standard_name'] = 'N calculation method'

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

frc_ds['west_east'].encoding['dtype']      = 'i4'
frc_ds['south_north'].encoding['dtype']    = 'i4'

for n in range(len(varmap)):
    row = varmap[n]
    eravar  = row[0]
    frcvar  = row[1]
    for key in erai_ds[eravar].attrs:
        val = erai_ds[eravar].attrs[key]
        frc_ds[frcvar].attrs[key] = val
        
        
frc_ds.to_netcdf('{:s}'.format(outname))
