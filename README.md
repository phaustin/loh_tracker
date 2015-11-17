[Cloud-tracker](https://github.com/lorenghoh/cloud-tracker "cloud-tracker")
==============

# Updated cloud-tracking algorithm for SAM #
To run the cloud-tracking algorithm, use 

    python run_tracker.py [Input_dir]

where [Input_dir] is the address of the input directory with the tracking data.

## Current Status ##

### Main ###
- [x] Make run_tracker.py run with command arg
- [ ] Get rid of config.cfg 
- [ ] Read model parameters from xray dataset

### Generate cloudlets ###
- [ ] Implement/benchmark asyncio operations on ~ 30,000 cloudlet computations
- [ ] Numba/Cython for the expansion algorithm (cloudtracker.utility_functions)
- [ ] Wrap up with dask -> HDF5 output

### Cluster cloudlets ###

### Output cloud data ###

## Profiling ##
To profile the cloud-tracking algorithm using line_profiler, do
	
	python -O -B -m kernprof -l -v run_tracker.py > line_stats.txt

or, to run with a memory profiler instead,	

	python -O -B -m memory_profiler run_tracker.py > memory_stats.txt
