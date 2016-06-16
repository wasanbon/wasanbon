import os, re

class Parser():
    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        str = open(self.filename, 'r').read()
        #def func(matchobj):
        #    return open(os.path.join(os.path.dirname(self.filename), matchobj.groupdict()['filename']), 
        #                'r').read()

        print str
        return str
        #return re.sub(r'<include[ \t\n\r\f\v]*arg=[\'\"](?P<filename>.+)[\'\"][ \t\n\r\f\v]*/>', func, str)

