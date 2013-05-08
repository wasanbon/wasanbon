from wasanbon.core import rtc

def print_usage():
    print 'Usage: %s system install [RTC NAME]\n' % argv[0]
    pass

class Command(object):
    """
    """

    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if len(argv) < 4:
            print_usage()
        rtcps = rtc.parse_rtcs()
        if(argv[2] == 'install'):
            print 'Installing RTC %s' % argv[3]
            for rtcp in rtcps:
                if rtcp.getName() == argv[3]:
                    rtc.install(rtcp)
