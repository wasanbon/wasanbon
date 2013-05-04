#!/usr/bin/env python

import os
import sys
import optparse

class OptionParserEx(optparse.OptionParser):
    
    def error(self, msg):
        pass

    def print_help(self):
        pass


    def _process_args(self, largs, rargs, values):
        while rargs:
            arg = rargs[0]
            try:
                if arg[0:2] == '--' and len(arg) > 2:
                    self._process_long_opt(rargs, values)
                elif arg[:1] == '-' and len(arg) > 1:
                    self._process_short_opts(rargs, values)
                else:
                    del rargs[0]
                    raise Exception

            except:
                largs.append(arg)
