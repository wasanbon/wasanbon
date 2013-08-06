#!/usr/bin/env python

from wasanbon.core import *
from wasanbon.core.management import *

import os, sys, platform
import yaml
import subprocess
import shutil

import wasanbon

def build_rtc(rtcp, verbose=False):
    pass

def clean_rtc(rtcp, verbose=False):
    if rtcp.language.kind == 'C++':
        clean_rtc_cpp(rtcp)
    pass

def clean_rtc_cpp(rtcp, verbose=False):
    rtc_dir, rtc_xml = os.path.split(rtcp.filename)
    build_dir = os.path.join(rtc_dir, 'build-' + sys.platform)
    if os.path.isdir(build_dir):
        if verbose:
            print ' - Removing Building Directory %s' % build_dir
        shutil.rmtree(build_dir, ignore_errors=True )
    for root, dirs, files in os.walk(rtc_dir):
        for file in files:
            if file.endswith('~'):
                fullpath = os.path.join(root, file)
                if fullpath.startswith(os.getcwd()):
                    fullpath = fullpath[len(os.getcwd())+1]
                if verbose:
                    print ' - Removing Emacs backup file %s' % fullpath
                os.remove(os.path.join(root, file))

