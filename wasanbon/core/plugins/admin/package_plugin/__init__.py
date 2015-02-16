import os, sys, traceback, optparse, subprocess
import wasanbon
from wasanbon.core.plugins import PluginFunction

def print_packages():
    import package
    packages = package.get_packages()
    for p in packages:
        print p.name

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.versioning', 'admin.binder']

    @property
    def package(self):
        import package
        return package
    
    def list(self, args):
        """ List Packages installed this machie.
        # Usage $ wasanbon-admin.py package list [-l, -v]
        """
        self.parser.add_option('-l', '--long', help='Long Format (default=False)', default=False, action='store_true', dest='long_flag')
        self.parser.add_option('-q', '--quiet', help='Verbosity option (default=False)', default=False, action='store_true', dest='quiet_flag')
        options, argv = self.parse_args(args[:])

        verbose = options.verbose_flag
        if options.quiet_flag: verbose = False
        long = options.long_flag


        import package
        packages = package.get_packages(verbose=verbose)
        for p in packages:
            if not long:
                print p.name
            else:
                print p.path
        
    def directory(self, args):
        """ Show Directory of Package.
        Usage: wasanbon-admin.py package directory [PROJ_NAME] """
        options, argv = self.parse_args(args[:], print_packages)
        verbose = options.verbose_flag

        import package
        packages = package.get_packages(verbose=verbose)
        for p in packages:
            if p.name == argv[3]:
                print p.path

    def create(self, args):
        """ Create Package
        # Usage $ wasanbon-admin.py package create [PACK_NAME]  """
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag

        wasanbon.arg_check(argv, 4)
        sys.stdout.write('# Creating package %s\n' % args[3])
        import package
        return package.create_package(prjname = argv[3], verbose=verbose)

    def delete(self, args):
        """ Delete Package
        # Usage $ wasanbon-admin.py package delete [PACK_NAME]
         -r : remove directory (default False) """

        self.parser.add_option('-r', '--remove', help='Remove All Files (default=False)', default=False, action='store_true', dest='remove_flag')
        options, argv = self.parse_args(args[:], print_packages)
        verbose = options.verbose_flag
        remove = options.remove_flag

        wasanbon.arg_check(args, 4)
        import package
        retval = 0
        for n in args[3:]:
            sys.stdout.write('# Removing package %s\n' % n)
            ret = package.delete_package(n, deletepath=remove, verbose=verbose)
            if ret != 0:
                retval = 1
        return retval
    
    def _list_package_repos(self):
        for r in wasanbon.plugins.admin.binder.binder.get_package_repos():
            print r.name
    
    def clone(self, args):
        #self.parser.add_option('-r', '--remove', help='Remove All Files (default=False)', default=False, action='store_true', dest='remove_flag')
        options, argv = self.parse_args(args[:], self._list_package_repos)
        verbose = options.verbose_flag
        #remove = options.remove_flag

        wasanbon.arg_check(argv, 4)
        repo_name = argv[3]
        package_repo = wasanbon.plugins.admin.binder.binder.get_package_repo(repo_name)
        if package_repo is None:
            raise wasanbon.RepositoryNotFoundException()

        pack_name = None
        if pack_name is None:
            pack_name = package_repo.basename
        import package
        try:
            p = package.get_package(pack_name, verbose=verbose)
            raise wasanbon.PackageAlreadyExistsException
        except wasanbon.PackageNotFoundException, ex:
            pass

        print '# Cloning package %s' % package_repo
        #import wasanbon
        wasanbon.plugins.admin.git.git.git_command(['clone', package_repo.url, pack_name], verbose=verbose)
        #import package
        package.create_package(pack_name, verbose=verbose, force_create=True, overwrite=False)

        pack = package.get_package(pack_name, verbose=verbose)
        package.validate_package(pack, verbose=verbose, autofix=True, ext_only=True)

        
