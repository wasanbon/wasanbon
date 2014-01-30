#!/usr/bin/env python
import os, sys
import wasanbon
from wasanbon.util import editor
from wasanbon.core import package as pack
from wasanbon.core import tools
class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        _package = pack.Package(os.getcwd())
        return [rtc.name for rtc in _package.rtcs]

    def execute_with_argv(self, argv, clean, force, verbose):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())
        try:
            rtc_ = _package.rtc(argv[2])
                
            if rtc_.is_git_repo():
                if rtc_.git_branch() != 'master':
                    sys.stdout.write(' @ You are not in master branch.\n')
                    if util.yes_no(' @ Do you want to checkout master first?') == 'yes':
                        rtc_.checkout(verbose=verbose)
            editor.edit_rtc(_package.rtc(argv[2]), verbose=verbose)
        except wasanbon.RTCNotFoundException, ex:
            rtnos = tools.get_rtno_packages(_package)
            for rtno in rtnos:
                if rtno.name == argv[2]:
                    tools.launch_arduino(rtno.file, verbose=verbose)
                    return
            raise wasanbon.RTCNotFoundException()

