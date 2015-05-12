import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']


    @property
    def rtcprofile(self):
        import rtcprofile
        return rtcprofile

    def create_rtcprofile(self, rtc, ns="localhost:2809", verbose=False):
        import rtcprofile
        rtcb = rtcprofile.RTCProfileBuilder()
    
        import rtctree.path
        import rtctree.tree
        ns_addr = ns
        full_path = '/' + ns_addr + '/' + rtc.rtcprofile.basicInfo.name + '0' + '.rtc'
        path, port = rtctree.path.parse_path(full_path)
        if not path[-1]:
            # There was a trailing slash
            trailing_slash = True
            path = path[:-1]
        filter = []
        tree = rtctree.tree.RTCTree(paths=path, filter=filter)
        comp = tree.get_node(path)    
        if not comp.is_component:
            sys.stdout.write(' Object is not component\n')
            return None
    
        rtcb.setBasicInfo(comp.type_name, comp.category, comp.vendor, comp.version, comp.description)
        rtcb.setLanguage(comp.properties['language'])
        keys = [key for key in comp.properties.keys() if key.startswith('conf.default')]
        for key in keys:
            type = 'string'
            rtcb.appendConfiguration(type, key.split('.')[-1], comp.properties[key])
            
        for p in comp.ports:
            if p.porttype == 'DataOutPort':
                data_type = p.properties['dataport.data_type'].split(':')[1].replace('/', '::')
                rtcb.appendDataPort('DataOutPort', data_type, p.name)
            elif p.porttype == 'DataInPort':
                data_type = p.properties['dataport.data_type'].split(':')[1].replace('/', '::')
                rtcb.appendDataPort('DataInPort', data_type, p.name)
            elif p.porttype == 'CorbaPort':
                rtcb.appendServicePort(p.name)
                for i in p.interfaces:
                    path = ""
                    idlFile = ""
                    rtcb.appendServiceInterfaceToServicePort(p.name, path, idlFile, i.type_name,
                                                             i.polarity_as_string(add_colour=False),
                                                             i.instance_name)
        
        return rtcb.buildRTCProfile()
    
    def tostring(self, rtcp, pretty_print=True):
        import rtcprofile
        return rtcprofile.tostring(rtcp, pretty_print=pretty_print)
