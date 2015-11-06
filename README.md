[Cloud-tracker](https://github.com/lorenghoh/cloud-tracker "cloud-tracker")
==============

### Updated cloud-tracking algorithm for SAM ###
To run the cloud-tracking algorithm, use 

    python run_tracker.py [Input_dir]

replace [Input_dir] with the address of the input directory where the tracking data files are located (relative addresses work well with the argument).

## Profiling ##
To profile the cloud-tracking algorithm using line_profiler, do
	
	python -O -B -m kernprof -l -v run_tracker.py > line_stats.txt

or, to run with a memory profiler instead,	

	python -O -B -m memory_profiler run_tracker.py > memory_stats.txt
