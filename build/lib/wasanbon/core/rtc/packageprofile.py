#!/usr/bin/env python
import os
import kotobuki.core.rtc.status_rtc as stat

class PackageProfile(object):

    """
    """
    def __init__(self, rtcp):
        [self.path, dummy] = os.path.split(rtcp.filename)
        self.bin = stat.find_rtc_bin(rtcp)
        self.conf = stat.find_rtc_conf(rtcp)
        if self.bin == None:
            self.bin = ''
        if self.conf == None:
            self.conf = ''

    def getPackagePath(self):
        return self.path

    def getRTCFilePath(self):
        return self.bin

    def getConfFilePath(self):
        return self.conf
