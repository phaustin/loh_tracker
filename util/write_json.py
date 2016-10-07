import json


def main():
    json_dict = {}

    #---- BOMEX 
    # json_dict['case_name'] = 'BOMEX'
    # json_dict['config'] = {}

    # stat_file = 'BOMEX_256x256x128_25m_25m_1s_stat.nc'

    # json_dict['location'] = '/newtera/loh/data/BOMEX'

    # json_dict['condensed'] = '%s/condensed_entrain' % json_dict['location']
    # json_dict['core'] = '%s/core_entrain' % json_dict['location']
    # json_dict['stat_file'] = '%s/%s' % (json_dict['location'], stat_file)
    # json_dict['tracking'] = '%s/tracking' % json_dict['location']
    # json_dict['variables'] = '%s/variables' % json_dict['location']

    # # Model parameters
    # json_dict['config']['nx'] = 256
    # json_dict['config']['ny'] = 256
    # json_dict['config']['nz'] = 128
    # json_dict['config']['nt'] = 180

    # json_dict['config']['dx'] = 25
    # json_dict['config']['dt'] = 60

    # json_dict['config']['ug'] = -8.
    # json_dict['config']['vg'] = 0.


    #---- CGILS_300K
    # json_dict['CGILS_300K'] = OrderedDict()
    # json_dict['CGILS_300K']['config'] = OrderedDict()

    # json_dict['CGILS_300K']['location'] = '/newtera/loh/data/CGILS_300K'

    # stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_300K_384x384x194_25m_1s_stat.nc'
    
    # json_dict['CGILS_300K']['condensed'] = '%s/condensed_entrain' % json_dict['CGILS_300K']['location']
    # json_dict['CGILS_300K']['core'] = '%s/core_entrain' % json_dict['CGILS_300K']['location']
    # json_dict['CGILS_300K']['stat_file'] = '%s/%s' % (json_dict['CGILS_300K']['location'], stat_file)
    # json_dict['CGILS_300K']['tracking'] = '%s/tracking' % json_dict['CGILS_300K']['location']
    # json_dict['CGILS_300K']['variables'] = '%s/variables' % json_dict['CGILS_300K']['location']

    # # Model parameters
    # json_dict['CGILS_300K']['config']['nt'] = 360
    # json_dict['CGILS_300K']['config']['nx'] = 384
    # json_dict['CGILS_300K']['config']['ny'] = 384
    # json_dict['CGILS_300K']['config']['nz'] = 194

    # json_dict['CGILS_300K']['config']['dx'] = 25
    # json_dict['CGILS_300K']['config']['dt'] = 60

    # json_dict['CGILS_300K']['config']['ug'] = 0.
    # json_dict['CGILS_300K']['config']['vg'] = 0.


    #---- CGILS_301K
    # json_dict['CGILS_301K'] = OrderedDict()
    # json_dict['CGILS_301K']['config'] = OrderedDict()

    # json_dict['CGILS_301K']['location'] = '/newtera/loh/data/CGILS_301K'

    # stat_file = 'ENT_CGILS_S6_IDEAL_3D_SST_301K_384x384x194_25m_1s_stat.nc'
    
    # json_dict['CGILS_301K']['condensed'] = '%s/condensed_entrain' % json_dict['CGILS_301K']['location']
    # json_dict['CGILS_301K']['core'] = '%s/core_entrain' % json_dict['CGILS_301K']['location']
    # json_dict['CGILS_301K']['stat_file'] = '%s/%s' % (json_dict['CGILS_301K']['location'], stat_file)
    # json_dict['CGILS_301K']['tracking'] = '%s/tracking' % json_dict['CGILS_301K']['location']
    # json_dict['CGILS_301K']['variables'] = '%s/variables' % json_dict['CGILS_301K']['location']

    # # Model parameters
    # json_dict['CGILS_301K']['config']['nt'] = 360
    # json_dict['CGILS_301K']['config']['nx'] = 384
    # json_dict['CGILS_301K']['config']['ny'] = 384
    # json_dict['CGILS_301K']['config']['nz'] = 194

    # json_dict['CGILS_301K']['config']['dx'] = 25
    # json_dict['CGILS_301K']['config']['dt'] = 60

    # json_dict['CGILS_301K']['config']['ug'] = 0.
    # json_dict['CGILS_301K']['config']['vg'] = 0.


    #---- GCSSARM
    # json_dict['GCSSARM'] = OrderedDict()
    # json_dict['GCSSARM']['config'] = OrderedDict()

    # json_dict['GCSSARM']['location'] = '/newtera/loh/data/GCSSARM'

    # stat_file = 'GCSSARM_256x256x208_25m_25m_1s_stat.nc'

    # json_dict['GCSSARM']['condensed'] = '%s/condensed_entrain' % json_dict['GCSSARM']['location']
    # json_dict['GCSSARM']['core'] = '%s/core_entrain' % json_dict['GCSSARM']['location']
    # json_dict['GCSSARM']['stat_file'] = '%s/%s' % (json_dict['GCSSARM']['location'], stat_file)
    # json_dict['GCSSARM']['tracking'] = '%s/tracking' % json_dict['GCSSARM']['location']
    # json_dict['GCSSARM']['variables'] = '%s/variables' % json_dict['GCSSARM']['location']

    # # Model parameters
    # json_dict['GCSSARM']['config']['nx'] = 256
    # json_dict['GCSSARM']['config']['ny'] = 256
    # json_dict['GCSSARM']['config']['nz'] = 128
    # json_dict['GCSSARM']['config']['nt'] = 510

    # json_dict['GCSSARM']['config']['dx'] = 25
    # json_dict['GCSSARM']['config']['dt'] = 60

    # json_dict['GCSSARM']['config']['ug'] = 10.
    # json_dict['GCSSARM']['config']['vg'] = 0.


    #---- GATE
    json_dict['case_name'] = 'GATE'
    json_dict['config'] = {}

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
    json_dict['config']['nz'] = 320
    json_dict['config']['nt'] = 180

    json_dict['config']['dx'] = 50
    json_dict['config']['dt'] = 60

    json_dict['config']['ug'] = -8.
    json_dict['config']['vg'] = 0.

    # Output JSON configuration file 
    with open('config.json','w') as f:
        json.dump(json_dict, f,indent=1)
        print('Wrote {} using util.write_json'.format('config.json'))
        print(json_dict)

if __name__ == '__main__':
    main()