import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package']

    def __call__(self, argv):
        print ' # this is plain function'
        pass

    def status(self, argv):
        """ This is print function
        """
        print '# Status of this package'
        packs = wasanbon.plugins.admin.package.package.get_packages()
        import os
        for p in packs:
            if p.path == os.getcwd():
                print 'Name : %s' % (p.name)
                print 'Path :'
                print '  /      : %s' % p.path
                print '  rtc    : %s' % p.get_rtcpath(fullpath=False)
                print '  bin    : %s' % p.get_binpath(fullpath=False)
                print '  conf   : %s' % p.get_confpath(fullpath=False)
                print '  system : %s' % p.get_systempath(fullpath=False)
        

    def echo(self, argv):
        """ This is help text
        """
        print ' # This is test plugin'

