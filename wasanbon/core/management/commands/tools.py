from wasanbon.core import tools 

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if(argv[2] == 'install'):
            print 'Installing Tools'
            tools.install_tools()
        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse()
