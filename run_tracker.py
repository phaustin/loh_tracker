import sys, json

from cloudtracker import main as tracker_main
    
def run_tracker(input):
    print( " Running the cloud-tracking algorithm... " )
    print( " Input dir: \"" + input + "\" \n" )

    # Read .json configuration file
    with open('model_config.json', 'r') as json_file:
        config = json.load(json_file)

    tracker_main.main(input, config)

    print( "\n Entrainment analysis completed " )

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_tracker("./data/")
    elif len(sys.argv) == 2:
        run_tracker(sys.argv[1])
    else:
        print( " Invalid input " ) 
    