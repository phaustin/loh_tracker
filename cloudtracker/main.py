#!/usr/bin/env python

import sys, os

from .generate_cloudlets import generate_cloudlets
from .cluster_cloudlets import cluster_cloudlets
from .make_graph import make_graph
from .output_cloud_data import output_cloud_data

global MC

def main(input, config, save_all=True):
    sys.setrecursionlimit(1000000)

    if not os.path.exists('cloudtracker/hdf5'):
        os.mkdir('cloudtracker/hdf5')

    # Model configuration dict
    MC = config

#----cloudlets----

    print( " Gathering cloudlets... " )

    generate_cloudlets(input)

#----cluster----
    print( "\n Creating clusters... " )

    cluster_cloudlets()

#----graph----

    print( "\n Make graph... " )
    
    cloud_graphs, cloud_noise = make_graph()
    
    print( "\tFound %d clouds" % len(cloud_graphs))
    
    # if save_all:
    #     FIXME: Object dtype dtype('object') has no native HDF5 equivalent
    #     with h5py.File('hdf5/graph_data.h5', 'w') as f:
    #         dset = f.create_dataset('cloud_graphs', data=cloud_graphs)
    #         dset = f.create_dataset('cloud_noise', data=cloud_noise)
    #     #cPickle.dump((cloud_graphs, cloud_noise), open('pkl/graph_data.pkl', 'wb'))
            
#----output----
    
    for n in range(510):
        print("\n Outputting cloud data, time step: %d" % n)
        output_cloud_data(cloud_graphs, cloud_noise)
            
