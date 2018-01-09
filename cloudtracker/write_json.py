"""

example:
python -m cloudtracker.util.write_json BOMEX

"""
import json
import pprint
import argparse


def make_parser():
    linebreaks = argparse.RawTextHelpFormatter
    descrip = __doc__.ljust(80)
    parser = argparse.ArgumentParser(formatter_class=linebreaks,
                                     description=descrip)
    parser.add_argument('casename', type=str, help='')
    return parser

def main(args=None):
    """
    args: optional -- if missing then args will be taken from command line
          or pass casename
    """
    parser = make_parser()
    args = parser.parse_args(args)
    case_name=args.casename

    json_dict = {}

    if case_name == 'BOMEX':
        #---- BOMEX 
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'BOMEX_256x256x128_25m_25m_1s_stat.nc'
        location = '/newtera/loh/data/BOMEX'

        json_dict['case_name'] = case_name
        json_dict['location'] = location

        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nx'] = 256
        json_dict['config']['ny'] = 256
        json_dict['config']['nz'] = 128
        json_dict['config']['nt'] = 180

        json_dict['config']['dx'] = 25
        json_dict['config']['dy'] = 25
        json_dict['config']['dz'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = -8.
        json_dict['config']['vg'] = 0.

    elif case_name == 'CGILS_CTL':
        #---- CGILS_CTL
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'ENT_CGILS_CTL_S6_3D_384x384x194_25m_1s_stat.nc'
        location = '/newtera/loh/data/CGILS_CTL'

        json_dict['case_name'] = case_name
        json_dict['location'] = location
        
        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nt'] = 360
        json_dict['config']['nx'] = 384
        json_dict['config']['ny'] = 384
        json_dict['config']['nz'] = 194

        json_dict['config']['dx'] = 25
        json_dict['config']['dy'] = 25
        json_dict['config']['dz'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 0.
        json_dict['config']['vg'] = 0.

    elif case_name == 'CGILS_300K':
        #---- CGILS_300K
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_300K_384x384x194_25m_1s_stat.nc'
        location = '/newtera/loh/data/CGILS_300K'

        json_dict['case_name'] = case_name
        json_dict['location'] = location
        
        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nt'] = 360
        json_dict['config']['nx'] = 384
        json_dict['config']['ny'] = 384
        json_dict['config']['nz'] = 194

        json_dict['config']['dx'] = 25
        json_dict['config']['dy'] = 25
        json_dict['config']['dz'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 0.
        json_dict['config']['vg'] = 0.

    elif case_name == 'CGILS_301K':
        #---- CGILS_301K
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_301K_384x384x194_25m_1s_stat.nc'
        location = '/newtera/loh/data/CGILS_301K'

        json_dict['case_name'] = case_name
        json_dict['location'] = location
        
        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nt'] = 360
        json_dict['config']['nx'] = 384
        json_dict['config']['ny'] = 384
        json_dict['config']['nz'] = 194

        json_dict['config']['dx'] = 25
        json_dict['config']['dy'] = 25
        json_dict['config']['dz'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 0.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GCSSARM':
        #---- GCSSARM
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'GCSSARM_256x256x208_25m_25m_1s_stat.nc'
        location = '/newtera/loh/data/GCSSARM'

        json_dict['case_name'] = case_name
        json_dict['location'] = location

        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nx'] = 256
        json_dict['config']['ny'] = 256
        json_dict['config']['nz'] = 128
        json_dict['config']['nt'] = 510

        json_dict['config']['dx'] = 25
        json_dict['config']['dy'] = 25
        json_dict['config']['dz'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 10.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GATE_BDL':
        #---- GATE_BDL
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'GATE_1920x1920x512_50m_1s_ent_stat.nc'
        location = '/newtera/loh/data/GATE_BDL'

        json_dict['case_name'] = case_name
        json_dict['location'] = location

        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '%s/tracking' % location
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nx'] = 1728
        json_dict['config']['ny'] = 1728
        json_dict['config']['nz'] = 80
        json_dict['config']['nt'] = 180

        json_dict['config']['dx'] = 50
        json_dict['config']['dy'] = 50
        json_dict['config']['dz'] = 50
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = -8.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GATE':
        #---- GATE
        json_dict = {}
        json_dict['config'] = {}

        stat_file = 'GATE_1920x1920x512_50m_1s_ent_stat.nc'
        location = '/newtera/loh/data/GATE'

        json_dict['case_name'] = case_name
        json_dict['location'] = location

        json_dict['condensed'] = '%s/condensed_entrain' % location
        json_dict['core'] = '%s/core_entrain' % location
        json_dict['stat_file'] = '%s/%s' % (location, stat_file)
        json_dict['tracking'] = '/tera/loh/cloudtracker/cloudtracker/hdf5'
        json_dict['variables'] = '%s/variables' % location

        # Model parameters
        json_dict['config']['nx'] = 1728
        json_dict['config']['ny'] = 1728
        json_dict['config']['nz'] = 320
        json_dict['config']['nt'] = 30

        json_dict['config']['dx'] = 50
        json_dict['config']['dy'] = 50
        json_dict['config']['dz'] = 50
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = -8.
        json_dict['config']['vg'] = 0.
    else:
        raise ValueError('Case name not found')


    with open('model_config.json','w') as f:
        json.dump(json_dict, f,indent=1)
        print('Wrote {} using util.write_json'.format('model_config.json'))
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(json_dict)
        
if __name__ == '__main__':
    main()
    
