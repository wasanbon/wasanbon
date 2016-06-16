import os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'mgr.repository', 'admin.rtcprofile', 'mgr.imaging', 'admin.repository']

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
        self.parser.add_option('-i', '--image', help="Output HTML document with Image link (default='False')", default=False, action="store_true", dest="image_flag")
        self.parser.add_option('-s', '--save', help="Save to html file (default='False')", default=False, action="store_true", dest="save_flag")
        self.parser.add_option('-c', '--css', help="Add style file include. Use with document option (-d) (default='None')", default=None, action="store", dest="css_name")
        self.parser.add_option('-d', '--doc', help="Generate html as stand alone document. (default='False')", default=False, action="store_true", dest="doc_flag")
        self.parser.add_option('-x', '--index', help='Add index.html file. Use with all argument. (default="False")', default=False, action="store_true", dest="index_flag")
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option
        image_flag = options.image_flag
        save_flag = options.save_flag
        css_name = options.css_name
        doc_flag = options.doc_flag
        index_flag = options.index_flag

        wasanbon.arg_check(argv, 4)

        package = admin.package.get_package_from_path(os.getcwd())

        if not css_name is None and not doc_flag:
            sys.stdout.write('# Error. -c option must be used with -d option\n')
            return -1

        if argv[3] == 'all':
            rtc_names = [rtc.rtcprofile.basicInfo.name for rtc in admin.rtc.get_rtcs_from_package(package)]
        else:
            if index_flag:
                sys.stdout.write('# Error. Use -x option with all argument.\n')
                return -1

            rtc_names = [argv[3]]
        for rtc_name in rtc_names:

            rtc = admin.rtc.get_rtc_from_package(package, rtc_name)
        
            html = self.get_html(rtc, image_flag)
            if doc_flag:
                if not css_name is None:
                    css_line = '<link rel="stylesheet" type="text/css" href="%s">' % css_name
                else:
                    css_line = ''
                html = '''<header>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>%s</title>
%s
</header>
<body>
%s
</body>''' % (rtc_name, css_line, html)
            if argv[3] == 'all' or save_flag:
                html_path = os.path.join(package.path, rtc_name + '.html')
                f = open(html_path, 'w')
                f.write(html)
                f.close()
                pass
            else:
                print html

            if image_flag:
                image_path = os.path.join(package.path, 'image')
                if not os.path.isdir(image_path):
                    os.mkdir(image_path)
                filepath = os.path.join(image_path, rtc.rtcprofile.basicInfo.name + '.png')
                im = mgr.imaging.get_image(rtc.rtcprofile)
                im.save(filepath)

        return 0

    def get_html(self, rtc, with_image=False, no_repo=True):
        repo = mgr.repository.get_registered_repository_from_rtc(rtc)
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        template_path = os.path.join(__path__[0], 'template')
        cwd = os.getcwd()
        os.chdir(template_path)
        tpl = env.get_template('page_template.html')
        os.chdir(cwd)

        if getattr(repo, 'url', None) == None:
            url = ''
        else:
            url = repo.url.strip()
        if repo:
            info = {'name' : rtc.rtcprofile.basicInfo.name,
                    'repo_name' : repo.name,
                    'url' : url,
                    'platform' : repo.platform}
        else:
            repo = admin.repository.get_repository_from_rtc(rtc, verbose=False)
            info = {'name' : rtc.rtcprofile.basicInfo.name,
                    'repo_name' : '',
                    'url' : url,
                    'platform' : wasanbon.platform}
            
        html = tpl.render({'rtc': rtc.rtcprofile, 'info':info})
        
        if with_image:
            line = '<img src="image/%s.png" />' % rtc.rtcprofile.basicInfo.name
            return html.replace("[post_thumbnail size='full']", line)
        return html

    @manifest
    def image(self, argv):
        """ Create image from RTCProfile. This will saved to ${path_to_package}/images/[RTC_NAME].png
        $ mgr.py rtcprofile image [RTC_NAME] """
        options, argv = self.parse_args(argv[:], self._print_rtcs)
        verbose = options.verbose_flag # This is default option

        wasanbon.arg_check(argv, 4)
        
        package = admin.package.get_package_from_path(os.getcwd())
        image_path = os.path.join(package.path, 'image')
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        rtc = admin.rtc.get_rtc_from_package(package, argv[3])
        filepath = os.path.join(image_path, rtc.rtcprofile.basicInfo.name + '.png')
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


