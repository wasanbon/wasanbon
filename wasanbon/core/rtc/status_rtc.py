import os, sys
from kotobuki.core.rtc.rtcprofile import *

bin_ext = 'dylib' if sys.platform == 'darwin' else ('dll' if sys.platform == 'win32' else 'so')

#def get_rtc_cpp_name_list(rtc_name):
#    if sys.platform == 'darwin':
#        return ['%s.%s' % (rtc_name, 'dylib')]
#    elif sys.platform == 'win32':
#        return ['%s.%s' % (rtc_name.lower(), 'dll')]
#    elif sys.platform == 'linux2':
#        return ['%s.%s' % (rtc_name, 'so')]
#    else:
#        raise InstallError('ERROR:Unsupported Operating System(%s)' % sys.platform)


def find_rtc_conf(rtcp):
    conf_file_name = rtcp.getName() + '.conf'
    [path_, file_] = os.path.split(rtcp.filename)
    conf_files_ = search_rtc.search_file(path_, conf_file_name)
    if len(conf_files_) == 1:
        return conf_files_[0]
    elif len(conf_files_) == 0:
        return None
    else:
        return on_multiple_conffile(conf_files_)

def on_multiple_conffile(files):
    print 'Multiple RTC.conf files are found:'
    for f in files:
        print '--' + f
    
    print 'Current Version cannot handle this warning.'
    print 'Use %s' % files[0]
    return files[0]


def on_multiple_rtcfile(files):
    print 'Multiple RTC files are found:'
    for f in files:
        print '--' + f
    
    print 'Current Version cannot handle this warning.'
    print 'Use %s' % files[0]
    return files[0]

def find_rtc_bin(rtcp):
    if rtcp.getLanguage() == 'C++':
        rtc_file_name_list = rtcp.getName() + '.' + bin_ext
    elif rtcp.getLanguage() == 'Python':
        rtc_file_name_list = rtcp.getName() + '.py'
    elif self.getLanguage() == 'Java':
        rtc_file_name_list = rtcp.getName() + '.jar'
    else:
        raise InvalidRTCProfileError(filename, 'Unsupported Language(%s)' % getLanguage())

    [path_, file_] = os.path.split(rtcp.filename)

    rtcs_files_ = search_rtc.search_file(path_, rtc_file_name_list)
    rtcs_files_available_ = []
        
    for file_ in rtcs_files_:
        if file_.count('Debug') > 0:
            print 'RTC file (%s) seems to build in Debug mode.' % file_
            print 'Debug mode binary is not available.'
        else:
            rtcs_files_available_.append(file_)
            pass
        rtcs_files_ = rtcs_files_available_

    if len(rtcs_files_) == 1:
        return rtcs_files_[0]
    elif len(rtcs_files_) == 0:
        return None
    else:
        return on_multiple_rtcfile(rtcs_files_)

    
