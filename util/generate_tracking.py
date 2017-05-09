import os, sys, glob
import numpy as np

from netCDF4 import Dataset

cp = 1004.    # Heat capacity at constant pressure for dry air [J kg^-1 K^-1]
cpv = 1870.    # Heat capacity at constant pressure of water vapor [J kg^-1 K^-1]
Cl = 4190.     # Heat capacity of liquid water [J kg^-1 K^-1]
Rv = 461.      # Gas constant of water vapor [J kg^-1 K^-1]
Rd = 287.      # Gas constant of dry air [J kg^-1 K^-1]
Lv = 2.5104e6 # Latent heat of vaporization [J kg^-1]
Lf = 0.3336e6  # Latent heat of fusion [J kg^-1]
Ls = 2.8440e6  # Latent heat of sublimation [J kg^-1]
g = 9.81       # Accelleration of gravity [m s^-2]
p_0 = 100000.
epsilon = Rd/Rv
lam = Rv/Rd - 1.
lam = 0.61

def memory_usage():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def T_v(T, qv, qn, qp):
    return T*(1. + lam*qv - qn - qp)

def theta(p, T): return T*(p_0/p)**(Rd/cp)

def theta_v(p, T, qv, qn, qp):
    return theta(p, T_v(T, qv, qn, qp))

def generate_tracking(file_name):
    print(file_name)

    time_step = filelist.index(file_name)
    vars = {'core', 'condensed', 'plume', 'u', 'v', 'w'}
    
    nc_file = Dataset(file_name)

    save_file = Dataset('data/cloudtracker_input_%08g.nc' % time_step, 'w')

    x = nc_file['x'][:]
    y = nc_file['y'][:]
    z = nc_file['z'][:]

    save_file.createDimension('x', len(x))
    save_file.createDimension('y', len(y))
    save_file.createDimension('z', len(z))

    x_var = save_file.createVariable('x', 'f', ('x',))
    x_var[:] = x[:]
    y_var = save_file.createVariable('y', 'f', ('y',))
    y_var[:] = y[:]
    z_var = save_file.createVariable('z', 'f', ('z',))
    z_var[:] = z[:]

    variables = {}
    for var_name in vars:
        if (var_name == {'core', 'condensed', 'plume'}):
            variables[var_name] = save_file.createVariable(var_name, 'i', ('z', 'y', 'x'), zlib = True)
        else:
            variables[var_name] = save_file.createVariable(var_name, 'f', ('z', 'y', 'x'), zlib = True)

    print("\t Open files for writing,", memory_usage())
    print("\t Calculating velocities...")

    temp_field = nc_file['U'][:, :, :].astype(np.float)
    temp_field[:, :-1, :] += temp_field[:, 1:, :]
    temp_field[:, -1, :] += temp_field[:, 0, :]
    variables['u'][:] = temp_field/2.

    temp_field = nc_file['V'][:, :, :].astype(np.float)
    temp_field[:, :, :-1] += temp_field[:, :, 1:]
    temp_field[:, :, -1] += temp_field[:, :, 0]
    variables['v'][:] = temp_field/2.

    #    print "Load w"
    temp_field = nc_file['W'][:, :, :].astype(np.float)
    temp_field[:-1, :, :] += temp_field[1:, :, :]
    temp_field[:-1, :, :] = temp_field[:-1, :, :]/2.
    variables['w'][:] = temp_field

    qn_field = nc_file['QN'][:, :, :].astype(np.float)/1000.
    thetav_field = theta_v((nc_file['p'][:].astype(np.float)*100.)[:, np.newaxis, np.newaxis],
                               nc_file['TABS'][:, :, :].astype(np.float), \
                               nc_file['QV'][:, :, :].astype(np.float)/1000., \
                               qn_field, nc_file['QP'][:, :, :].astype(np.float)/1000.)
    print("\tLoad thermodynamic fields", memory_usage())
                     
    buoy_field = (thetav_field > 
         (thetav_field.mean(2).mean(1))[:, np.newaxis, np.newaxis])
    print("\tBuoyancy field,", memory_usage())

    variables['core'][:] = (temp_field > 1.) & buoy_field & (qn_field > 1.e-4)
    variables['condensed'][:] = (qn_field > 1.e-4)
    print("\tSave core/condensed region", memory_usage())

    # Tracer fields
    tr_field = nc_file['TR01'][0, :].astype(double)
    tr_mean = tr_field.reshape((len(z), len(y)*len(x))).mean(1)
    tr_stdev = np.sqrt(tr_field.reshape((len(z), len(y)*len(x))).var(1))
    tr_min = .05 * np.cumsum(tr_stdev)/(np.arange(len(tr_stdev))+1)
    
    variables['plume'][:] = (tr_field > np.max(np.array([tr_mean + tr_stdev, tr_min]), 0)[:, None, None])

    save_file.close()
    nc_file.close()

def main():
    global model_config
    with open('config.json', 'r') as json_file:
        model_config = json.load(json_file)

    filelist = sorted(glob.glob('%s/*.nc' % model_config['variables']))
    for time_step, file_name in enumerate(filelist):
      print("time_step: " + str(time_step))
      main(file_name)

if __name__ == "__main__":
    main()
