#!/usr/bin/env python

import os, sys
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core.package import run
from wasanbon.core import rtc, tools, repositories
from wasanbon.util import editor
from wasanbon import util


class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        _package = pack.Package(os.getcwd())
        return [rtc.name for rtc in _package.rtcs]

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())
        sys.stdout.write(' @ Executing RTC %s\n' % argv[2])
        rtc_ = _package.rtc(argv[2])
        rtcconf = _package.rtcconf(rtc_.language)
        rtc_temp = os.path.join("conf", "rtc_temp.conf")
        if os.path.isfile(rtc_temp):
            os.remove(rtc_temp)
        rtcconf.sync(verbose=True, outfilename=rtc_temp)
        _package.uninstall(_package.rtcs, rtcconf_filename=rtc_temp, verbose=True)
        _package.install(rtc_, rtcconf_filename=rtc_temp, copy_conf=False)

        try:
            if rtc_.language == 'C++':
                p = run.start_cpp_rtcd(rtc_temp, verbose=True)
            elif rtc_.language == 'Python':
                p = run.start_python_rtcd(rtc_temp, verbose=True)
            elif rtc_.language == 'Java':
                p = run.start_java_rtcd(rtc_temp, verbose=True)
            p.wait()
        except KeyboardInterrupt, e:
            sys.stdout.write(' -- Aborted.\n')


