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

    def alternative(self):
        _package = pack.Package(os.getcwd())
        return [rtc.name for rtc in _package.rtcs]

    def execute_with_argv(self, args, verbose, force, clean):
        wasanbon.arg_check(argv, 4)
        _package = pack.Package(os.getcwd())
        sys.stdout.write(' @ Commiting Changes of RTC %s\n' % argv[2])
        rtc_ = self.get_rtc_rtno(_package, argv[2], verbose=verbose)
        rtc_.commit(comment=argv[3], verbose=verbose)
        _package.update_rtc_repository(rtc_.repository, verbose=verbose)
