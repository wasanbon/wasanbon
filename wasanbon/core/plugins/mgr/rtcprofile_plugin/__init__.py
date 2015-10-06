import os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'mgr.repository', 'admin.rtcprofile', 'mgr.imaging']

    def _print_rtcs(self, args):
        pack = admin.package.get_package_from_path(os.getcwd())
        rtcs = admin.rtc.get_rtcs_from_package(pack)
        for r in rtcs:
            print r.rtcprofile.basicInfo.name

    @manifest
    def dump(self, argv):
        """ Dump RTCProfile to STDOUT
        $ mgr.py rtcprofile dump [RTC_NAME] """
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)
        
        pack = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(pack, argv[3])

        
        #path = rtc.get_rtc_profile_path()
        #with open(path, 'r') as f:
        #    sys.stdout.write(f.read())
        sys.stdout.write(admin.rtcprofile.tostring(rtc.rtcprofile, pretty_print=True))        

        return 0

    @manifest
    def html(self, argv):
        """ Dump HTML Document to STDOUT
        $ mgr.py rtcprofile html [RTC_NAME] """
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)

        rtc_name = argv[3]
        pack = admin.package.get_package_from_path(os.getcwd())
        rtc = admin.rtc.get_rtc_from_package(pack, rtc_name)
        
        html = self.get_html(rtc)
        print html
        return 0

    def get_html(self, rtc):
        repo = mgr.repository.get_registered_repository_from_rtc(rtc)
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        template_path = os.path.join(__path__[0], 'template')
        cwd = os.getcwd()
        os.chdir(template_path)
        tpl = env.get_template('page_template.html')
        os.chdir(cwd)
        info = {'name' : rtc.rtcprofile.basicInfo.name,
                'repo_name' : repo.name,
                'url' : repo.url.strip(),
                'platform' : repo.platform}
        html = tpl.render({'rtc': rtc.rtcprofile, 'info':info})
        return html

    @manifest
    def image(self, argv):
        """ Create image from RTCProfile. This will saved to ${path_to_package}/images/[RTC_NAME].jpg
        $ mgr.py rtcprofile image [RTC_NAME] """
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)
        
        package = admin.package.get_package_from_path(os.getcwd())
        image_path = os.path.join(package.path, 'image')
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        rtc = admin.rtc.get_rtc_from_package(package, argv[3])
        filepath = os.path.join(image_path, rtc.rtcprofile.basicInfo.name + '.jpg')
        im = mgr.imaging.get_image(rtc.rtcprofile)
        im.save(filepath)
        return 0


    @manifest
    def cat(self, args):
        self.parser.add_option('-f', '--file', help='RTCProfile filename (default="RTC.xml")', default='RTC.xml', dest='filename', action='store', type='string')
        self.parser.add_option('-i', '--inputfile', help='Input from RTCProfile filename (default=None)', default=None, dest='inputfile', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        filename = options.filename
        inputfile = options.inputfile
        if inputfile:
            sys.stdout.write('## Input File is %s\n' % inputfile)
            wasanbon.arg_check(argv, 4)
        else:
            wasanbon.arg_check(argv, 5)
        rtc_name = argv[3]
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        filepath = os.path.join(rtc.path, filename)

        if os.path.isfile(filepath):
            file = filepath + wasanbon.timestampstr()
            os.rename(filepath, file)

        if inputfile:
            inputData = open(inputfile, 'r').read()
        else:
            inputData = argv[4]
        fout = open(filepath, 'w')
        fout.write(inputData)
        fout.close()

        sys.stdout.write('Success\n')
        return 0


