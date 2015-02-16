import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.git']

    @property
    def binder(self):
        import binder
        return binder

    def _print_alternatives(self):
        print 'hoo'
        print 'foo'
        print 'hoge'
        print 'yah'

    def update(self, argv):
        """ This is help text
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option


        import binder
        path = os.path.join(wasanbon.plugins.admin.environment.setting_path, '..', 'repository.yaml')
        binder.download_repositories(path, verbose=verbose)

    def list(self, args):
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        import binder
        binders = binder.get_binders(verbose=verbose)
        print binders
        
    def rtcs(self, args):
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        long = options.long_flag

        import binder
        binders = binder.get_binders(verbose=verbose)
        for binder in binders:
            for rtc in binder.rtcs:
                if not long:
                    print ' - %s' % rtc.name
                else:
                    print '%s :' % rtc.name
                    print '  %s : %s' % ('url', rtc.url)
                    print '  %s : %s' % ('type', rtc.type)
                    print '  %s : %s' % ('description', rtc.description)
                    print '  %s : %s' % ('platform', rtc.platform)
            

    def packages(self, args):
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        options, argv = self.parse_args(args)
        verbose = options.verbose_flag
        long = options.long_flag

        import binder
        binders = binder.get_binders(verbose=verbose)
        for binder in binders:
            for package in binder.packages:
                if not long:
                    print ' - %s' % package.name
                else:
                    print '%s :' % package.name
                    print '  %s : %s' % ('url', package.url)
                    print '  %s : %s' % ('type', package.type)
                    print '  %s : %s' % ('description', package.description)
                    print '  %s : %s' % ('platform', package.platform)
            
