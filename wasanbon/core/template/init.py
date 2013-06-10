#!/usr/bin/env python

import os, sys, shutil, yaml
import subprocess
import wasanbon


def register_workspace(appname, appdir):
    print ' - Registering workspace:'
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    f_bak = False
    if os.path.isfile(ws_file_name):
        if os.path.isfile(ws_file_name + ".bak"):
            os.remove(ws_file_name + ".bak")
        os.rename(ws_file_name, ws_file_name + ".bak")
        f_bak = open(ws_file_name + ".bak", "r")
    
    fout = open(ws_file_name, "w")
    if f_bak:
	for line in f_bak:
            fout.write(line)
    
    fout.write("%s: '%s'\n" % (appname, appdir))
    fout.close()

def unregister_workspace(appname):
    print ' - Unregistering workspace:'
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    f_bak = False
    if os.path.isfile(ws_file_name):
        if os.path.isfile(ws_file_name + ".bak"):
            os.remove(ws_file_name + ".bak")
        os.rename(ws_file_name, ws_file_name + ".bak")
        f_bak = open(ws_file_name + ".bak", "rt")
    
    fout = open(ws_file_name, "wt")
    if f_bak:
	for line in f_bak:
            print ' -- %s' % line
            if not line.strip().startswith(appname):
                fout.write(line)
    fout.close()

def get_workspace_list():
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if os.path.isfile(ws_file_name):
        f = open(ws_file_name, "r")
        y = yaml.load(f)
        f.close()
        return y
    return None

def list_workspace():
    print ' - Listing worksace:'
    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if os.path.isfile(ws_file_name):
        f = open(ws_file_name, "r")
        y = yaml.load(f)
        if not y:
            print ' - No workspace registered.'
            return
        for key in y.keys():
            print "%s : '%s'" % (key, y[key])
        f.close()


def init_workspace(appname):
    print ' - Initializing workspace %s:' % appname

    ws_file_name = os.path.join(wasanbon.rtm_home, "workspace.yaml")
    if os.path.isfile(ws_file_name):
        f = open(ws_file_name, "r")
        y = yaml.load(f)
        if appname in y.keys():
            print ' - Error: There seems to be %s project in localhost.' % appname
            return False
        f.close()

    tempdir = os.path.join(wasanbon.__path__[0], 'template')
    appdir = os.path.join(os.getcwd(), appname)

    if os.path.isdir(appdir) or os.path.isfile(appdir):
        print 'There seems to be %s here. Please change application name.' % appname

    sys.stdout.write(" - copying from %s to %s\n" % (tempdir, appdir))
        
    for root, dirs, files in os.walk(tempdir):
        distdir = os.path.join(appdir, root[len(tempdir)+1:])
        os.mkdir(distdir)
        for file in files:
            sys.stdout.write("    - file: %s\n" % file)
            fin = open(os.path.join(root, file), "r")
            fout = open(os.path.join(distdir, file), "w")
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

    register_workspace(appname, appdir)    
    pass

