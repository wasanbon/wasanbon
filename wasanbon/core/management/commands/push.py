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
        wasanbon.arg_check(argv, 3)

        sys.stdout.write(' @ Pushing RTC repository  %s to upstream.\n' % argv[2])
        pself.get_rtc_rtno(_package, argv[2], verbose=verbose).push(verbose=True) # when pushing always must be verbose 

