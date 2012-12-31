#!/usr/bin/env python

import OpenTPR.core.ParseRTC

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if argv[2] == 'parse':
            OpenTPR.core.ParseRTC.parse_rtcs()

        pass
