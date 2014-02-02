#!/usr/bin/env python

import os, sys, optparse, yaml, types
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core import rtc, tools, repositories
from wasanbon.util import editor
from wasanbon import util


class Command(object):
    def __init__(self):
        pass

    def get_rtc_rtno(self, _package, name, verbose=False):
        try:
            return _package.rtc(name)
        except wasanbon.RTCNotFoundException, e:
            return tools.get_rtno_package(_package, name, verbose=verbose)

    def alternative(self):
        _package = pack.Package(os.getcwd())
        return [rtc.name for rtc in _package.rtcs]

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        sys.stdout.write(' @ Pulling the changing upstream RTC repository %s\n' % argv[2])
        _package = pack.Package(os.getcwd())
        rtc_ = self.get_rtc_rtno(_package, argv[2], verbose=verbose)
        rtc_.pull(verbose=verbose)
        _package.update_rtc_repository(rtc_.repository, verbose=verbose)

