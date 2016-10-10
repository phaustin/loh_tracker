import os, sys, glob
import numpy as np
import xray, dask, h5py, json

from netCDF4 import Dataset as nc

cp = 1004.    # Heat capacity at constant pressure for dry air [J kg^-1 K^-1]
Rv = 461.      # Gas constant of water vapor [J kg^-1 K^-1]
Rd = 287.      # Gas constant of dry air [J kg^-1 K^-1]
p_0 = 100000.
lam = Rv/Rd - 1.

model_config = {}

def T_v(T, qv, qn, qp):
    return T*(1. + lam*qv - qn - qp)

def theta(p, T): return T*(p_0/p)**(Rd/cp)

def theta_v(p, T, qv, qn, qp):
    return theta(p, T_v(T, qv, qn, qp))

def generate_tracking(time, ds):
    dn = xray.Dataset(
        {
            'u': (ds.U.dims, ds.U, ds.U.attrs),
            'v': (ds.V.dims, ds.V, ds.V.attrs),
            'w': (ds.W.dims, ds.W, ds.W.attrs),
        },
        coords=ds.coords)

    try:
        qp = ds.qp
    except:
        qp = 0
    thetav = theta_v((ds.p * 100.),
                    ds.TABS, ds.QV / 1e3, 
                    ds.QN / 1e3, qp / 1e3)
    buoy = thetav > np.mean(thetav, axis=(2, 3))

    dn['core'] = (ds.W.dims, buoy & (ds.W > 0.) & (ds.QN > 0.))
    dn['condensed'] = (ds.W.dims, (ds.QN > 0.))
    dn['plume'] = (ds.W.dims, (ds.W > 0.))

    dest = 'data'
    dn.to_netcdf('%s/cloudtracker_input_%08g.nc' % (dest, time))

    # time, datasets = zip(*dn.groupby('time'))
    # # dest = model_config['location'] + '/tracking_input'
    # dest = 'data'
    # paths = ['%s/cloudtracker_input_%08g.nc' % (dest, t) \
    #                         for t in np.arange(len(time))]
    # xray.save_mfdataset(datasets, paths)


def main():
    global model_config
    with open('config.json', 'r') as json_file:
        model_config = json.load(json_file)

    filelist = sorted(glob.glob('%s/*.nc' % model_config['variables']))
    with xray.open_mfdataset(filelist, concat_dim="time") as ds:
        print(ds)

        for time in range(len(ds.time)):
            generate_tracking(time, ds.isel(time=time))

if __name__ == "__main__":
    main()
