#!/usr/bin/env python

from wasanbon.core.management import Application

import $APPNAME as app
from $APPNAME.setting import *

if __name__ == '__main__':
    Application.execute(application["name"])

    
