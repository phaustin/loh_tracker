import sys
import lib.model_param as mc

from cloudtracker import main
    
def run_tracker(input_dir):
    model_config = mc.model_config
    
    print( " Running the cloud-tracking algorithm... " )
    print( " Input dir: \"" + input_dir + "\" \n" )
    
    main.main(input_dir)

    print( "\n Entrainment analysis completed " )

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_tracker("./data/tracking2")
    elif len(sys.argv) == 2:
        run_tracker(sys.argv[1])
    else:
        print( " Invalid input " ) 
    