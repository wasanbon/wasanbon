#!/usr/bin/env python

import OpenTPR
import OpenRTM_aist


def CommandInit(manager):
    pass

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        args = ['OpenTPR', '-f', 'conf/rtc.conf']
        print args
        mgr = OpenRTM_aist.Manager.init(args)
        mgr.setModuleInitProc(CommandInit)
        mgr.activateManager()
        mgr.runManager()
        pass
