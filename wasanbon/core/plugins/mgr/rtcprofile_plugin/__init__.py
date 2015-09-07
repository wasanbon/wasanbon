import os, sys

import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest


class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.package', 'admin.rtc', 'mgr.repository']

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

        path = rtc.get_rtc_profile_path()
        with open(path, 'r') as f:
            sys.stdout.write(f.read())

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
        im = self.get_image(rtc.rtcprofile)
        im.save(filepath)
        return 0

    def get_image(self, rtcprofile):
        return create_image(rtcprofile)

    @manifest
    def cat(self, args):
        self.parser.add_option('-f', '--file', help='RTCProfile filename (default="RTC.xml")', default='RTC.xml', dest='filename', action='store', type='string')
        options, argv = self.parse_args(args[:])
        verbose = options.verbose_flag
        filename = options.filename
        wasanbon.arg_check(argv, 5)
        rtc_name = argv[3]
        package = admin.package.get_package_from_path(os.getcwd(), verbose=verbose)
        rtc = admin.rtc.get_rtc_from_package(package, rtc_name, verbose=verbose)
        filepath = os.path.join(rtc.path, filename)

        if os.path.isfile(filepath):
            file = filepath + wasanbon.timestampstr()
            os.rename(filepath, file)

        fout = open(filepath, 'w')
        fout.write(argv[4])
        fout.close()

        sys.stdout.write('Success\n')
        return 0






def create_image(rtcprof):
    from PIL import Image, ImageDraw, ImageFont

    len_svc_intf = 0
    for s in rtcprof.serviceports:
        len_svc_intf = len_svc_intf + len(s.serviceInterfaces)
    num_rightside_port = len(rtcprof.outports) + len(rtcprof.serviceports) + len_svc_intf
    num_leftside_port = len(rtcprof.inports)
    if num_rightside_port > num_leftside_port:
        num_port = num_rightside_port
    else:
        num_port = num_leftside_port
        pass

    top_margin = 20
    bottom_margin = 40
    top_bottom_margin = 20
    port_height = 20
    port_margin = 20
    num_margin = num_port -1
    if num_margin < 0: num_margin = 0
    img_height = num_port * port_height + num_margin * port_margin + top_bottom_margin *2 + top_margin + bottom_margin
    img_width  = 800

    fill_color = (20, 20, 255, 255)
    outline_color = (15, 15, 30, 255)
    text_color = (15, 15, 30, 255)
    line_color = (15, 15, 30, 255)

    if sys.platform == 'win32':
        font_path = "C:\\Windows\\Fonts\\cour.ttf"
        text_font = ImageFont.truetype(font_path, 14)
        title_font = ImageFont.truetype(font_path, 20)
    else:
        text_font = ImageFont.truetype("/Library/Fonts/Courier New.ttf", 14)
        title_font = ImageFont.truetype("/Library/Fonts/Courier New.ttf", 20)
    im = Image.new('RGBA', (img_width, img_height), (228, 212, 162, 0))
    draw = ImageDraw.Draw(im)
    
    rtc_height = num_port * port_height + num_margin * port_margin + top_bottom_margin *2
    rtc_width  = 100

    rtc_topleft = ( (img_width - rtc_width) / 2, top_margin)
    rtc_rightbottom = (rtc_topleft[0] + rtc_width, top_margin + rtc_height)
    draw.rectangle((rtc_topleft, rtc_rightbottom), fill=fill_color, outline=outline_color)

    text = rtcprof.name
    width, height = draw.textsize(text, font=title_font)
    text_offset = (img_width/2 - width/2, top_margin + rtc_height + height/2)
    draw.text(text_offset, text, font=title_font, fill=text_color)
    
    outport_polygon = ((-port_height/2, -port_height/2), (+port_height/2, -port_height/2),
                       (port_height/2+port_height/2, 0), (port_height/2, port_height/2),
                       (-port_height/2, port_height/2), (-port_height/2, -port_height/2))
        
    for i, p in enumerate(rtcprof.outports):
        offset = (img_width/2 + rtc_width/2, top_margin + top_bottom_margin + (port_height+port_margin)*i + port_height/2)
        port_polygon = []
        for point in outport_polygon:
            port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
        draw.polygon(port_polygon, fill=fill_color, outline=outline_color)
        
        text = p.name + '(' + p.type + ')'
        text_pos = (offset[0] + port_height/2, offset[1] - port_height*1.5)
        draw.text(text_pos, text, fill=text_color, font=text_font)


    svcport_polygon = ((-port_height/2, -port_height/2), (+port_height/2+port_height/2, -port_height/2),
                       (+port_height/2+port_height/2, port_height/2),
                       (-port_height/2, port_height/2), (-port_height/2, -port_height/2))
        
    len_svc = 0
    i = len(rtcprof.outports) - 1
    for j, s in enumerate(rtcprof.serviceports):
        i = i + 1
        offset = (img_width/2 + rtc_width/2, top_margin + top_bottom_margin + (port_height+port_margin)*i + port_height/2)

        for k, f in enumerate(s.serviceInterfaces):
            i = i + 1
            start = (offset[0] + port_height/2, offset[1])
            intf_offset = (img_width/2 + rtc_width/2 + port_height/2 * 5, top_margin + top_bottom_margin + (port_height+port_margin)*i + port_height/2)
            pivot0 = (start[0] + port_height/2 *2, start[1])
            pivot1 = (pivot0[0], intf_offset[1])
            draw.line((start, pivot0), fill=outline_color)
            draw.line((pivot0, pivot1), fill=outline_color)
            draw.line((pivot1, intf_offset), fill=outline_color)

            bbox = ((intf_offset[0], intf_offset[1]-port_height/2),
                    (intf_offset[0] + port_height, intf_offset[1]+port_height/2))

            if f.direction == 'Provided':
                draw.ellipse(bbox, outline=outline_color)
            else:
                draw.arc(bbox, 90, 270, fill=outline_color)

            text = f.type
            text_pos = (intf_offset[0] + port_height/2, intf_offset[1] - port_height*1.5)
            draw.text(text_pos, text, fill=text_color, font=text_font)
        
            
        len_svc = len_svc + len(s.serviceInterfaces)


        port_polygon = []
        for point in svcport_polygon:
            port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
        draw.polygon(port_polygon, fill=fill_color, outline=outline_color)


        text = s.name
        text_pos = (offset[0] + port_height/2, offset[1] - port_height*1.5)
        draw.text(text_pos, text, fill=text_color, font=text_font)



    inport_polygon = ((-port_height/2-port_height/2, -port_height/2), (+port_height/2, -port_height/2),
                      (+port_height/2, +port_height/2),
                       (-port_height/2-port_height/2, port_height/2),
                      (-port_height/2-port_height/2+port_height/2, 0),
                      (-port_height/2-port_height/2, -port_height/2))
        
    for i, p in enumerate(rtcprof.inports):
        offset = (img_width/2 - rtc_width/2, top_margin + top_bottom_margin + (port_height+port_margin)*i + port_height/2)
        port_polygon = []
        for point in inport_polygon:
            port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
        draw.polygon(port_polygon, fill=fill_color, outline=outline_color)

        text = p.name + '(' + p.type + ')'
        width, height = draw.textsize(text, font=text_font)
        text_pos = (offset[0] - port_height/2 - width, offset[1] - port_height*1.5)
        draw.text(text_pos, text, fill=text_color, font=text_font)
    
    return im

