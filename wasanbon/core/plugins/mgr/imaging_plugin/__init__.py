import os, sys
import wasanbon
from wasanbon.core.plugins import PluginFunction, manifest

class Plugin(PluginFunction):

    def __init__(self):
        #PluginFunction.__init__(self)
        super(Plugin, self).__init__()
        pass

    def depends(self):
        return ['admin.environment', 'admin.rtc']

    def get_num_ports(self, rtcprof):
        len_pro_svc_intf = 0
        len_req_svc_intf = 0
        for s in rtcprof.serviceports:
            flag = False
            for f in s.serviceInterfaces:
                if f.direction == 'Provided':
                    flag = True
            if flag:
                len_pro_svc_intf = len_pro_svc_intf + len(s.serviceInterfaces) + 1
            else:
                len_req_svc_intf = len_req_svc_intf + len(s.serviceInterfaces) + 1
            pass
        num_rightside_port = len(rtcprof.outports) + len_pro_svc_intf
        num_leftside_port = len(rtcprof.inports) + len_req_svc_intf
        if num_rightside_port > num_leftside_port:
            num_port = num_rightside_port
        else:
            num_port = num_leftside_port
            pass
        return num_port, num_rightside_port, num_leftside_port

    def get_image_height(self, rtcprof, port_height = 20):
        (num_port, num_rightside_port, num_leftside_port) = self.get_num_ports(rtcprof)
        top_margin = port_height
        bottom_margin = port_height * 3
        top_bottom_margin = port_height
        port_margin = port_height
        num_margin = num_port -1
        if num_margin < 0: num_margin = 0
        img_height = num_port * port_height + num_margin * port_margin + top_bottom_margin * 2 + top_margin + bottom_margin
        img_width  = 800
        return img_height

    def get_image(self, rtcprof, port_height=20, 
                  fill_color=(20,20,255,255), line_color=(15,15,30,255), background_color=(228,212,162,0)):
        from PIL import Image
        img_width = 800
        img_height = self.get_image_height(rtcprof, port_height)
        img_height = img_height + port_height # for text

        im = Image.new('RGBA', (img_width, img_height), background_color)
        top_margin = port_height
        rtc_width  = port_height * 5
        rtc_topleft = ( (img_width - rtc_width) / 2, top_margin)
        
        self.write_rtc_image(im, rtcprof, rtc_topleft, port_height, line_color, fill_color)
        return im

    def write_rtc_image(self, im, rtcprof, rtc_topleft, port_height, line_color, fill_color, port_text_font=14, title_text_font=20):
        from PIL import Image, ImageDraw, ImageFont
        img_width = im.width
        draw = ImageDraw.Draw(im)

        (num_port, num_rightside_port, num_leftside_port) = self.get_num_ports(rtcprof)
        num_margin = num_port -1
        if num_margin < 0: num_margin = 0

        port_margin = port_height
        top_margin = port_height
        top_bottom_margin = port_height
        rtc_height = num_port * port_height + num_margin * port_margin + top_bottom_margin *2
        rtc_width  = port_height * 5
        rtc_rightbottom = (rtc_topleft[0] + rtc_width, rtc_topleft[1] + top_margin + rtc_height)

        draw.rectangle((rtc_topleft, rtc_rightbottom), fill=fill_color, outline=line_color)

        # For FONT
        text_color = line_color
        if sys.platform == 'win32':
            font_path = "C:\\Windows\\Fonts\\cour.ttf"
        else:
            font_path = "/Library/Fonts/Courier New.ttf"
            pass
        text_font = ImageFont.truetype(font_path, port_text_font)
        title_font = ImageFont.truetype(font_path, title_text_font)
        
        text = rtcprof.name
        width, height = draw.textsize(text, font=title_font)
        text_offset = (rtc_topleft[0] + rtc_width/2 - width/2, rtc_topleft[1] + top_margin + rtc_height + height/2)
        draw.text(text_offset, text, font=title_font, fill=text_color)
        
        outport_polygon = ((-port_height/2, -port_height/2), (+port_height/2, -port_height/2),
                           (port_height/2+port_height/2, 0), (port_height/2, port_height/2),
                           (-port_height/2, port_height/2), (-port_height/2, -port_height/2))
        
        for i, p in enumerate(rtcprof.outports):
            offset = (rtc_topleft[0] + rtc_width, rtc_topleft[1] +top_bottom_margin + (port_height+port_margin)*i + port_height)
            port_polygon = []
            for point in outport_polygon:
                port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
                pass
            draw.polygon(port_polygon, fill=fill_color, outline=line_color)
            
            text = p.name + '(' + p.type + ')'
            text_pos = (offset[0] + port_height/2, offset[1] - port_height*1.5)
            draw.text(text_pos, text, fill=text_color, font=text_font)
            pass

        svcport_polygon = ((-port_height/2, -port_height/2), (+port_height/2+port_height/2, -port_height/2),
                           (+port_height/2+port_height/2, port_height/2),
                           (-port_height/2, port_height/2), (-port_height/2, -port_height/2))
        
        len_svc = 0
        pi = len(rtcprof.outports) - 1
        for j, s in enumerate(rtcprof.serviceports):
            flag = False
            for k, f in enumerate(s.serviceInterfaces):
                if f.direction == 'Provided':
                    flag = True

            if not flag:
                continue
            pi = pi + 1
            offset = (rtc_topleft[0] + rtc_width, rtc_topleft[1] + top_bottom_margin + (port_height+port_margin)*pi + port_height)
            
            for k, f in enumerate(s.serviceInterfaces):

                pi = pi + 1
                start = (offset[0] + port_height/2, offset[1])
                intf_offset = (rtc_topleft[0] + rtc_width + port_height/2 * 5, rtc_topleft[1] + top_bottom_margin + (port_height+port_margin)*pi + port_height)
                pivot0 = (start[0] + port_height/2 *2, start[1])
                pivot1 = (pivot0[0], intf_offset[1])
                draw.line((start, pivot0), fill=line_color)
                draw.line((pivot0, pivot1), fill=line_color)
                draw.line((pivot1, intf_offset), fill=line_color)
                
                bbox = ((intf_offset[0], intf_offset[1]-port_height/2),
                        (intf_offset[0] + port_height, intf_offset[1]+port_height/2))
                
                if f.direction == 'Provided':
                    draw.ellipse(bbox, outline=line_color)
                else:
                    draw.arc(bbox, 90, 270, fill=line_color)
                    pass

                text = f.type
                #width, height = draw.textsize(text, font=text_font)
                text_pos = (intf_offset[0] + port_height/2, intf_offset[1] - port_height*1.5)
                draw.text(text_pos, text, fill=text_color, font=text_font)
                pass
                
            len_svc = len_svc + len(s.serviceInterfaces)

            port_polygon = []
            for point in svcport_polygon:
                port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
                pass
            draw.polygon(port_polygon, fill=fill_color, outline=line_color)
            
            text = s.name
            text_pos = (offset[0] + port_height/2, offset[1] - port_height*1.5)
            draw.text(text_pos, text, fill=text_color, font=text_font)
            
        inport_polygon = ((-port_height/2-port_height/2, -port_height/2), (+port_height/2, -port_height/2),
                          (+port_height/2, +port_height/2),
                          (-port_height/2-port_height/2, port_height/2),
                          (-port_height/2-port_height/2+port_height/2, 0),
                          (-port_height/2-port_height/2, -port_height/2))
        
        for i, p in enumerate(rtcprof.inports):
            offset = (rtc_topleft[0], rtc_topleft[1] + top_bottom_margin + (port_height+port_margin)*i + port_height)
            port_polygon = []
            for point in inport_polygon:
                port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
                pass
            draw.polygon(port_polygon, fill=fill_color, outline=line_color)
            
            text = p.name + '(' + p.type + ')'
            width, height = draw.textsize(text, font=text_font)
            text_pos = (offset[0] - port_height/2 - width, offset[1] - port_height*1.5)
            draw.text(text_pos, text, fill=text_color, font=text_font)
            pass


        svcport_polygon = ((-port_height/2 - port_height/2, -port_height/2), (+port_height/2, -port_height/2),
                           (+port_height/2, port_height/2),
                           (-port_height/2 - port_height/2, port_height/2), (-port_height/2 - port_height/2, -port_height/2))

        pi = len(rtcprof.inports) - 1
        for j, s in enumerate(rtcprof.serviceports):
            flag = False
            for k, f in enumerate(s.serviceInterfaces):
                if f.direction == 'Provided':
                    flag = True
            if flag:
                continue

            pi = pi + 1
            offset = (rtc_topleft[0], rtc_topleft[1] + top_bottom_margin + (port_height+port_margin)*pi + port_height)
            
            for k, f in enumerate(s.serviceInterfaces):

                pi = pi + 1
                start = (offset[0] - port_height/2, offset[1])
                intf_offset = (rtc_topleft[0] - port_height/2 * 5, rtc_topleft[1] + top_bottom_margin + (port_height+port_margin)*pi + port_height)
                pivot0 = (start[0] - port_height/2 *2, start[1])
                pivot1 = (pivot0[0], intf_offset[1])
                draw.line((start, pivot0), fill=line_color)
                draw.line((pivot0, pivot1), fill=line_color)
                draw.line((pivot1, intf_offset), fill=line_color)
                
                bbox = ((intf_offset[0] - port_height, intf_offset[1]-port_height/2),
                        (intf_offset[0], intf_offset[1]+port_height/2))
                
                if f.direction == 'Provided':
                    #draw.ellipse(bbox, outline=line_color)
                    pass
                else:
                    draw.arc(bbox, 270, 90, fill=line_color)
                    pass

                text = f.type
                width, height = draw.textsize(text, font=text_font)
                text_pos = (intf_offset[0] - port_height/2 - width, intf_offset[1] - port_height*1.5)
                draw.text(text_pos, text, fill=text_color, font=text_font)
                pass
                
            len_svc = len_svc + len(s.serviceInterfaces)

            port_polygon = []
            for point in svcport_polygon:
                port_polygon.append((point[0] + offset[0], point[1] + offset[1]))
                pass
            draw.polygon(port_polygon, fill=fill_color, outline=line_color)
            
            text = s.name
            width, height = draw.textsize(text, font=text_font)
            text_pos = (offset[0] - port_height/2 - width, offset[1] - port_height*1.5)
            draw.text(text_pos, text, fill=text_color, font=text_font)

        return im



    def get_rtsp_image(self, package, rtsp, background_color=(255,255,255,255), line_color=(0,0,0,255), fill_color=(0,0,127,255), verbose=False, port_text_font=14, title_text_font=20, port_height = 20):
        from PIL import Image
        img_width = 1600

        if verbose:
            sys.stdout.write('# Get RTSP Image.\n')
        #port_height = 20
        count = 0
        height = 0
        img_height = 0
        height_array = []
        
        row = 3
        column = 0
        if verbose:
            sys.stdout.write('# ROW = %s\n' % row)
        components = []
        i = 0

        def comp_chara(comp):
            rtc_typename = comp.id.split(':')[3]
            rtc = admin.rtc.get_rtc_from_package(package, rtc_typename, verbose=verbose)
            rtcprof = rtc.rtcprofile

            print rtcprof.basicInfo.name, ':',

            in_score = +1
            out_score = -1
            prov_score = +2
            req_score = -2
            score = 0
            score = score + len(rtcprof.inports) * in_score
            score = score + len(rtcprof.outports) * out_score
            for sp in rtcprof.serviceports:
                for i in sp.serviceInterfaces:
                    if i.polarity == 'Provided':
                        score = score + prov_score
                    else:
                        score = score + req_score
            print score
            return score

        for c in rtsp.components:
            components.append(c)
        
        components_buf = sorted(components, key=comp_chara)
        
        max_col = len(components) / row 
        if len(components) % row > 0:
            max_col = max_col + 1
            pass
        ind = 0
        components_dic = {}
        r = 0
        for i, c in enumerate(components_buf):
            components_dic[ind*row + r] = c
            ind = ind + 1
            if ind == max_col:
                ind = 0
                r = r + 1
        components = []
        for i in range(0, len(components_dic.keys())):
            components.append(components_dic[i])
        
        for c in components:
            sys.stdout.write('# Component %s\n' % c.instance_name)
            rtc_typename = c.id.split(':')[3]
            rtc = admin.rtc.get_rtc_from_package(package, rtc_typename, verbose=verbose)
            rtcprof = rtc.rtcprofile
            rtc_height = self.get_image_height(rtcprof, port_height)
            if rtc_height > height:
                height = rtc_height
            count = count + 1
            if count == row:
                count = 0
                column = column+1
                sys.stdout.write('# Column %s height = %s\n' % (column, height))
                img_height = img_height + height + port_height*4
                height_array.append(height)
        if count > 0:
            column = column+1
            sys.stdout.write('# Column %s height = %s\n' % (column, height))
            img_height = img_height + height + port_height*4
            height_array.append(height)

        #img_height = img_height + port_height # for text

        im = Image.new('RGBA', (img_width, img_height), background_color)
        top_margin = port_height
        bottom_margin = port_height
        rtc_width  = port_height * 5

        count = 0
        height = 0
        column = 0
        for c in components:
            rtc_typename = c.id.split(':')[3]
            rtc = admin.rtc.get_rtc_from_package(package, rtc_typename, verbose=verbose)
            rtcprof = rtc.rtcprofile
            sys.stdout.write(' - RTC (%s)\n' % rtcprof.basicInfo.name)
            rtc_img_width = img_width / row
            rtc_topleft = ( (rtc_img_width - rtc_width) / 2 + rtc_img_width * count, top_margin + height + bottom_margin * column * 2)
            self.write_rtc_image(im, rtcprof, rtc_topleft, port_height, line_color, fill_color, port_text_font=port_text_font, title_text_font=title_text_font)
            
            count = count + 1
            if count == row:
                count = 0
                height = height + height_array[column]
                column = column + 1
        return im
