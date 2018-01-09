
# coding: utf-8

# # Cloud-tracking algorithm
# 
# There has been some major changes to the cloud-tracking algorithm. I have now push most of the changes to the main repository (https://github.com/lorenghoh/loh_tracker), which uses HDF5 for data storage. We have since then moved to Parquet, and I will eventually modify the cloud-tracking algorithm to output Parquet files instead, but for now we will simply create HDF5 files and translate them afterwards.
# 
#  So we start with the main branch:

# In[1]:


get_ipython().run_line_magic('cd', '/tera/users/loh/repos/vlad_cloudtracker/loh_tracker/')
get_ipython().run_line_magic('ls', '')


#  Normally, we will run util/write_json.py 

# In[3]:


get_ipython().run_line_magic('run', 'util/write_json.py CGILS_301K')


#  Running util/generate_tracking.py then creates the input files for the cloud-tracking algorithm. For this notebook, I've slightly modified this script to only translate two timesteps:

# In[4]:


get_ipython().run_line_magic('run', 'util/generate_tracking.py')


#  The resulting input files for the cloudtracking is automatically written in ./data (without checking if the folder exists -- too lazy to fix that now):

# In[14]:


get_ipython().run_line_magic('ls', 'data')


#  Then we can start the actual cloud-tracking:

# In[2]:


get_ipython().run_line_magic('run', 'run_tracker.py')


#  The cloud-tracking algorithm will now output the full event histories (./data/events.json) in Python Dictionary format. It saves all the merging and splitting events for each cloud and the timesteps they occur -- it is also possible to store the cluster ids associated with these events, which I will update...later. 
#  
#  The output HDF5 files also store the cloud properties in a dictionary format. For example,

# In[2]:


get_ipython().run_line_magic('ls', 'hdf5')


# In[5]:


import h5py
f = h5py.File('hdf5/cloudlets_00000000.h5')
list(f.keys())[:15]


# In[11]:


list(f['1'])


# In[13]:


f['1/core'][...]

