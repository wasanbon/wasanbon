
import os, sys
import wasanbon
from wasanbon import util
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):
    """ This plugin provides search and access APIs from package """
    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        import rtc
        rtc.plugin_obj = self
        pass

    def depends(self):
        return ['admin.environment', 'admin.rtcprofile']

    def get_rtcs_from_package(self, package, verbose=False):
        return get_rtcs_from_package(package, verbose=verbose)

    def get_rtc_from_package(self, package, rtcname, verbose=False):
        if verbose: sys.stdout.write('# Searching RTC (%s) from Package (%s)...\n' % (rtcname, package.name))
        rtcs = get_rtcs_from_package(package, verbose=verbose)

        for rtc in rtcs:
            if rtc.rtcprofile.basicInfo.name == rtcname:
                return rtc
        raise wasanbon.RTCNotFoundException


class RTCPackage(object):
    def __init__(self, path, verbose=False):
        self._path = path
        self._rtcprofile_path = os.path.join(path, 'RTC.xml')
        import wasanbon
        if not os.path.isfile(self._rtcprofile_path):
            raise wasanbon.RTCProfileNotFoundException()

        self._rtcprofile = None

    @property
    def path(self):
        return self._path

    @property
    def rtcprofile(self):
        if self._rtcprofile is None:
            #rtcprofile = plugin_obj.admin.rtcprofile.rtcprofile
            #from __init__ import admin
            rtcprofile = admin.rtcprofile.rtcprofile
            self._rtcprofile = rtcprofile.RTCProfile(self._rtcprofile_path)
        return self._rtcprofile
    
    def get_rtc_profile_path(self, verbose=False):
        return self._rtcprofile_path

    def get_rtc_file_path(self, verbose=False):
        return find_rtc_bin(self.rtcprofile)

    def get_rtc_executable_file_path(self, verbose=False):
        return find_rtc_exec(self.rtcprofile)

    def get_rtc_conf_path(self, verbose=False):
        return find_rtc_conf(self.rtcprofile)

def get_rtcs_from_package(package, verbose=False):
    import wasanbon
    rtcs = []

    for rtc_dir in os.listdir(package.get_rtcpath()):
        rtc_fullpath = os.path.join(package.get_rtcpath(), rtc_dir)
        if not os.path.isdir(rtc_fullpath):
            continue
        try:
            rtc = RTCPackage(rtc_fullpath, verbose=verbose)
            rtcs.append(rtc)
        except wasanbon.RTCProfileNotFoundException, ex:
            pass
    return rtcs



def find_rtc_srcs(rtcp):
    [path, file] = os.path.split(rtcp.filename)
    if rtcp.language.kind == 'Python':
        return util.search_file(path, rtcp.basicInfo.name + '.py')
    elif rtcp.language.kind == 'Java':
        return util.search_file(path, rtcp.basicInfo.name + 'Impl.java')
    elif rtcp.language.kind == 'C++':
        hdrs = util.search_file(path, rtcp.basicInfo.name + '.h')
        srcs = util.search_file(path, rtcp.basicInfo.name + '.cpp')
        return hdrs + srcs

def find_rtc_exec(rtcp):
    if rtcp.language.kind == 'C++':
        [path, file] = os.path.split(rtcp.filename)
        exec_file_name = rtcp.basicInfo.name + "Comp"
        if sys.platform == 'win32':
            exec_file_name = exec_file_name + ".exe"
        files = util.search_file(path, exec_file_name)
        if len(files) == 0:
            return ""
        return files[0]
    elif rtcp.language.kind == 'Python':
        return find_rtc_bin(rtcp)
    elif rtcp.language.kind == 'Java':
        return find_rtc_bin(rtcp)
        

def get_rtc_bin_filename(rtcp):
    if rtcp.language.kind == 'C++':
        if sys.platform == 'win32':
            bin_ext = 'dll'
        elif sys.platform == 'linux2':
            bin_ext = 'so'
        elif sys.platform == 'darwin':
            bin_ext = 'dylib'
        else:
            raise wasanbon.UnsupportedSystemException()
            return
        rtc_file_name_list = rtcp.basicInfo.name + '.' + bin_ext
    elif rtcp.language.kind == 'Python':
        rtc_file_name_list = rtcp.basicInfo.name + '.py'
    elif rtcp.language.kind == 'Java':
        rtc_file_name_list = rtcp.basicInfo.name + '.jar'
    else:
        raise wasanbon.InvalidRTCProfileException()

    return rtc_file_name_list


def find_rtc_bin(rtcp):
    rtc_file_name_list = get_rtc_bin_filename(rtcp)

    [path, file] = os.path.split(rtcp.filename)

    try:
        rtcs_files = util.search_file(path, rtc_file_name_list)
    except OSError:
        return ""

    rtcs_files_available = []
        
    for file in rtcs_files:
        if file.count('Debug') > 0:
            sys.stdout.write('RTC file (%s) seems to build in Debug mode.\n' % file)
            sys.stdout.write('Debug mode binary is not available.\n')
        else:
            rtcs_files_available.append(file)

    rtcs_files = rtcs_files_available

    if len(rtcs_files) == 1:
        return rtcs_files[0]
    elif len(rtcs_files) == 0:
        return ""
    else:
        return on_multiple_rtcfile(rtcs_files)

    
def on_multiple_rtcfile(files):
    for f in files:
        print '# -' + f
    
    print '# Current Version cannot handle this warning.'
    print '# Use %s' % files[0]
    return files[0]


def find_rtc_conf(rtcp):
    conf_file_name = rtcp.basicInfo.name + '.conf'
    [path, file] = os.path.split(rtcp.filename)
    try:
        conf_files = util.search_file(path, conf_file_name)
    except OSError:
        return ""

    if len(conf_files) == 1:
        return conf_files[0]
    elif len(conf_files) == 0:
        return ""
    else:
        return on_multiple_conffile(conf_files)

def on_multiple_conffile(files):
    print 'Multiple RTC.conf files are found:'
    for f in files:
        print '--' + f
    
    print 'Current Version cannot handle this warning.'
    print 'Use %s' % files[0]
    return files[0]


