#!/usr/bin/env python

import os, sys, shutil, yaml
import subprocess
import wasanbon

def init_workspace(appname):
    print 'Initializing workspace %s:' % appname
    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), appname)

    if os.path.isdir(appdir) or os.path.isfile(appdir):
        print 'There seems to be %s here. Please change application name.' % appname
        
    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        os.mkdir(distdir)
        print 'copy from %s \n     to   %s' % (root, distdir)

        for file in files:
            fin = open(os.path.join(root, file), "r")
            fout = open(os.path.join(distdir, file), "w")
            print '    file: %s' % file
            for line in fin:
                index = line.find('$APP')
                if index >= 0:
                    line = line[:index] + appname + line[index + len('$APP'):]
                fout.write(line)
            fin.close()
            fout.close()
            
    y = yaml.load(open(os.path.join(appdir, 'setting.yaml'), 'r'))
    file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    shutil.copy(file, os.path.join(appdir, y['application']['RTC_DIR'], 'repository.yaml'))
    
    if sys.platform == 'darwin' or sys.platform == 'linux2':
        cmd = ['chmod', '755', os.path.join(appname, 'mgr.py')]
        subprocess.call(cmd)
    pass

