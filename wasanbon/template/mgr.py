#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('cp932')(sys.stdout)


import wasanbon
from wasanbon.core.management import application

if __name__ == '__main__':
    sys.exit(application.execute())
