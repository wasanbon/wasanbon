import os, sys, time, subprocess, signal, yaml, getpass, threading, traceback, optparse
import wasanbon
from wasanbon.core import package, nameserver
from wasanbon import util


def get_rtc_rtno(_package, name, verbose=False):
    try:
        return _package.rtc(name)
    except wasanbon.RTCNotFoundException, e:
        return tools.get_rtno_package(_package, name, verbose=verbose)
    
def alternative():
    return  ['all'] + [rtc.name for rtc in package.Package(os.getcwd()).rtcs]

def execute_with_argv(argv, verbose, force=False, clean=False):
    wasanbon.arg_check(argv, 3)

    _package = package.Package(os.getcwd())
    if 'all' in argv[2:]:
        rtc_names = [rtc.name for rtc in _package.rtcs]
    else:
        rtc_names = [arg for arg in argv[2:] if not arg.startswith('-')]

    for name in rtc_names:
        sys.stdout.write(' @ Installing RTC (%s).\n' % name)
        try:
            #_package.install(_package.rtc(name), verbose=verbose)
            rtc = _package.rtc(name)
            package.install_rtc(_package, rtc, verbose=verbose, overwrite_conf=force)
        except Exception, ex:
            sys.stdout.write(' - Installing RTC %s failed.\n' % name)
            print ex



