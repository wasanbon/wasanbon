from wasanbon import setup

class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return []

    def execute_with_argv(self, args, force=False, verbose=False, clean=False):
        sys.stdout.write(' - Starting wasanbon environment.\n')
        
