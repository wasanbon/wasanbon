import os
import twisted
from nevow import static, rend, loaders
from nevow import tags as T
from parser import Parser

_background_img = 'waseda_background.jpg'
_version = '0.1.0'
CSS_DIR='static/css'
HTML_DIR='static/html'
JS_DIR='static/js'
MEDIA_DIR='static/media'

def document_factory(file):
    parser = Parser(file)
    return loaders.htmlstr(
        parser.parse()
    );
    

class Page(rend.Page):
    def __init__(self, file):
        self.file = file
        self.parser = Parser(file)

    def renderHTTP(self, context):
        print 'Context:', context
        return self.parser.parse()

class ResourceManager(rend.Page):
    isLeaf = True
    __except_dir = ['js', 'index.css']

    _index_files = []

    def _search_image(self, dir):
        for f in os.listdir(dir):
            if f.endswith('png') or f.endswith('jpg') or f.endswith('bmp') or f.endswith('gif'):
                return f
        return ''

    def _search_index_html(self, dir):
        for root, dirs, files in os.walk(dir):
            #print ' - Parsing %s' % root
            if 'index.html' in files or 'index.htm' in files:
                print ' -- Found.'
                self._index_files.append(root)
        
        print ' -- Files are'
        for p in self._index_files:
            print ' --- %s' % p
        index_file = ''
        max_count = 1000
        for index in self._index_files:
            if index.count(os.sep) < max_count:
                index_file = index
                max_count = index.count(os.sep)
        return index_file

    def __init__(self, static_dir='static'):
        rend.Page.__init__(self)
        self._index_files = []
        self.static_dir = static_dir
        print 'ResourceManager.__init__(%s)' % static_dir

        
        #self.putChild('index.css', static.File(os.path.join(static_dir, 'index.css')))
        for f in os.listdir(static_dir):
            if f.endswith('~'):
                continue
            path = os.path.join(static_dir, f)

            
            if not os.path.isdir(path):
                self.putChild(f, static.File(path))
                continue
            print ' - Now Parsing : %s' % path

            
            self._index_files = []
            index_path = self._search_index_html(path)
            print index_path
            #print 'Application: ', index_path
            self.putChild(f, static.File(path))
            img_path = f + '/' + self._search_image(path)
            if not f in self.__except_dir:                
                self._index += """
    <a href="%s">
      <li class="plugin_item" id="%s-li">
        <img id="%s-img" src="%s"></img>
        <h1>%s</h1>
      </li>
    </a>
""" % (index_path[len(static_dir)+1:], f, f, img_path, f)

        self._index += """
  </ul>
  </div>
</body></html>"""
        filename = os.path.join(self.static_dir, 'index.html')
        open(filename, 'w').write(self._index)

    _index = """
<html>
<head>
  <title>Wasanbon Web System %s</title>
  <script type="text/javascript" src="js/jquery-1.11.0.min.js"></script>
  <script type="text/javascript" src="js/jquery-ui-1.10.4.min.js"></script>
  <link rel="stylesheet" href="index.css" type="text/css"></link>
</head>
<body id="content" style="background-image:url(%s); background-position: top center; background-size: cover;">
  <div id="toolbar">
  </div>
<!--
  <div id="top">
    <h1>wasanbon web server</h1>
    <p>Framework for Robotic Technology System</p>
    <p>Version : %s</p>
  </div>
-->
  <div id="container">
  <ul class="plugin_items">
""" % (_version, _background_img, _version)
    
    def parse(self):
        for file in os.listdir(self.static_dir):
            if file.endswith('~'): continue

            if os.path.isfile(os.path.join(self.static_dir, file)):
                self.putChild(file, Page(os.path.join(self.static_dir, file)))

    def renderHTTP(self, ctx):
        return self._index
        #filename = os.path.join(self.static_dir, 'index.html')
        #return open(filename, 'r').read()
        
