"""
Build RT-component from source code.
This command will create build-*** directory in your RTC's directory, and make it.

* This command does not install the compiled binary file into the system.
* If you want to use it, use 'install' command after compilation.

ex.,
  $ mgr.py build YOUR_RTC_NAME

If you want to know your RTCs' name, use :
  $ mgr.py rtc list


"""

#!/usr/bin/env python
import os, sys
import wasanbon
from wasanbon.core import package as pack
from wasanbon import util

def alternative():
    _package = pack.Package(os.getcwd())
    return [rtc.name for rtc in _package.rtcs]

def execute_with_argv(argv, verbose, force=False, clean=False):
    wasanbon.arg_check(argv, 3)
    _package = pack.Package(os.getcwd())
    
    build_all = True if 'all' in argv else False
    found_flag = False
    if sys.platform == 'win32':
        verbose=True
        pass
    
    for rtc in _package.rtcs:
        if build_all or rtc.name in argv:
            sys.stdout.write(' @ Building RTC %s\n' % rtc.name)
            ret = rtc.build(verbose=verbose)
            if ret[0]:
                sys.stdout.write(' - Success\n')
            else:
                sys.stdout.write(' - Failed\n')
                if util.yes_no(' - Do you want to watch error message?') == 'yes':
                    print ret[1]
            found_flag = True
            pass
        pass
    
    if not found_flag:
        sys.stdout.write(' - Can not find RTC.\n')


                    

