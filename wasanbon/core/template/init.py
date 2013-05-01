#!/usr/bin/env python

import os, sys
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
    
