import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']

    def get_connectable_pairs(self, nameservers, verbose=False):
        pairs = []

        # For DataPorts
        outports = []
        for ns in nameservers:
            outports = outports + ns.dataports(port_type='DataOutPort')
        for outport in outports:
            inports = []
            for ns in nameservers:
                inports = inports + ns.dataports(port_type='DataInPort', 
                                                 data_type=outport.properties['dataport.data_type'])
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

    
    
