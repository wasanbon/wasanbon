#!/usr/bin/env python

from wasanbon.core import *
from wasanbon.core.management import *

import os, sys
import yaml
import subprocess
import shutil

import wasanbon

def build_rtc(rtcp):
    if rtcp.getLanguage() == 'C++':
        build_rtc_cpp(rtcp)
    pass

def clean_rtc(rtcp):
    if rtcp.getLanguage() == 'C++':
        clean_rtc_cpp(rtcp)
    pass

def clean_rtc_cpp(rtcp):
    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-' + sys.platform)
    if os.path.isdir(build_dir):
        print 'removing %s' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True )
    for root, dirs, files in os.walk(rtc_dir):
        for file in files:
            if file.endswith('~'):
                fullpath = os.path.join(root, file)
                if fullpath.startswith(os.getcwd()):
                    fullpath = fullpath[len(os.getcwd())+1]
                print 'removing %s' % fullpath
                os.remove(os.path.join(root, file))


def build_rtc_cpp(rtcp):
    rtc_name = rtcp.getName()
    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-%s' % sys.platform)
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [setting['local']['cmake'], '..']
    subprocess.call(cmd)

    if sys.platform == 'win32':
        if '%s.sln' % rtcp.getName in os.listdir(os.getcwd()):
            print 'Solution is successfully generated.'
            cmd = [setting['local']['msbuild'], file, '/p:Configuration=Release', '/p:Platform=Win32']
            subprocess.call(cmd)
            return
    elif sys.platform == 'darwin':
        if 'Makefile' in os.listdir(os.getcwd()):
            print 'Makefile is successfully generated.'
            cmd = ['make']
            subprocess.call(cmd)
            return

