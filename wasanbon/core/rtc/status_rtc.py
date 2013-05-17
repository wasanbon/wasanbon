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


