import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

# Multiprocessing modules
import multiprocessing as mp
from multiprocessing import Pool
PROC = 1

import model_param as mc
import cloudtracker.main

# Default working directory for ent_analysis package
cwd = os.getcwd()

# Output profile names
profiles = {'condensed', 'condensed_env', 'condensed_edge', \
	'condensed_shell' , 'core', 'core_env', 'core_edge', 'core_shell', \
	'plume', 'condensed_entrain', 'core_entrain', 'surface'}

def wrapper(module_name, script_name, function_name, filelist):
	pkg = __import__ (module_name, globals(), locals(), ['*'])
	md = getattr(pkg, script_name)
	fn = getattr(md, function_name)
	
	pool = mp.Pool(PROC)
	pool.map(fn, filelist)
	
def run_cloudtracker():
	# Change the working directory for cloudtracker
	#os.chdir('%s/cloudtracker/' % (cwd))
	model_config = mc.model_config
	
	# Swap input directory for cloudtracker 
	cloudtracker.main.main(model_config) 

if __name__ == '__main__':
	run_cloudtracker()
	
	print("Entrainment analysis completed")
	
