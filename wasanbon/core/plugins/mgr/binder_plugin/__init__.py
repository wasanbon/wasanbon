import sys
import os
import wasanbon
from wasanbon import util
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):
    """ Binder (Collection of components) management Plugin. """

    def __init__(self):
        # PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.binder', 'admin.package', 'admin.rtc', 'admin.repository', 'admin.git']

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
            print(b.owner)

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(pack)
        for r in rtcs:
            print(r.rtcprofile.basicInfo.name)

    @manifest
    def list(self, argv):
        """ Show binder list
        $ ./mgr.py binder list
        """
        return admin.binder.list(argv)

    @manifest
    def add_rtc(self, argv):
        """ Add RTC information to binder
        $ ./mgr.py binder add_rtc <BINDER_NAME> <RTC_NAME>
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives)
        verbose = options.verbose_flag  # This is default option

        wasanbon.arg_check(argv, 5)
        binder_name = argv[3]
        rtc_name = argv[4]
        sys.stdout.write('# Information of RTC (%s) will be added to %s binder\n' % (rtc_name, binder_name))

        binder = admin.binder.get_binder(binder_name, verbose=verbose)
        if binder is None:
            sys.stdout.write('# Binder(%s) is not found. Use wasanbon-admin.py binder create command.\n' % binder_name)
            return -1

        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        global filename
        filename = None
        rtcs = [rtc_.name for rtc_ in binder.rtcs]
        if rtc_name in rtcs:
            sys.stdout.write('# This binder have the same RTC information.\n')

        else:
            def choice_command(ans):
                global filename
                filename = os.path.join(binder.rtcs_path, binder.rtc_files[ans])
                return -1
            util.choice(binder.rtc_files, choice_command, 'Select RTC repository file')
            if filename == None:
                return -1

            p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'], path=rtc._path)
            output, _ = p_branch.communicate()
            branch = output.decode(encoding="utf-8").strip()

            text = open(filename, 'r').read()
            text = text + """
%s :
  description : '%s'
  type : git
  url : '%s'
  platform :
    %s : %s
""" % (repo.name, rtc.rtcprofile.basicInfo.doc.description, repo.url.strip().decode(encoding="utf-8"), wasanbon.platform(), branch)
            print(text)
            os.rename(filename, filename + wasanbon.timestampstr())
            open(filename, 'w').write(text)
            sys.stdout.write('## Success. \n')

        return 0

    @manifest
    def add_package(self, argv):
        """ Add This package information to binder
        $ ./mgr.py binder add_package <BINDER_NAME>
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives_for_package)
        verbose = options.verbose_flag  # This is default option

        wasanbon.arg_check(argv, 4)
        binder_name = argv[3]
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        package_name = package.name
        sys.stdout.write('# Information of Package will be added to %s binder\n' % (binder_name))

        binder = admin.binder.get_binder(binder_name, verbose=verbose)
        if binder is None:
            sys.stdout.write('# Binder(%s) is not found. Use wasanbon-admin.py binder create command. \n' % binder_name)
            return -1

        repo = admin.repository.get_repository_from_path(package.path, verbose=verbose)
        if repo is None:
            sys.stdout.write('# Repository(%s) is not found. Use mgr.py admin git_init/remote_create command. \n' % package.path)
            return -1

        global filename
        filename = None
        packages = [package_.name for package_ in binder.packages]
        if package_name in packages:
            sys.stdout.write('# This binder have the same Package information.\n')

        else:
            def choice_command(ans):
                global filename
                filename = os.path.join(binder.packages_path, binder.package_files[ans])
                return -1
            util.choice(binder.package_files, choice_command, 'Select RTC repository file')
            if filename is None:
                return -1

            p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
            output, _ = p_branch.communicate()
            branch = output.decode(encoding="utf-8").strip()

            text = open(filename, 'r').read()
            text = text + """
%s :
  description : '%s'
  type : git
  url : '%s'
  platform :
    %s : %s
""" % (repo.name, package.description, repo.url.strip().decode(encoding="utf-8"), wasanbon.platform(), branch)
            print(text)
            os.rename(filename, filename + wasanbon.timestampstr())
            open(filename, 'w').write(text)
            sys.stdout.write('## Success. \n')

        return 0

    @manifest
    def update_rtc(self, argv):
        """ Update RTC information to binder
        $ ./mgr.py binder update_rtc <BINDER_NAME> <RTC_NAME>
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives_for_package)
        verbose = options.verbose_flag  # This is default option

        wasanbon.arg_check(argv, 5)
        binder_name = argv[3]
        rtc_name = argv[4]

        binder = admin.binder.get_binder(binder_name, verbose=verbose)
        if binder is None:
            sys.stdout.write('# Binder(%s) is not found. Use wasanbon-admin.py binder create command. \n' % binder_name)
            return -1

        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        repo = admin.repository.get_repository_from_rtc(rtc, verbose=verbose)
        global filename
        filename = None
        rtcs = [rtc_.name for rtc_ in binder.rtcs]
        if not rtc_name in rtcs:
            sys.stdout.write('# The same RTC information is not found.\n')
        else:
            rtc_yaml = None
            rtc_filepath = None
            for rtc_file in binder.rtc_files:
                import yaml
                filepath = os.path.join(binder._path, 'rtcs', rtc_file)
                tmp_yaml = yaml.safe_load(open(filepath, 'r'))
                if rtc_name in tmp_yaml:
                    sys.stdout.write('# Found package(%s) in File(%s).\n' % (rtc_name, rtc_file))
                    rtc_filepath = filepath
                    rtc_yaml = tmp_yaml
                    break
            if rtc_filepath is None:
                sys.stdout.write('# Binder is not found. \n')
                return -1

            sys.stdout.write('# Information of RTC (%s) will be update %s binder\n' % (rtc_name, binder_name))
            platform = rtc_yaml[rtc_name]['platform']
            if type(platform) is list:
                platform = {}

            p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'], path=rtc._path)
            output, stderr = p_branch.communicate()
            branch = output.decode(encoding="utf-8").strip()
            platform[wasanbon.platform()] = branch
            rtc_yaml[rtc_name]['description'] = rtc.rtcprofile.basicInfo.doc.description
            rtc_yaml[rtc_name]['type'] = 'git'
            rtc_yaml[rtc_name]['url'] = repo.url.strip().decode(encoding="utf-8")
            rtc_yaml[rtc_name]['platform'] = platform

            yaml.safe_dump(rtc_yaml, open(rtc_filepath, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
            sys.stdout.write('## Success. \n')

        return 0

    @manifest
    def update_package(self, argv):
        """ Update this package information to binder
        $ ./mgr.py binder update_package <BINDER_NAME>
        """
        options, argv = self.parse_args(argv[:], self._print_alternatives_for_package)
        verbose = options.verbose_flag  # This is default option

        wasanbon.arg_check(argv, 4)
        binder_name = argv[3]
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        package_name = package.name

        binder = admin.binder.get_binder(binder_name, verbose=verbose)
        if binder is None:
            sys.stdout.write('# Binder(%s) is not found. Use wasanbon-admin.py binder create command. \n' % binder_name)
            return -1

        repo = admin.repository.get_repository_from_path(package.path, verbose=verbose)
        if repo is None:
            sys.stdout.write('# Repository(%s) is not found. Use mgr.py admin git_init/remote_create command. \n' % package.path)
            return -1

        packages = [package_.name for package_ in binder.packages]
        if not package_name in packages:
            sys.stdout.write('# The same Package information is not found.\n')

        else:
            packages_yaml = None
            packages_filepath = None
            for package_file in binder.package_files:
                import yaml
                filepath = os.path.join(binder._path, 'packages', package_file)
                tmp_yaml = yaml.safe_load(open(filepath, 'r'))
                if package_name in tmp_yaml:
                    sys.stdout.write('# Found package(%s) in File(%s).\n' % (package_name, package_file))
                    packages_filepath = filepath
                    packages_yaml = tmp_yaml
                    break
            if packages_filepath is None:
                sys.stdout.write('# Binder is not found. \n')
                return -1

            sys.stdout.write('# Information of Package will be update %s binder\n' % (binder_name))
            platform = packages_yaml[package_name]['platform']
            if type(platform) is list:
                platform = {}

            p_branch = admin.git.git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
            output, stderr = p_branch.communicate()
            branch = output.decode(encoding="utf-8").strip()
            platform[wasanbon.platform()] = branch
            packages_yaml[package_name]['description'] = package.description
            packages_yaml[package_name]['type'] = 'git'
            packages_yaml[package_name]['url'] = repo.url.strip().decode(encoding="utf-8")
            packages_yaml[package_name]['platform'] = platform

            yaml.safe_dump(packages_yaml, open(packages_filepath, 'w'), encoding='utf8', allow_unicode=True, default_flow_style=False)
            sys.stdout.write('## Success. \n')

        return 0
