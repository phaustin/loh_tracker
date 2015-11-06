import sys
import lib.model_param as mc

from cloudtracker import main
    
def run_tracker(input_dir):
    model_config = mc.model_config

    model_config['input_directory'] = input_dir
    main.main(model_config)

    print("Entrainment analysis completed")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print( " Running: " + sys.argv[0] )
        print( " Input dir: " + "./data/tracking2" )
        run_tracker("./data/tracking2")
    elif len(sys.argv) == 2:
        print( " Running: " + sys.argv[0] )
        print( " Input dir: " + sys.argv[1] )
        run_tracker(sys.argv[1])
    else:
        print(" Invalid input ") 
    