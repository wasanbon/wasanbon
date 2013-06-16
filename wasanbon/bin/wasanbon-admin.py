#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('cp932')(sys.stdout)


import wasanbon
from wasanbon.core import management

if __name__ == '__main__':
    management.application.execute()
    
