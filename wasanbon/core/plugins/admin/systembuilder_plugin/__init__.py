import time, sys, os
from rtshell import rtstart, rtresurrect, rtstop
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment']


    def build_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Building RT-System (file=%s)\n' % system_file)
            if rtresurrect.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()

    def activate_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Activating RT-System (file=%s)\n' % system_file)
            if rtstart.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()
    

    def deactivate_system(self, package, system_file=None, verbose=False, try_count=5, wait_time=1.0):
        if system_file is None:
            system_file = package.default_system_filepath

        for i in range(0, try_count):
            if verbose: sys.stdout.write('# Activating RT-System (file=%s)\n' % system_file)
            if rtstop.main([system_file]) == 0:
                return 0
            time.sleep(wait_time)
        raise wasanbon.BuildSystemException()
    
    
