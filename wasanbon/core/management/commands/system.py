import os, sys, time, subprocess, signal
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run


class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3 or argv[2] == 'help':
            show_help_description('system')
            return

        rtcps = rtc.parse_rtcs()
        if(argv[2] == 'install'):
            if len(argv) < 4:
                show_help_description('system')
                return

            if argv[3] == 'all':
                for rtcp in rtcps:
                    print 'Installing RTC %s' % rtcp.getName()
                    rtc.install(rtcp)
                return

            for rtcp in rtcps:
                if rtcp.getName() == argv[3]:
                    print 'Installing RTC %s' % argv[3]
                    rtc.install(rtcp)
                    return
            print 'RTC(%s) can not found.' % argv[3]

        elif(argv[2] == 'run'):
            if len(argv) >= 4 and argv[3] == '--nobuild':
                sys.stdout.write('\n - Launch System without System Build.\n\n')
                nobuild=True
            else:
                nobuild=False

            system.run_system(nobuild=nobuild)

        elif(argv[2] == 'datalist'):
            system.list_rtcs_by_dataport()
                 
