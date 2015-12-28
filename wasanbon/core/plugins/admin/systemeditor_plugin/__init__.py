import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ This plugin provides APIs to edit System Profile """
    def __init__(self):
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def get_active_configuration_data(self, rtc):
        if not 'configuration_sets' in dir(rtc):
            return []
        for conf in rtc.configuration_sets:
            if conf.id == rtc.active_configuration_set:
                return conf.configuration_data

    def get_connectable_pairs(self, nameservers, verbose=False):
        pairs = []

        # For DataPorts
        outports = []
        for ns in nameservers:
            outports = outports + ns.dataports(port_type='DataOutPort', verbose=verbose)
        for outport in outports:
            inports = []
            for ns in nameservers:
                inports = inports + ns.dataports(port_type='DataInPort', 
                                                 data_type=outport.properties['dataport.data_type'],
                                                 verbose=verbose)
            for inport in inports:
                pairs.append([outport, inport])

        # For ServicePorts
        provports = []
        for ns in nameservers:
            provports = provports + ns.svcports(polarity='Provided')
        for provport in provports:
            reqports = []
            for interface in provport.interfaces:
                if interface.polarity_as_string(False) == 'Provided':
                    interface_type = interface.type_name
                    for ns in nameservers:
                        reqports = reqports + ns.svcports(polarity='Required', interface_type=interface_type)
                    for reqport in reqports:
                        pairs.append([provport, reqport])
        return pairs

    
    
    def save_to_file(self, nameservers, filepath, verbose=False, system_name='DefaultSystem',
                     version='1.0', vendor='DefaultVendor', abstract='RT System'):
        argv = ['-n', system_name, 
                '-a', abstract, 
                '-v', version,
                '-e', vendor,
                '-o', filepath]
        
        for ns in nameservers:
            argv.append(ns.path)

        if verbose: sys.stdout.write('## rtcryo %s\n' % argv)
        from rtshell import rtcryo
        rtcryo.main(argv=argv)

        return 0

