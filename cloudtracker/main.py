#!/usr/bin/env python

import glob
import sys, os, gc

from .generate_cloudlets import generate_cloudlets
from .cluster_cloudlets import cluster_cloudlets
from .make_graph import make_graph
from .output_cloud_data import output_cloud_data

def main(MC, save_all=True):
    sys.setrecursionlimit(1000000)

    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('hdf5'):
        os.mkdir('hdf5')

    # TODO: command line input for data directory

#----cloudlets----
    print("gathering cloudlets")

    generate_cloudlets(MC)
    return
#----cluster----

    print("making clusters")

    cluster_cloudlets(MC)

#----graph----

    print("make graph")
    
    cloud_graphs, cloud_noise = make_graph(MC)
    
    print("\tFound %d clouds" % len(cloud_graphs))
    
    # if save_all:
    #     FIXME: Object dtype dtype('object') has no native HDF5 equivalent
    #     with h5py.File('hdf5/graph_data.h5', 'w') as f:
    #         dset = f.create_dataset('cloud_graphs', data=cloud_graphs)
    #         dset = f.create_dataset('cloud_noise', data=cloud_noise)
    #     #cPickle.dump((cloud_graphs, cloud_noise), open('pkl/graph_data.pkl', 'wb'))
            
#----output----
    
    # TODO: Parallelize file output (multiprocessing)
    for n in range(nt):
        print("output cloud data, time step: %d" % n)
        output_cloud_data(cloud_graphs, cloud_noise, n, MC)
            
