#!/usr/bin/env python
#Runtime (690,130,128,128): ?

import pickle

import networkx

import numpy as np
import glob, h5py, dask, code

full_output=False

def full_output(cloud_times, cloud_graphs, merges, splits, MC):
    cloud_times = tuple(cloud_times)

    pickle.dump(cloud_times, open('pkl/cloud_times.pkl','wb'))

    n = 0
    clouds = {}
    for subgraph in cloud_graphs:
        events = {'has_condensed': False, 'has_core': False}
        for node in subgraph:
            node_events = []
            t = int(node[:8])
            if t == 0: node_events.append('break_start')
            if t == (MC['nt']-1): node_events.append('break_end')

            if node in merges:
                node_events.append('merge_end')
            if node in splits:
                node_events.append('split')
                
            info = subgraph.node[node]
            if info['merge']:
                node_events.append('merge')
            if info['split']:
                node_events.append('split_start')
                
            events['has_condensed'] = (info['condensed'] > 0) or events['has_condensed']
            events['has_core'] = (info['core'] > 0) or events['has_core']

            if t in events:
                events[t].extend(node_events)
            else:
                events[t] = node_events[:]

        clouds[n] = events
        n = n + 1

    pickle.dump(clouds, open('pkl/graph_events.pkl', 'wb'))

    


#---------------------

def make_graph():
    graph = networkx.Graph()

    merges = {}
    splits = {}

    for t in range(len(glob.glob('cloudtracker/hdf5/clusters_*.h5'))):
        with h5py.File('cloudtracker/hdf5/clusters_%08g.h5' % t, 'r') as f:
            keys = list(f['clusters'].keys())
            keys.sort()
            for id in keys:
                m_conns = set(f['%s/merge_connections' % id])
                s_conns = set(f['%s/split_connections' % id])
                core = len(f['%s/core' % id])
                condensed = len(f['%s/condensed' % id])
                plume = len(f['%s/plume' % id])
                attr_dict = {'merge': m_conns,
                             'split': s_conns,
                             'core': core,
                             'condensed': condensed,
                             'plume': plume}
                             
                for item in m_conns:
                    node1 = '%08g|%08g' % (t, int(id))
                    node2 = '%08g|%08g' % (t-1, int(item))
                    merges[node2] = node1
                for item in s_conns:
                    node1 = '%08g|%08g' % (t, int(id))
                    node2 = '%08g|%08g' % (t, int(item))
                    splits[node2] = node1            
            
                # Construct a graph of the cloudlet connections
                graph.add_node('%08g|%08g' % (t, int(id)), attr_dict = attr_dict)
                if f['%s/past_connections' % id]:
                    for item in f['%s/past_connections' % id]:
                        graph.add_edge('%08g|%08g' % (t-1, int(item)),
                                       '%08g|%08g' % (t, int(id)))

    # Iterate over every cloud in the graph
    for subgraph in networkx.connected_component_subgraphs(graph):
        # Find the duration over which the cloud_graph has cloudy points.
        times = set()
        for node in subgraph:
            if subgraph.node[node]['condensed'] > 0:
                times.add(int(node[:8]))

        # If cloud exists for less than 5 minutes, check if it has split events
        # If it has split events, remove them and reconnect the cloud
        if len(times) < 5:
            for node in subgraph:
                if subgraph.node[node]['split']:
                    item = subgraph.node[node]['split'].pop()
                    t = int(node[:8]) 
                    graph.add_edge(node, '%08g|%08g' % (t, int(item)))

    for subgraph in networkx.connected_component_subgraphs(graph):
        # Find the duration over which the cloud_graph has cloudy points.
        times = set()
        for node in subgraph:
            if subgraph.node[node]['condensed'] > 0:
                times.add(int(node[:8]))

        # If a cloud exists less than 5 minutes, check for merge events
        if len(times) < 5:
            for node in subgraph:
                if subgraph.node[node]['merge']:
                    item = subgraph.node[node]['merge'].pop()
                    t = int(node[:8])
                    graph.add_edge(node, '%08g|%08g' % (t-1, int(item)))


    cloud_times = []
    
    cloud_graphs = []
    cloud_noise = []
    for subgraph in networkx.connected_component_subgraphs(graph):
        # If a cloud exists less than 2 minutes, classify it as noise
        # Otherwise, put it in cloud_graphs
        condensed_time = set()
        core_time = set()
        condensed_volume = 0
        core_volume = 0
        for node in subgraph.nodes():
            condensed_vol = subgraph.node[node]['condensed'] 
            if condensed_vol > 0:
                condensed_volume = condensed_volume + condensed_vol
                time = int(node[:8])
                condensed_time.add(time)

            core_vol = subgraph.node[node]['core'] 
            if core_vol > 0:
                core_volume = core_volume + core_vol
                time = int(node[:8])
                core_time.add(time)

        if (len(condensed_time) < 2) or (len(core_time) == 0):
            cloud_noise.append(subgraph)
        else:
            cloud_graphs.append((condensed_volume, subgraph))
            times = list(times)
            times.sort()
            cloud_times.append(tuple(times))
            
    cloud_graphs.sort(key=lambda key:keys[0])
    cloud_graphs.reverse()
    cloud_graphs = [item[1] for item in cloud_graphs]
    
    #if full_output: full_output(cloud_times, cloud_graphs, merges, splits, MC)

    return cloud_graphs, cloud_noise
