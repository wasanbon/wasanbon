#!/usr/bin/env python
import os, sys
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core import rtc
class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        _package = pack.Package(os.getcwd())
        return [rtc.name for rtc in _package.rtcs]

    def get_rtc_rtno(self, _package, name, verbose=False):
        try:
            return _package.rtc(name)
        except wasanbon.RTCNotFoundException, e:
            return tools.get_rtno_package(_package, name, verbose=verbose)

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())
        sys.stdout.write(' @ Checkout and overwrite  RTC %s\n' % argv[3])
        self.get_rtc_rtno(_package, argv[2], verbose=verbose).checkout(verbose=verbose)
