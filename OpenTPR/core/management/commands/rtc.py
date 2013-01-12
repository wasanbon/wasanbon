#!/usr/bin/env python

from OpenTPR.core.rtc.search_rtc import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if argv[2] == 'search':
            rtcp_ = parse_rtcs()
            print rtcp_
        pass
