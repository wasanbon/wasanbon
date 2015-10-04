import wasanbon, os, sys
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'mgr.imaging']

    def _print_system_profiles(self, args):
        package = admin.package.get_package_from_path(os.getcwd(), verbose=False)
        for f in os.listdir(package.get_systempath()):
            if f.endswith('.xml'): sys.stdout.write('%s\n' % f)

    @manifest
    def dump(self, args):
        self.parser.add_option('-f', '--file', help='Build System with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        options, argv = self.parse_args(args[:], self._print_system_profiles)
        systemfile = options.systemfile
        verbose = options.verbose_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)

        if systemfile is None:
            systemfile = package.default_system_filepath
        else:
            systemfile = os.path.join(package.get_systempath(), systemfile)

        if not os.path.isfile(systemfile):
            print '# File Not Found.'
            return -1

        for line in open(systemfile, 'r'):
            sys.stdout.write(line)
        return 0

    @manifest
    def cat(self, args):
        self.parser.add_option('-f', '--file', help='Build System with Specific RTSProfile (must be placed in system_dir', default=None, dest='systemfile', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        systemfile = options.systemfile
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        if systemfile is None:

            systemfile = package.default_system_filepath
        else:
            systemfile = os.path.join(package.get_systempath(), systemfile)

        if os.path.isfile(systemfile):
            newfile = systemfile + wasanbon.timestampstr()
            os.rename(systemfile, newfile)

        fout = open(systemfile, 'w')
        fout.write(argv[3])
        fout.close()

        sys.stdout.write('Success\n')
        return 0


    @manifest
    def copy(self, args):
        self.parser.add_option('-f', '--force', help='Force Delete without yes/no option (default=False)', default=False, dest='force_flag', action='store_true')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        force = options.force_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        wasanbon.arg_check(argv, 5)
        srcfile = argv[3]
        dstfile = argv[4]
        srcfile_relpath = os.path.join(package.get_systempath(fullpath=False), srcfile)
        srcfile_fullpath = os.path.join(package.get_systempath(), srcfile)
        if not os.path.isfile(srcfile_fullpath):
            sys.stdout.write('## No System File exists.\n')
            return -1

        dstfile_fullpath = os.path.join(package.get_systempath(), dstfile)
        if os.path.isfile(dstfile_fullpath):
            if not force:
                from wasanbon import util
                if util.no_yes('# Overwrite? (%s):' % systemfile_relpath) == 'no':
                    sys.stdout.write('## Aborted.\n')
                    return 0
            newfile = dstfile_fullpath + wasanbon.timestampstr()
            os.rename(dstfile_fullpath, newfile)
        
        import shutil
        shutil.copyfile(srcfile_fullpath, dstfile_fullpath)
        sys.stdout.write('## Success\n')
        return 0
        

    @manifest
    def delete(self, args):
        self.parser.add_option('-f', '--force', help='Force Delete without yes/no option (default=False)', default=False, dest='force_flag', action='store_true')
        options, argv = self.parse_args(args[:], self._print_system_profiles)
        verbose = options.verbose_flag
        force = options.force_flag
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        systemfile = argv[3]
        systemfile_relpath = os.path.join(package.get_systempath(fullpath=False), systemfile)
        systemfile_fullpath = os.path.join(package.get_systempath(), systemfile)
        if not os.path.isfile(systemfile_fullpath):
            sys.stdout.write('## No System File exists.\n')
            return -1

        if not force:
            from wasanbon import util
            if util.no_yes('# Delete? (%s):' % systemfile_relpath) == 'no':
                sys.stdout.write('## Aborted.\n')
                return 0
        
        newfile = systemfile_fullpath + wasanbon.timestampstr()
        os.rename(systemfile_fullpath, newfile)

        sys.stdout.write('## Success\n')
        return 0

    @manifest
    def image(self, args):
        """ Create image from RTSProfile. This will saved to ${path_to_package}/images/[RTSP_NAME].jpg
        $ mgr.py rtsprofile image [RTSP_NAME] """
        options, argv = self.parse_args(args[:], self._print_system_profiles)
        verbose = options.verbose_flag # This is default option
        wasanbon.arg_check(argv, 4)
        package = admin.package.get_package_from_path(os.getcwd())
        systemfile = argv[3]
        systemfile_relpath = os.path.join(package.get_systempath(fullpath=False), systemfile)
        systemfile_fullpath = os.path.join(package.get_systempath(), systemfile)
        if not os.path.isfile(systemfile_fullpath):
            sys.stdout.write('## No System File exists.\n')
            return -1

        image_path = os.path.join(package.path, 'image')
        if not os.path.isdir(image_path):
            os.mkdir(image_path)

        from rtsprofile.rts_profile import RtsProfile
        rtsp = RtsProfile(open(systemfile_fullpath, 'r').read())

        im = mgr.imaging.get_rtsp_image(package, rtsp, port_height=10, port_text_font=10)
        filepath = os.path.join(image_path, argv[3][:-4] + '.png')
        #im = self.get_image()
        im.save(filepath)
        return 0
        
