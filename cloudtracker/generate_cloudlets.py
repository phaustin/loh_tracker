#!/usr/bin/env python
"""
This program generates a pkl file containing a list of dictionaries.
Each dictionary in the list represents a condensedlet.
The dictionaries have the structure:
{'core': array of ints of core points,
'condensed': array of ints of condensed points,
'plume': array of ints of plume points,
'u_condensed': ,
'v_condensed': ,
'w_condensed': ,
'u_plume': ,
'v_plume': ,
'w_plume': }
pkl files are saved in pkl/ subdirectory indexed by time
"""

import numpy as np
import numba

from netCDF4 import Dataset as nc
import xray, dask, h5py

from dask import distributed

from .utility_functions import index_to_zyx, expand_indexes

#-------------------

# @profile
def expand_cloudlet(cloudlet, indexes, MC):
    """Given an array of indexes composing a cloudlet and a boolean mask 
    array indicating if each model index may be expanded into (True) or 
    not (False), expand the cloudlet into the permissable indicies that 
    are find all indicies adjacent to the cloudlet.
    
    Returns an array of the indicies composing the expanded cloudlet, and 
    an array of the remaining indicies that may be expanded into.
    """

    # Expand the cloudlet indexes into their nearest neighbours
    expanded_cloudlet = np.array(expand_indexes(cloudlet, MC['nz'], MC['ny'], MC['nx']))

    # Find the mask values of the expanded indexes
    mask = indexes[expanded_cloudlet]

    # Select the expanded cloudlet indexes that may be expanded into
    new_points = expanded_cloudlet[mask]

    # Remove the indicies that have been added to the cloudlet
    indexes[new_points] = False

    return new_points, indexes

#---------------------

def expand_current_cloudlets(key, cloudlets, mask, MC):

    cloudlet_points = []
    for cloudlet in cloudlets:
        cloudlet_points.append( [cloudlet[key]] )

    cloudlet_expand_indexes = range(len(cloudlet_points))

    while cloudlet_expand_indexes:
        next_loop_cloudlet_list = []
            
        # Go through the current list of cloudlets
        for n in cloudlet_expand_indexes:
            expanded_points, mask = expand_cloudlet(cloudlet_points[n][-1], 
                                                    mask,  
                                                    MC)

            if len(expanded_points) > 0:
                cloudlet_points[n].append(expanded_points)
                next_loop_cloudlet_list.append(n)
                
        cloudlet_expand_indexes = next_loop_cloudlet_list
                
    for n, cloudlet in enumerate(cloudlet_points):
        cloudlets[n][key] = np.hstack(cloudlet)

    return cloudlets, mask

#---------------------

# @profile
def make_new_cloudlets(key, mask, MC):
    indexes = np.arange(MC['nx']*MC['ny']*MC['nz'])[mask]
    cloudlets = []

    for n in indexes:
        if mask[n]:
            mask[n] = False
            cloudlet_indexes = [np.array((n,))]
            
            # add_new_cloudlet
            done = False            
            while not done:
                new_indexes, mask = expand_cloudlet(cloudlet_indexes[-1], mask, MC)

                if len(new_indexes) > 0:
                    cloudlet_indexes.append( new_indexes )
                else:
                    # If the number of points in the cloudlet has not changed, we are done
                    done = True
        
            cloudlet = {}
            cloudlet[key] = np.hstack(cloudlet_indexes)
            cloudlets.append( cloudlet )
            
    return cloudlets

#-----------------

# TODO (LOH): Parallelize 
# @profile
def find_mean_cloudlet_velocity(cloudlets, 
                                u, v, w, 
                                MC):
    # TODO: get mean velocities directly from model values
    dx, dy, dz, dt = MC['dx'], MC['dy'], MC['dz'], MC['dt']                                
    ug, vg = MC['ug'], MC['vg']

    u, v, w = u.values, v.values, u.values
    # TODO: async operation for each cloudlet in cloudlets
    for cloudlet in cloudlets:
        if len(cloudlet['condensed']) > 0:
            K, J, I = index_to_zyx( cloudlet['condensed'], MC['nz'], MC['ny'], MC['nx'] )
            # find the mean motion of the cloudlet
            u_mean = u[K, J, I].mean()-ug
            v_mean = v[K, J, I].mean()-vg
            w_mean = w[K, J, I].mean()
        
            cloudlet['u_condensed'] = (u_mean*dt/dx)
            cloudlet['v_condensed'] = (v_mean*dt/dy)
            cloudlet['w_condensed'] = (w_mean*dt/dz)
        else:
            cloudlet['u_condensed'] = 0.
            cloudlet['v_condensed'] = 0.
            cloudlet['w_condensed'] = 0.


        K, J, I = index_to_zyx( cloudlet['plume'], MC['nz'], MC['ny'], MC['nx'] )
        # find the mean motion of the cloudlet
        u_mean = u[K, J, I].mean()-ug
        v_mean = v[K, J, I].mean()-vg
        w_mean = w[K, J, I].mean()
        
        cloudlet['u_plume'] = (u_mean*dt/dx)
        cloudlet['v_plume'] = (v_mean*dt/dy)
        cloudlet['w_plume'] = (w_mean*dt/dz)

    return cloudlets

#----------------------------

# @profile
def find_cloudlets(core, condensed, plume, u, v, w, MC): 
    # find the indexes of all the core and plume points
    core = np.ravel(core)
    condensed = np.ravel(condensed)
    plume = np.ravel(plume)

    plume[condensed] = False
    condensed[core] = False

    # Create the list that will hold the cloudlets
    cloudlets = make_new_cloudlets('core', core, MC)
                    
    for cloudlet in cloudlets:
        cloudlet['condensed'] = cloudlet['core'][:]
            
    ncore = len(cloudlets)
    print(" \t%d core cloudlets" % ncore) 

    cloudlets, condensed = expand_current_cloudlets('condensed', 
                                                    cloudlets,
                                                    condensed,
                                                    MC)

    # Add any remaining points that have not been added to cloudlets 
    # as new cloudlets.
    condensed_cloudlets = make_new_cloudlets('condensed', condensed, MC)

    for cloudlet in condensed_cloudlets:
        cloudlet['core'] = np.array([], dtype=np.int)
        cloudlets.append(cloudlet)

    for cloudlet in cloudlets:
        cloudlet['plume'] = cloudlet['condensed'][:]

    ncondensed = len(cloudlets)
    print(" \t%d condensed cloudlets" % (ncondensed-ncore))


    cloudlets, plume = expand_current_cloudlets('plume', 
                                                 cloudlets,
                                                 plume,
                                                 MC)

    # Add any remaining points that have not been added to cloudlets 
    # as new cloudlets.
    plume_cloudlets = make_new_cloudlets('plume', plume, MC)

    for cloudlet in plume_cloudlets:
        cloudlet['core'] = np.array([], dtype=np.int)
        cloudlet['condensed'] = np.array([], dtype=np.int)
        cloudlets.append(cloudlet)

    nplume = len(cloudlets)
    
    print(" \t%d plume cloudlets" % (nplume-ncondensed))

    cloudlets = find_mean_cloudlet_velocity(cloudlets, 
                                            u, v, w,
                                            MC)

    return cloudlets

def load_data(ds):
    core = ds.variables['core'][:].astype(bool)
    condensed = ds.variables['condensed'][:].astype(bool)
    plume = ds.variables['plume'][:].astype(bool)
    u = ds.variables['u'][:].astype(np.float)
    v = ds.variables['v'][:].astype(np.float)
    w = ds.variables['w'][:].astype(np.float)

    return core, condensed, plume, u, v, w

# @profile
def generate_cloudlets(MC):
    ds = xray.open_mfdataset(((MC['input_directory'] + "/*.nc")), concat_dim="time",
        chunks=1000)

    for i in range(len(ds.time)):
        core, condensed, plume, u, v, w = load_data(ds.isel(time=i))
        cloudlets = find_cloudlets(core, condensed, plume, u, v, w, MC)
        
        # # TEST: linear calls instead of for loop to speed this up?
        # with h5py.File('hdf5/cloudlets_%08g.h5' % i, "w") as f:
        #     for n in range(len(cloudlets)):
        #         grp = f.create_group(str(n))
        #         for var in cloudlet_items:
        #             if(var in ['core', 'condensed', 'plume']):
        #                 dset = grp.create_dataset(var, data=cloudlets[n][var][...])
        #             else:
        #                 deset = grp.create_dataset(var, data=cloudlets[n][var])
        break
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
