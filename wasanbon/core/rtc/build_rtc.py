#!/usr/bin/env python

from wasanbon.core import *
from wasanbon.core.management import *

import os, sys
import yaml
import subprocess
import shutil

def build_rtc(rtcp):
    if sys.platform == 'win32':
        build_rtc_win32(rtcp)
    elif sys.platform == 'darwin':
        build_rtc_osx(rtcp)
    pass

def clean_rtc(rtcp):
    if sys.platform == 'win32':
        clean_rtc_win32(rtcp)
    elif sys.platform == 'darwin':
        clean_rtc_osx(rtcp)
    pass

def clean_rtc_win32(rtcp):
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    current_y = yaml.load(open(os.path.join(os.getcwd(), 'setting.yaml'), 'r'))
    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-win32')
    if build_dir.startswith(os.getcwd()):
        build_dir = build_dir[len(os.getcwd())+1:]
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

def clean_rtc_osx(rtcp):
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    current_y = yaml.load(open(os.path.join(os.getcwd(), 'setting.yaml'), 'r'))
    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-osx')
    if build_dir.startswith(os.getcwd()):
        build_dir = build_dir[len(os.getcwd())+1:]
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

def build_rtc_osx(rtcp):
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    current_y = yaml.load(open(os.path.join(os.getcwd(), 'setting.yaml'), 'r'))

    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-osx')
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [y['cmake_path'], '..']
    subprocess.call(cmd)

    for file in os.listdir(os.getcwd()):
        if file == 'Makefile':
            print 'Makefile is successfully generated.'
            cmd = ['make']
            subprocess.call(cmd)
            return

def build_rtc_win32(rtcp):
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    current_y = yaml.load(open(os.path.join(os.getcwd(), 'setting.yaml'), 'r'))

    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-win32')
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [y['cmake_path'], '..']
    subprocess.call(cmd)

    for file in os.listdir(os.getcwd()):
        if file.endswith('.sln'):
            print 'Solution %s is successfully generated.' % file
            cmd = [y['msbuild_path'], file, '/p:Configuration=Release', '/p:Platform=Win32']
            subprocess.call(cmd)
