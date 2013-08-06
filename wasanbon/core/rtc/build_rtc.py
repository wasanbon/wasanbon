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

