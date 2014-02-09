#!/usr/bin/env python
import os, sys, optparse, yaml, types
import wasanbon
from wasanbon.core import package as pack
from wasanbon.core import rtc, tools, repositories
from wasanbon.util import editor
from wasanbon import util


class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return [rtc.name for rtc in pack.Package(os.getcwd()).rtcs]

    def get_rtc_rtno(self, _package, name, verbose=False):
        try:
            return _package.rtc(name)
        except wasanbon.RTCNotFoundException, e:
            return tools.get_rtno_package(_package, name, verbose=verbose)

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())

        rtc_name = argv[2]
        targets = []
        for i in range(0, 16):
            if rtc_name.endswith(str(i)):
                target_file = os.path.join(_package.conf_path, rtc_name + '.conf')
                targets.append(target_file)
     
        if len(targets) == 0: # all files
            for i in range(0, 16):
                target_file = os.path.join(_package.conf_path, rtc_name + str(i) + '.conf')
                if os.path.isfile(target_file):
                    targets.append(target_file)

        for target in targets:
            sys.stdout.write(' - Configuring "%s"\n' % os.path.basename(target))
            rtcc = wasanbon.core.rtc.RTCConf(target)
                
            choice1 = ['add'] + [key + ':' + rtcc[key] for key in rtcc.keys()]
            def callback1(ans1):
                if ans1 == 0: # add
                    key = raw_input('    - Input keyname (ex., conf.default.param1) : ')
                else:
                    key = rtcc.keys()[ans1-1]
                    pass
                
                val = raw_input('    - Input value of %s (ex., 1) : ' % key)
                if util.yes_no('    - Update Configuration (%s:%s)?' % (key, val)) == 'yes':
                    sys.stdout.write('    - Configuring (key=%s, value=%s).\n' % (key, val))
                    rtcc[key] = val
                    choice1 = ['add'] + [key + ':' + rtcc[key] for key in rtcc.keys()]
                    return [False, choice1]
                else:
                    sys.stdout.write('    - Aborted.\n')
                    return False
            util.choice(choice1, callback1, ' @ Choice configuration', choice_msg=' @ Choice?:')
            rtcc.sync(verbose=verbose)
            
