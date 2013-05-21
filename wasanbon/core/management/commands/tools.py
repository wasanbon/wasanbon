from wasanbon.core import tools 
from wasanbon.core import system

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')

        if(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')

        if(argv[2] == 'rtse'):
            print 'Launching Eclipse'

            system.run_system(argv, nobuild=True)
            tools.launch_eclipse('RTS_DIR')
            system.terminate_all_process()

