import sys
import wasanbon

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        sys.stdout.write(' - Platform = %s\n' % wasanbon.platform())
        sys.stdout.write(' - Version  = %s\n' % wasanbon.get_version())

