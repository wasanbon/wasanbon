import os, types, traceback, sys
from twisted.web import server, xmlrpc, resource
from twisted.web.xmlrpc import withRequest

import WSB
from plugin import *
from misc import *
from processes import *
from nameservice import *
from files import *
from setting import *
from mgrRtc import *
from mgrRepository import *
from mgrSystem import *
from adminPackage import *
from adminRepository import *
from wsconverter import *
from appshare import *

class RpcManager(xmlrpc.XMLRPC):
    """
    An example object to be published.
    """
    isLeaf = True

    def __init__(self, directory=None, verbose=False):
        xmlrpc.XMLRPC.__init__(self, allowNone=True)

        self.add_plugin(MiscPlugin(), verbose=verbose)
        self.add_plugin(SettingPlugin(), verbose=verbose)
        self.add_plugin(FilesPlugin(), verbose=verbose)
        self.add_plugin(ProcessesPlugin(), verbose=verbose)
        self.add_plugin(MgrRtcPlugin(), verbose=verbose)
        self.add_plugin(MgrRepositoryPlugin(), verbose=verbose)
        self.add_plugin(MgrSystemPlugin(), verbose=verbose)
        self.add_plugin(AdminPackagePlugin(), verbose=verbose)
        self.add_plugin(AdminRepositoryPlugin(), verbose=verbose)
        self.add_plugin(NameServicePlugin(), verbose=verbose)
        self.add_plugin(WSConverterPlugin(), verbose=verbose)
        self.add_plugin(AppsharePlugin(), verbose=verbose)

        if not directory:
            directory = os.getcwd()
        self.directory = directory
        if not os.path.isdir(directory):
            os.mkdir(directory)

        self.old_directory = os.getcwd()


    def add_plugin(self, plugin_obj, verbose=False):
        except_functions = ['debug', 'return_value']
        print '# Plugin %s' % plugin_obj.name
        for atr_name in dir(plugin_obj):
            attribute = getattr(plugin_obj, atr_name)
            if atr_name.startswith('_'):
                continue
            elif atr_name in except_functions:
                continue

            if type(attribute) == types.MethodType:
                func_name = 'xmlrpc_' + plugin_obj.name + '_' + atr_name
                if verbose: print '# -Function: %s' %func_name
                setattr(self, func_name, attribute)

    def pre_rpc(self):
        os.chdir(self.directory)

    def post_rpc(self):
        os.chdir(self.old_directory)
        
    #def xmlrpc_echo(self, x):
    #
    #    return [True, x]

    def xmlrpc_get_package_alter(self, pkg, sub):
        res = WSB.getPackageAlternative(pkg, sub)
        return [True, res]
        


    # Repository Management


    def xmlrpc_repository_package(self, pkg):
        res = WSB.getRepositoryPackage(pkg)
        return [True, res]

    def xmlrpc_repository_rtc(self, rtc):
        res = WSB.getRepositoryRTC(rtc)
        return [True, res]
    
    def render_OPTIONS(self, request):    
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')        
        request.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        return ""

    # Package Management

    def xmlrpc_running_packages(self, request):
        res = WSB.getRunningPackages()
        #res = '<package></package>'
        
        return [True, (res)]

    def xmlrpc_running_packages(self):
        res = WSB.getRunningPackages()
        return [True, res]


    def xmlrpc_build_rtc(self, pkg, rtc):
        result, stdout = WSB.buildRTC(pkg, rtc)
        return [True, result, stdout]

    def xmlrpc_clean_rtc(self, pkg, rtc):
        result, stdout = WSB.cleanRTC(pkg, rtc)
        return [True, result, stdout]

    def xmlrpc_delete_rtc(self, pkg, rtc):
        result, stdout = WSB.deleteRTC(pkg, rtc)
        return [True, result, stdout]


    def xmlrpc_package_rtc(self, pkg, rtc):
        res = WSB.getPackageRTC(pkg, rtc)
        return [True, res]

    def xmlrpc_rtcconf_list(self, pkg):
        res = WSB.getRTCConfList(pkg)
        return [True, res]

    def xmlrpc_rts_profile(self, pkg, filename):
        res = WSB.getRTSProfile(pkg, filename)
        return [True, res]

    def xmlrpc_system_update(self, pkg, filename, content):
        res = WSB.updateSystemFile(pkg, filename, content)
        return [True, res]

    def xmlrpc_rtcprofile_update(self, pkg, rtc, content):
        res = WSB.updateRTCProfile(pkg, rtc, content)
        return [True, res]

    def xmlrpc_rtcprofile_sync(self, pkg, rtc):
        res = WSB.syncRTCProfile(pkg, rtc)
        return [True, res]
    
    def xmlrpc_system_copy(self, pkg, srcfilename, dstfilename):
        res = WSB.copySystem(pkg, srcfilename, dstfilename)
        return [True, res]
    
    def xmlrpc_system_delete(self, pkg, filename):
        res = WSB.deleteSystem(pkg, filename)
        return [True, res]

    def xmlrpc_system_list(self, pkg):
        res = WSB.getSystemList(pkg)
        return [True, res]

    def xmlrpc_misc_send_code(self, code):
        res = WSB.sendCode(code)
        return [True, res]

    def xmlrpc_misc_start_code(self, filename):
        res = WSB.startCode(filename)
        return [True, res]

    def xmlrpc_misc_kill_code(self, filename):
        res = WSB.killCode(self, filename)
        return [True, res]

    def xmlrpc_misc_read_stdout(self, filename):
        res = WSB.readStdout(filename)
        return [True, res]

    def xmlrpc_misc_communicate(self, filename):
        res = WSB.communicate(filename)
        return [True, res]
