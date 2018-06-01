import os
from netCDF4   import Dataset
from numpy     import arange
from numpy     import flipud
from bunch     import Bunch
from utilities import * 

R=8.3144621 # J/mol/K
cp=29.19 # J/mol/K   =1.012 J/g/K
g=9.81 # m/s^2


def write(data,units,outfile,ifld): 
   ""
   
   out = Dataset(outfile,'w',format='NETCDF4')

   ntim = len(data.time)
   nlon = len(data.lon)
   nlat = len(data.lat)
   nlvl = len(data.lvl)

   nlonu = len(data.lon)+1
   nlatv = len(data.lat)+1

   out.createDimension(ifld.dimtime, None)
   out.createDimension(ifld.dimlvl,  nlvl)
   out.createDimension(ifld.dimlat,  nlat)
   out.createDimension(ifld.dimlon,  nlon)
   

   otime  		  = out.createVariable(ifld.vartime,  ifld.typtime,  (ifld.dimtime,))
   otime.units 	  = ifld.unttime
   otime.calendar = ifld.caltime
   
   olon   = out.createVariable(ifld.varlon,   ifld.typlon,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))   
   olat   = out.createVariable(ifld.varlat,   ifld.typlat,   (ifld.dimtime, ifld.dimlat, ifld.dimlon,))

   ou     = out.createVariable(ifld.varu,     ifld.typu,     (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
   ov     = out.createVariable(ifld.varv,     ifld.typv,     (ifld.dimtime, ifld.dimlvl, ifld.dimlat, ifld.dimlon,))
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

   osp		= out.createVariable(ifld.varsp, 	ifld.typsp,		(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   '''
   olspf    = out.createVariable(ifld.varlspf,	ifld.typlspf,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   olsp		= out.createVariable(ifld.varlsp,	ifld.typlsp,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ocp		= out.createVariable(ifld.varcp,	ifld.typcp,		(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ou10		= out.createVariable(ifld.varu10,	ifld.typu10,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ov10		= out.createVariable(ifld.varv10,	ifld.typv10,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ot2m		= out.createVariable(ifld.vart2m,	ifld.typt2m,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   olcc		= out.createVariable(ifld.varlcc,	ifld.typlcc,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   omcc		= out.createVariable(ifld.varmcc,	ifld.typmcc,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   ohcc		= out.createVariable(ifld.varhcc,	ifld.typhcc,	(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   otp		= out.createVariable(ifld.vartp,	ifld.typtp,		(ifld.dimtime, ifld.dimlat, ifld.dimlon,))
   '''
   
   
   olon.units	= ifld.untlon
   olat.units	= ifld.untlat
   ou.units		= ifld.untu
   ov.units		= ifld.untv
   ogphp.units	= ifld.untgphp
   opt.units	= ifld.untpt
   opb.units	= ifld.untpb
   opp.units	= ifld.untpp
   ohgt.units	= ifld.unthgt
   ogphb.units	= ifld.untgphb
   oqvapor.units = ifld.untqvapor
   oqcloud.units = ifld.untqcloud
   oqice.units	= ifld.untqice
   qtsk.units	= ifld.unttsk
   
   osp.units	= ifld.untsp
   
   '''
   olspf.units	= ifld.untlspf
   olsp.units	= ifld.untlsp
   ocp.units	= ifld.untcp
   ou10.units	= ifld.untu10
   ov10.units	= ifld.untv10
   ot2m.units	= ifld.untt2m
   olcc.units	= ifld.untlcc
   omcc.units	= ifld.untmcc
   ohcc.units	= ifld.unthcc
   otp.units	= ifld.unttp
   '''

   olon.description = ifld.dsclon
   olat.description  = ifld.dsclat
   ou.description = ifld.dscu
   ov.description = ifld.dscv
   ogphp.description = ifld.dscgphp
   opt.description = ifld.dscpt
   opb.description = ifld.dscpb
   opp.description = ifld.dscpp
   ohgt.description = ifld.dschgt
   ogphb.description = ifld.dscgphb
   oqvapor.description = ifld.dscqvapor
   oqcloud.description = ifld.dscqcloud
   oqice.description = ifld.dscqice
   qtsk.description = ifld.dsctsk
   
   osp.description	= ifld.dscsp
   '''
   olspf.description= ifld.dsclspf
   olsp.description	= ifld.dsclsp
   ocp.description	= ifld.dsccp
   ou10.description	= ifld.dscu10
   ov10.description	= ifld.dscv10
   ot2m.description	= ifld.dsct2m
   olcc.description	= ifld.dsclcc
   omcc.description	= ifld.dscmcc
   ohcc.description	= ifld.dschcc
   otp.description	= ifld.dsctp
   '''
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

     osp[n,::]		= flipud(data.sp[n,::])
     '''
     olspf[n,::]    = flipud(data.lspf[n,::])
     olsp[n,::]		= flipud(data.lsp[n,::])
     ocp[n,::]		= flipud(data.cp[n,::])
     ou10[n,::]		= flipud(data.u10[n,::])
     ov10[n,::]		= flipud(data.v10[n,::])
     ot2m[n,::]		= flipud(data.t2m[n,::])
     olcc[n,::]		= flipud(data.lcc[n,::])
     omcc[n,::]		= flipud(data.mcc[n,::])
     ohcc[n,::]		= flipud(data.hcc[n,::])
     otp[n,::]		= flipud(data.tp[n,::])
	 '''
     for k in range(nlvl):
       ou[n,nlvl-k-1,::]     = flipud(data.u[n,k,::])
       ov[n,nlvl-k-1,::]     = flipud(data.v[n,k,::])
       oqvapor[n,nlvl-k-1,::]= flipud(data.q[n,k,::])
       oqcloud[n,nlvl-k-1,::]= flipud(data.clwc[n,k,::])
       oqice[n,nlvl-k-1,::]  = flipud(data.ciwc[n,k,::])
       ogphp[n,nlvl-k-1,::]  = flipud(data.hgt[n,k,::])
       ogphb[n,nlvl-k-1,::]  = 0
       opb[n,nlvl-k-1,::]    = 0
       opt[n,nlvl-k-1,::]    = flipud(data.tpot[n,k,::])
       opp[n,nlvl-k-1,::]    = flipud(data.p[n,k,::])
       
       
       
   out.close()
   
   return
