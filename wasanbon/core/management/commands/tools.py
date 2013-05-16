from wasanbon.core import tools 

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')

        if(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')

        if(argv[2] == 'rtse'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTS_DIR')
