import sys, os
import wasanbon
from wasanbon import util
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.binder', 'admin.package', 'admin.rtc', 'admin.repository']

    def _print_alternatives_for_package(self, argv):
        argv = [arg for arg in argv if not arg.startswith('-')]
        if len(argv) == 3:
            self._print_binders(argv)
    
    def _print_alternatives(self, argv):
        argv = [arg for arg in argv if not arg.startswith('-')]
        if len(argv) == 3:
            self._print_binders(argv)
        else:
            self._print_rtcs(argv)

    def _print_binders(self, argv):
        binders = admin.binder.get_binders()
        for b in binders:
            print b.owner

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(pack)
        for r in rtcs:
            print r.rtcprofile.basicInfo.name


        
    @manifest
    def list(self, argv):
        return admin.binder.list(argv)

    @manifest
    def add_rtc(self, argv):
        """ Add RTC information to binder
        $ mgr.py binder add_rtc $BINDER_NAME $RTC_NAME
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 5)
        binder_name = argv[3]
        rtc_name = argv[4]
        sys.stdout.write('# Information of RTC (%s) will be added to %s binder\n' % (rtc_name, binder_name))
        
        binder = admin.binder.get_binder(binder_name, verbose=verbose)
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        global filename
        filename= None
        rtcs = [rtc_.name for rtc_ in binder.rtcs]
        if rtc_name in rtcs:
            sys.stdout.write('# This binder have the same RTC information.\n')

        else:
            if filename is None:
                def choice_command(ans):
                    global filename
                    filename = os.path.join(binder.rtcs_path, binder.rtc_files[ans])
                    return -1
                util.choice(binder.rtc_files, choice_command, 'Select RTC repository file')
            else:
                if not filename in binder.rtcs_files:
                    sys.stdout.write('# File %s is not found.\n' % filenmae)
                    filename = os.path.join(binder.rtcs_path, filename)
                    return -1
            print filename
            text = open(filename, 'r').read()
            #os.rename(filename, filename + wasanbon.timestampstr())
            #import yaml
            #repo_dic = yaml.load(open(filename, 'w'))

            text = text + """
%s :
  description : "%s"
  type : git
  url : '%s'
  platform : [%s]
""" % (repo.name, rtc.rtcprofile.basicInfo.doc.description, repo.url.strip(), wasanbon.platform())
            print text
            os.rename(filename, filename + wasanbon.timestampstr())
            open(filename, 'w').write(text)
            
            
        return 0


    @manifest
    def add_package(self, argv):
        """ Add This package information to binder
        $ mgr.py binder add_package $BINDER_NAME
        """
        self.parser.add_option('-f', '--force', help='Force option (default=False)', default=False, action='store_true', dest='force_flag')
        options, argv = self.parse_args(argv[:], self._print_alternatives_for_package)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)
        binder_name = argv[3]
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        package_name = package.name
        sys.stdout.write('# Information of Package will be added to %s binder\n' % (binder_name))
        
        binder = admin.binder.get_binder(binder_name, verbose=verbose)

        repo = admin.repository.get_repository_from_path(package.path, verbose=verbose)
        global filename
        filename= None
        packages = [package_.name for package_ in binder.packages]
        if package_name in packages:
            sys.stdout.write('# This binder have the same Package information.\n')
            
        else:
            if filename is None:
                def choice_command(ans):
                    global filename
                    filename = os.path.join(binder.packages_path, binder.package_files[ans])
                    return -1
                util.choice(binder.package_files, choice_command, 'Select RTC repository file')
            else:
                if not filename in binder.package_files:
                    sys.stdout.write('# File %s is not found.\n' % filenmae)
                    filename = os.path.join(binder.packages_path, filename)
                    return -1
            print filename
            text = open(filename, 'r').read()
            #os.rename(filename, filename + wasanbon.timestampstr())
            #import yaml
            #repo_dic = yaml.load(open(filename, 'w'))

            text = text + """
%s :
  description : "%s"
  type : git
  url : '%s'
  platform : [%s]
""" % (repo.name, package.description, repo.url.strip(), wasanbon.platform())
            print text
            os.rename(filename, filename + wasanbon.timestampstr())
            open(filename, 'w').write(text)
            
            
        return 0
