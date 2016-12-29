import sys, json

from cloudtracker.main import main
from cloudtracker.load_config import config 
from cloudtracker.load_config import c
    
def run_tracker():
    print( " Running the cloud-tracking algorithm... " )

    # Print out model parameters from config.json
    print( " \n Model parameters: " )
    print( " \t Case name: {}".format(config.case_name) )
    print( " \t Model Domain {}x{}x{}".format(c.nx, c.ny, c.nz) )
    print( " \t {} model time steps \n".format(c.nt) )

    main()

    print( "\n Entrainment analysis completed " )

if __name__ == '__main__':
    run_tracker()
    