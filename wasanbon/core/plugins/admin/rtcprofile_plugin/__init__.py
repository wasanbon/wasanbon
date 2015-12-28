import sys, os, time, traceback
import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):
    """ This plugin provides APIs for RTC.xml manaagement"""
    def __init__(self):
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
        tree = None
        import CORBA
        while True:
            try:
                if verbose: sys.stdout.write('# Searching for RTC (%s)\n' % full_path)
                tree = rtctree.tree.RTCTree(paths=path, filter=filter)
                comp = tree.get_node(path)

                if not comp.is_component:
                    sys.stdout.write(' Object is not component\n')
                    return None

                break
            except:
                if verbose: traceback.print_exc()
            time.sleep(1.0)
    
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
                    rtcb.appendServiceInterfaceToServicePort(p.name, 
                                                             path, 
                                                             idlFile, 
                                                             i.type_name,
                                                             i.polarity_as_string(add_colour=False),
                                                             i.instance_name)
        
        return rtcb.buildRTCProfile()
    
    def tostring(self, rtcp, pretty_print=True):
        import rtcprofile
        return rtcprofile.tostring(rtcp, pretty_print=pretty_print)

    def compare_rtcprofile(self, rtcp0, rtcp1, verbose=False):
        return compare_rtcprofile(rtcp0, rtcp1, verbose=verbose)
    
def compare_rtcprofile(rtcp, rtcp_real, verbose=False):
    import rtcprofile
    b = rtcprofile.RTCProfileBuilder(rtcp)
    modifiedFlag = False
    # compare dataports
    if verbose: sys.stdout.write('# Comparing RTC.xml with Running RTC(%s)\n' % (rtcp.name))
    
    basicInfo_diff = False
    if rtcp_real.basicInfo.name != rtcp.basicInfo.name or \
       rtcp_real.basicInfo.category != rtcp.basicInfo.category or \
       rtcp_real.basicInfo.vendor != rtcp.basicInfo.vendor or \
       rtcp_real.basicInfo.version != rtcp.basicInfo.version or \
       rtcp_real.basicInfo.description != rtcp.basicInfo.description:
        from wasanbon import util
        if util.yes_no('# Basic Info is different. Update?:') == 'yes':
            b.setBasicInfo(rtcp_real.basicInfo.name, rtcp_real.basicInfo.category,
                           rtcp_real.basicInfo.vendor, 
                           rtcp_real.basicInfo.version, rtcp_real.basicInfo.description)
            modifiedFlag = True
    
    for dp in rtcp.dataports:
        match_flag = False
        if verbose:
            sys.stdout.write('# Searching DataPort in RTC %s : %s (written in RTC.xml)... ' % (dp['rtc:name'], dp['rtc:type']))
        for dp_real in rtcp_real.dataports:
            if dp.equals(dp_real):
                match_flag = True
                break
        
        if not match_flag: # RTC.xml does not have dp
            if verbose: sys.stdout.write('## Not Found in the running RTC\n')
            b.removeDataPort(dp)
            modifiedFlag = True
        else:
            if verbose: sys.stdout.write('## Match.\n')

    for dp_real in rtcp_real.dataports:
        match_flag = False
        if verbose:
            sys.stdout.write('# Searching DataPort in RTC.xml %s : %s (implemented in RTC)... ' % (dp_real['rtc:name'], dp_real['rtc:type']))
        for dp in rtcp.dataports:
            if dp.equals(dp_real):
                match_flag = True
                break
        
        if not match_flag: # RTC.xml does not have dp
            if verbose: sys.stdout.write('## Not Found in the existing RTC.xml\n')
            b.appendDataPort(dp_real.portType, dp_real.type, dp_real.name)
            modifiedFlag = True
        else:
            if verbose: sys.stdout.write('## Match.\n')

    for sp in rtcp.serviceports:
        match_flag = False
        if verbose:
            sys.stdout.write('# Searching ServicePort %s (writeen in RTC.xml) ...' % (sp['rtc:name']))
        for sp_real in rtcp_real.serviceports:
            if sp.equals(sp_real):
                match_flag = True
                if verbose: sys.stdout.write('## Match.\n')
                for i in sp.serviceInterfaces:
                    i_match_flag = False
                    if verbose: sys.stdout.write('## Searching ServiceInterface %s :: %s (written in RTC.xml) ... ' % (i.name, i.type))
                    for i_real in sp_real.serviceInterfaces:
                        if i.equals(i_real):
                            i_match_flag = True
                            if verbose: sys.stdout.write('### Match\n')
                    if not i_match_flag:
                        if verbose: sys.stdout.write('### Not Found.\n')
                        b.removeServiceInterfaceFromServicePort(sp.name, i.name)
                        modifiedFlag = True
                break
        if not match_flag:
            if verbose: sys.stdout.write('## Not Found in the running RTC\n')
            b.removeServicePort(sp)
            modifiedFlag = True


    for sp_real in rtcp_real.serviceports:
        match_flag = False
        if verbose:
            sys.stdout.write('# Searching ServicePort %s (implemented in RTC)' % (sp_real['rtc:name']))
        for sp in rtcp.serviceports:
            if sp.equals(sp_real):
                match_flag = True
                if verbose: sys.stdout.write('## Match.\n')

                for i_real in sp_real.serviceInterfaces:
                    i_match_flag = False
                    if verbose: sys.stdout.write('## Searching ServiceInterface %s :: %s (implemented in RTC)' % (i_real.name, i_real.type))
                    for i in sp.serviceInterfaces:
                        if i.equals(i_real):
                            i_match_flag = True
                            if verbose: sys.stdout.write('### Match\n')
                    if not i_match_flag:
                        if verbose: sys.stdout.write('### Not Found.\n')
                        b.appendServiceInterfaceToServicePort(sp_real.name, "", "", i_real.type, i_real.direction, i_real.name)
                        modifiedFlag = True
                break
        if not match_flag:
            if verbose: sys.stdout.write('## Not Found in RTC.xml\n')
            b.appendServicePort(sp_real.name)
            for i in sp_real.serviceInterfaces:
                b.appendServiceInterfaceToServicePort(sp_real.name, "", "", i.type, i.direction, i.name)
            modifiedFlag = True

    if rtcp.configurationSet:
        for conf in rtcp.configurationSet.configurations:
            match_flag = False
            if verbose: sys.stdout.write('# Searching Configuration %s (written in RTC.xml) ... ' % (conf.name))
            for conf_real in rtcp_real.configurationSet.configurations:
                if conf.equals(conf_real):
                    match_flag = True
                    if verbose: sys.stdout.write('## Match\n')
                    pass
                pass
            if not match_flag:
                if verbose: sys.stdout.write('## Not Found in the running RTC\n')
                b.removeConfiguration(conf.name)
                modifiedFlag = True
                pass
            pass
        pass
    
    
    for conf_real in rtcp_real.configurationSet.configurations:
        match_flag = False
        if verbose: sys.stdout.write('# Searching Configuration %s (implemented in RTC) ...' % (conf_real.name))
        if rtcp.configurationSet:
            for conf in rtcp.configurationSet.configurations:
                if conf.equals(conf_real):
                    match_flag = True
                    if verbose: sys.stdout.write('## Match\n')
                    pass
                pass
            pass
        if not match_flag:
            if verbose: sys.stdout.write('## Not Found in the existing RTC.xml\n')
            b.appendConfiguration(conf_real.type, conf_real.name, conf_real.defaultValue)
            modifiedFlag = True
            pass
        pass

    if modifiedFlag:
        if verbose: sys.stdout.write("Modified.\n")
        return b.buildRTCProfile()
    if verbose: sys.stdout.write('Not Modified.\n') 
    return None
