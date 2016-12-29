import sys, json, pprint

def main(case_name):
    json_dict = {}

    if case_name == 'BOMEX':
        #---- BOMEX 
        json_dict = {}
        json_dict['config'] = {}

        json_dict['case_name'] = case_name
        json_dict['location'] = '/newtera/loh/data/BOMEX'

        stat_file = 'BOMEX_256x256x128_25m_25m_1s_stat.nc'

        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nx'] = 256
        json_dict['config']['ny'] = 256
        json_dict['config']['nz'] = 128
        json_dict['config']['nt'] = 180

        json_dict['config']['dx'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = -8.
        json_dict['config']['vg'] = 0.

    elif case_name == 'CGILS_300K':
        #---- CGILS_300K
        json_dict = {}
        json_dict['config'] = {}

        json_dict['case_name'] = case_name
        json_dict['location'] = '/newtera/loh/data/CGILS_300K'

        stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_300K_384x384x194_25m_1s_stat.nc'
        
        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nt'] = 360
        json_dict['config']['nx'] = 384
        json_dict['config']['ny'] = 384
        json_dict['config']['nz'] = 194

        json_dict['config']['dx'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 0.
        json_dict['config']['vg'] = 0.

    elif case_name == 'CGILS_301K':
        #---- CGILS_301K
        json_dict = {}
        json_dict['config'] = {}

        json_dict['case_name'] = case_name
        json_dict['location'] = '/newtera/loh/data/CGILS_301K'

        stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_301K_384x384x194_25m_1s_stat.nc'
        
        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nt'] = 360
        json_dict['config']['nx'] = 384
        json_dict['config']['ny'] = 384
        json_dict['config']['nz'] = 194

        json_dict['config']['dx'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 0.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GCSSARM':
        #---- GCSSARM
        json_dict = {}
        json_dict['config'] = {}

        json_dict['case_name'] = case_name
        json_dict['location'] = '/newtera/loh/data/GCSSARM'

        stat_file = 'GCSSARM_256x256x208_25m_25m_1s_stat.nc'

        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nx'] = 256
        json_dict['config']['ny'] = 256
        json_dict['config']['nz'] = 128
        json_dict['config']['nt'] = 510

        json_dict['config']['dx'] = 25
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = 10.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GATE_BDL':
        #---- GATE_BDL
        json_dict = {}
        json_dict['config'] = {}

        json_dict['case_name'] = case_name
        json_dict['location'] = '/newtera/loh/data/GATE_BDL'

        stat_file = 'GATE_1920x1920x512_50m_1s_ent_stat.nc'

        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nx'] = 1728
        json_dict['config']['ny'] = 1728
        json_dict['config']['nz'] = 80
        json_dict['config']['nt'] = 180

        json_dict['config']['dx'] = 50
        json_dict['config']['dt'] = 60

        json_dict['config']['ug'] = -8.
        json_dict['config']['vg'] = 0.

    elif case_name == 'GATE':
        #---- GATE
        json_dict = {}
        json_dict['config'] = {}

        json_dict['location'] = '/newtera/loh/data/GATE'

        stat_file = 'GATE_1920x1920x512_50m_1s_ent_stat.nc'

        json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
        json_dict['core'] = '%s/core_entrain' % json_dict['location']
        json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
        json_dict['tracking'] = '/tera/loh/cloudtracker/cloudtracker/hdf5'
        # json_dict['tracking'] = '%s/tracking' % json_dict['location']
        json_dict['variables'] = '%s/variables' % json_dict['location']

        # Model parameters
        json_dict['config']['nx'] = 1728
        json_dict['config']['ny'] = 1728
        json_dict['config']['nz'] = 320
        json_dict['config']['nt'] = 30

        json_dict['config']['dx'] = 50
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
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        print("Missing parameter")
        print("For example, run python write_json.py BOMEX \n")
        raise ValueError('Case name is not given')
