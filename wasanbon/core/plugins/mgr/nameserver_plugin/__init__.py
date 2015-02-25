import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.nameserver', 'admin.package']

    @manifest
    def list(self, argv):
        """ List Nameservices in Package """
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        package = admin.package.get_package_from_path(os.getcwd())
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        for ns in nss:
            sys.stdout.write(' - %s\n' % ns.path)

        return 0

    @manifest
    def is_running(self, argv):
        """ Check Nameservice is launched """
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        package = admin.package.get_package_from_path(os.getcwd())
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        retval  =0
        for ns in nss:
            if verbose: sys.stdout.write('# Checking NameServer %s\n' % ns.path)
            ret = admin.nameserver.is_running(ns, verbose=verbose)

            if ret:
                sys.stdout.write('## Name Server (%s) is running.\n' % ns.path)
            else:
                sys.stdout.write('## Name Server (%s) is not running.\n' % ns.path)
                retval = -1
            
        return retval

    @manifest 
    def terminate(self, argv):
        """ Terminate NameService with Package setting
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        package = admin.package.get_package_from_path(os.getcwd())
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        retval = 0
        for ns in nss:
            ret = admin.nameserver.terminate(ns, verbose=verbose)
            if ret != 0:
                retval = ret

        return retval


    @manifest
    def launch(self, argv):
        """ Launch NameService with Package setting
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:])
        verbose = options.verbose_flag # This is default option
        force   = options.force_flag

        package = admin.package.get_package_from_path(os.getcwd())
        nss = admin.nameserver.get_nameservers_from_package(package, verbose=verbose)
        retval = 0
        for ns in nss:
            ret = admin.nameserver.launch(ns, verbose=verbose, force=force, pidfile=True)
            if ret != 0:
                retval = ret

        return retval
