import os, sys, glob
import numpy as np
import ujson as json

import xarray as xr
from netCDF4 import Dataset as nc

cp = 1004.    # Heat capacity at constant pressure for dry air [J kg^-1 K^-1]
Rv = 461.      # Gas constant of water vapor [J kg^-1 K^-1]
Rd = 287.      # Gas constant of dry air [J kg^-1 K^-1]
p_0 = 100000.
lam = Rv/Rd - 1.

def T_v(T, qv, qn, qp):
    return T*(1. + lam*qv - qn - qp)

def theta(p, T): return T*(p_0/p)**(Rd/cp)

def theta_v(p, T, qv, qn, qp):
    return theta(p, T_v(T, qv, qn, qp))

def generate_tracking(time, file):
    with xr.open_dataset(file) as f:
        try:
            f = f.squeeze('time')
        except:
            pass
        print(f)

        print("\t Calculating velocity fields...")
        w_field = f['W'][:]
        w_field = (w_field + np.roll(w_field, 1, axis=0)) / 2

        u_field = f['U'][:]
        u_field = (u_field + np.roll(u_field, 1, axis=1)) / 2

        v_field = f['V'][:]
        v_field = (v_field + np.roll(v_field, 1, axis=2)) / 2

        print("\t Calculating buoynacy fields...")
        qn_field = f['QN'][:] / 1e3
        thetav_field = theta_v(f['p'][:]*100, f['TABS'][:], 
                               f['QV'][:] / 1e3, qn_field, 0)
        buoy_field = (thetav_field > 
                      np.mean(thetav_field, axis=(1,2)))

        print("\t Calculating tracer fields...")
        tr_field = np.array(f['TR01'][:])
        tr_mean = np.mean(tr_field.reshape((len(f.z), len(f.y)*len(f.x))), axis=1)
        tr_stdev = np.sqrt(tr_field.reshape((len(f.z), len(f.y)*len(f.x))).var(1))
        tr_min = .05 * np.cumsum(tr_stdev)/(np.arange(len(tr_stdev))+1)

        #---- Dataset for storage 
        print("\t Saving DataArrays...")
        ds = xr.Dataset(coords= {'z': f.z, 'y':f.y, 'x':f.x})

        mask = (qn_field > 1e-4) | (w_field > 0.)
        ds['u'] = u_field.where(mask)
        ds['v'] = v_field.where(mask)
        ds['w'] = w_field.where(mask)
    
        ds['core'] = (w_field > 0.) & (buoy_field > 0.) & (qn_field > 1e-4)
        ds['condensed'] = (qn_field > 1e-4)
        ds['plume'] = xr.DataArray(tr_field > 
                np.max(np.array([tr_mean + tr_stdev, tr_min]), 0)[:, None, None], 
                dims=['z', 'y', 'x'])

        # Flag for netCDF compression (very effective for large, sparse arrays)
        encoding = {}
        if True:
            encoding = {var: dict(zlib=True) for var in ds.data_vars}
        ds.to_netcdf('data/cloudtracker_input_%08g.nc' % time, encoding=encoding)

def main():
    global model_config
    with open('model_config.json', 'r') as json_file:
        model_config = json.load(json_file)
        nt = model_config['config']['nt']

    filelist = sorted(glob.glob('%s/*.nc' % model_config['variables']))
    for time in range(nt):
        print('\t Working...%s/%s                        ' % (time, nt), end='\r')
        generate_tracking(time, filelist[time])

if __name__ == "__main__":
    main()
