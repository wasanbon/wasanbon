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

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())
        for rtcname in argv[2:]:
            _package.delete_rtc(_package.rtc(rtcname), verbose=verbose)

