import sys, os


import wasanbon

from wasanbon.util import git
from wasanbon.core.rtc import rtcprofile
from wasanbon.core.rtc import packageprofile
from wasanbon.core.rtc import build

class RTCProfileNotFoundException(Exception):
    def __init__(self):
        pass


class RtcObject():

    def __init__(self, path, verbose=False):
        self._path = path
        self._rtc_xml = ""
        self._rtcprofile = None
        print path
        for root, dirs, files in os.walk(path):
            print ' - Parsing %s' % root
            if 'RTC.xml' in files:
                self._rtc_xml = os.path.join(root, 'RTC.xml')
                return
        raise RTCProfileNotFoundException()
        pass

    @property
    def rtcprofile(self):
        if not self._rtcprofile:
            self._rtcprofile = rtcprofile.RTCProfile(self._rtc_xml)
        return self._rtcprofile

    @property
    def packageprofile(self):
        return packageprofile.PackageProfile(self.rtcprofile)

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self.rtcprofile.basicInfo.name
    
    @property
    def language(self):
        return self.rtcprofile.language.kind

    def build(self, verbose=False):
        
        if self.language == 'C++':
            build.build_rtc_cpp(self.rtcprofile, verbose=verbose)
        elif self.language == 'Python':
            build.build_rtc_python(rtcp, verbose=verbose)
        elif self.language == 'Java':
            build.build_rtc_java(rtcp, verbose=verbose)
        pass

    def clean(self, verbose=False):
        if self.language == 'C++':
            build.clean_rtc_cpp(self.rtcprofile, verbose=verbose)
        pass

    def git_init(self, verbose=False):
        git.git_command(['init'], path=self.path, verbose=verbose)
        
        if verbose:
            sys.stdout.write(" - git init in repository in %s\n" % self.path)

        
        gitignore_files = ['*~', '.pyc', 'build-*']
        fout = open(os.path.join(self.path, '.gitignore'), 'w')
        for filename in gitignore_files:
            fout.write(filename + '\n')
        fout.close()

        git.git_command(['add', '.'], path=self.path, verbose=verbose)

        first_comment = 'This if first commit. This repository is generated by wasanbon'    
        git.git_command(['commit', '-a', '-m', first_comment], path=self.path, verbose=verbose)
        pass

    @property
    def git(self):
        return git.GitRepository(self.path)
