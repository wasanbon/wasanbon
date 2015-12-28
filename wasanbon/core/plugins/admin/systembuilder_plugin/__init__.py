import time, sys, os

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):
    """ This plugin provides building RT-system (connecting and configuring) APIs """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']


    def get_component_full_path(self, comp):
        str = ""
        for p in comp.full_path:
            str = str + p
            if not str.endswith('/') and not str.endswith('.rtc'):
                str = str + '/'
        return str

    def get_port_full_path(self, port):
        return self.get_component_full_path(port.owner) + ':' + port.name

    def connect_ports(self, port1, port2, props = {}, verbose=False):
        if verbose: sys.stdout.write('## Connecting %s to %s\n' % (self.get_port_full_path(port1),
                                                                   self.get_port_full_path(port2)))
        # from rtshell.rtcon import connect_ports
        port1.connect([port2], props=props)
        
        return 0

    def set_active_configuration_data(self, rtc, key, value):
        for conf in rtc.configuration_sets:
            if conf.id == rtc.active_configuration_set:
                for conf_data in conf.configuration_data:
                    if conf_data.name == key:
                        conf_data.data = value
        pass


    def build_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Building RT-System (file=%s)\n' % system_file)
            from rtshell import rtresurrect
            if rtresurrect.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()

    def activate_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Activating RT-System (file=%s)\n' % system_file)
            from rtshell import rtstart
            if rtstart.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()
    

    def deactivate_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Activating RT-System (file=%s)\n' % system_file)
            from rtshell import rtstop
            if rtstop.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()
    
    
