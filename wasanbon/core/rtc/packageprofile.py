import os, sys
from wasanbon import util
from wasanbon.core import *


class PackageProfile(object):
    """
    """
    def __init__(self, rtcp):
        self.rtcprofile = rtcp
        [self.path, dummy] = os.path.split(rtcp.path)
        self.bin = find_rtc_bin(rtcp)
        self.conf = find_rtc_conf(rtcp)
        self.sources = find_rtc_srcs(rtcp)
        self.executable = find_rtc_exec(rtcp)
        if self.bin == None:
            self.bin = ''
        if self.conf == None:
            self.conf = ''

    def getPackagePath(self):
        return self.path

    def getRTCFilePath(self, verbose=False):
        return self.bin

    @property
    def bin_filename(self):
        return get_rtc_bin_filename(self.rtcprofile)

    @property
    def conf_filename(self):
        return os.path.basename(self.conf)
        
    def get_rtc_bin_filename(self):
        return get_rtc_bin_filename(self.rtcprofile)

    def getConfFilePath(self):
        return self.conf

    def getSourceFiles(self):
        return self.sources

    def getRTCExecutableFilePath(self):
        return self.executable


def get_rtc_bin_filename(rtcp):
    if rtcp.language.kind == 'C++':
        if sys.platform == 'win32':
            bin_ext = 'dll'
        elif sys.platform == 'linux2':
            bin_ext = 'so'
        elif sys.platform == 'darwin':
            bin_ext = 'dylib'
        else:
            sys.stdout.write('Unsupported platform %s' % sys.platform)
            return
        rtc_file_name_list = rtcp.basicInfo.name + '.' + bin_ext
    elif rtcp.language.kind == 'Python':
        rtc_file_name_list = rtcp.basicInfo.name + '.py'
    elif rtcp.language.kind == 'Java':
        rtc_file_name_list = rtcp.basicInfo.name + '.jar'
    else:
        raise InvalidRTCProfileError(self.filename, 'Unsupported Language(%s)' % rtcp.language.kind)

    return rtc_file_name_list


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
        print '--' + f
    
    print 'Current Version cannot handle this warning.'
    print 'Use %s' % files[0]
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


