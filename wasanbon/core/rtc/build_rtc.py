#!/usr/bin/env python

from wasanbon.core import *
from wasanbon.core.management import *

import os, sys, platform
import yaml
import subprocess
import shutil

import wasanbon

def build_rtc(rtcp):
    if rtcp.getLanguage() == 'C++':
        build_rtc_cpp(rtcp)
    elif rtcp.getLanguage() == 'Java':
        build_rtc_java(rtcp)
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

    if sys.platform == 'linux2' and platform.architecture()[0] == '64bit':
        print ' - detected 64bit linux2. modify PKG_CONFIG_PATH environ.'
        os.environ['PKG_CONFIG_PATH'] = '/usr/lib64/pkgconfig/:/usr/local/lib64/pkgconfig/'
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    os.chdir(build_dir)
    cmd = [wasanbon.setting['local']['cmake'], '..']
    subprocess.call(cmd, env=os.environ)

    if sys.platform == 'win32':
        sln = '%s.sln' % rtcp.getName()
        if sln in os.listdir(os.getcwd()):
            print 'Solution is successfully generated.'
            cmd = [wasanbon.setting['local']['msbuild'], sln, '/p:Configuration=Release', '/p:Platform=Win32']
            subprocess.call(cmd)
            return
    elif sys.platform == 'darwin':
        if 'Makefile' in os.listdir(os.getcwd()):
            print 'Makefile is successfully generated.'
            cmd = ['make']
            subprocess.call(cmd)
            return
    elif sys.platform == 'linux2':
        if 'Makefile' in os.listdir(os.getcwd()):
            print 'Makefile is successfully generated.'
            cmd = ['make']
            subprocess.call(cmd)
            return


def build_rtc_java(rtcp):
    rtc_name = rtcp.getName()
    rtc_dir, rtc_xml = os.path.split(rtcp.getRTCProfileFileName())
    build_dir = os.path.join(rtc_dir, 'build-%s' % sys.platform)
    src_dir = os.path.join(rtc_dir, 'src')
    cls_dir = os.path.join(build_dir, 'class')
    bin_dir = os.path.join(build_dir, 'bin')
    current_dir = os.getcwd()
    os.chdir(rtc_dir)
    rtm_java_classpath = os.path.join(wasanbon.rtm_home, 'jar')           

    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    if not os.path.isdir(cls_dir):
        os.makedirs(cls_dir)
    if not os.path.isdir(bin_dir):
        os.makedirs(bin_dir)


    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    if sys.platform == 'win32':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)

    javafiles = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.java'):
                javafiles.append(os.path.join(root, f))

    cmd = [wasanbon.setting['local']['javac'], '-encoding', 'SJIS',
           '-s', src_dir, '-d', cls_dir]
    for f in javafiles:
        cmd.append(f)
    print cmd
    subprocess.call(cmd, env=java_env)

    clsfiles = []
    for root, dirs, files in os.walk(cls_dir):
        for f in files:
            if f.endswith('.class'):
                clsfiles.append(os.path.join(root, f)[len(cls_dir)+1:])

    jarcmd = os.path.join(os.path.split(wasanbon.setting['local']['javac'])[0], 'jar')
    cmd = [jarcmd, 'cfv', os.path.join(bin_dir, rtc_name + '.jar'), '-C', os.path.join(build_dir, 'class')]

    for f in clsfiles:
        cmd.append(cls_dir)
        cmd.append(f)
    print cmd
    subprocess.call(cmd, env=java_env)
