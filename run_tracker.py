import sys

# # Multiprocessing modules
# import multiprocessing as mp
# from multiprocessing import Pool
# PROC = 1

import lib.model_param as mc

from cloudtracker import main
	
def run_tracker():
	model_config = mc.model_config
	main.main(model_config) 

if __name__ == '__main__':
	run_tracker()
	
	print("Entrainment analysis completed")
	