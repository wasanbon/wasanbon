#!/usr/bin/env python
import os, sys
import wasanbon
from wasanbon import util

plugin_obj = None

class RTCConf(object):
    def __init__(self, rtcconf, verbose=False):
        if verbose:
            sys.stdout.write(' - Parsing rtcconf %s\n' % rtcconf)
        self.filename = rtcconf
        self.dic = {}

        fin = open(rtcconf, 'r')
        
        line_num = 0
        while True:
            line_num = line_num + 1
            line = fin.readline()
            if not line:
                break

            if line.strip().startswith('#'):
                continue

            while line.strip().endswith('\\'):
                line_new =  fin.readline()
                if not line_new:
                    return
                line = line.strip().split('\\')[0] + line_new
                line_num = line_num+1

            if not len(line.strip()) > 0:
                continue

            nv = line.strip().split(':')
            if len(nv) < 2:
                print ' - Invalid Configuration in line %d' % line_num
                print '>>> ' + line
                return
            if len(nv) > 2:
                for v in nv[2:]:
                    nv[1] =  nv[1].strip() + ':' + v.strip()
            self.dic[nv[0].strip()] = nv[1]


    def __str__(self):
        return str(self.dic)

    def keys(self):
        return self.dic.keys()

    def values(self):
        return self.dic.values()

    def items(self):
        return zip(self.keys(), self.values())

    def __getitem__(self, key):
        return self.dic.get(key, "")

    def __setitem__(self, key, value):
        self.dic[key] = value
    
    def pop(self, key):
        self.dic.pop(key)
        pass
        
    def append(self, key, value):
        if not key in self.dic.keys():
            self.dic[key] = value
        elif len(self.dic[key].strip()) == 0:
            self.dic[key] = value
        else:
            values = [v.strip() for v in self.dic[key].split(',')]
            if not value in values:
                self.dic[key] = self.dic[key] + ',' + value

    def remove(self, key, value=None, verbose=False):
        if verbose:
            sys.stdout.write(' - Removing %s from key (%s) in rtcconf (%s)\n' % (value, key, os.path.basename(self.filename)))
        if not key in self.dic.keys():
            return
        elif len(self.dic[key].strip()) == 0:
            return
        else:
            if value==None:
                del(self.dic[key])
                return
            values = [v.strip() for v in self.dic[key].split(',')]
            self.dic[key] = ''
            for v in values:
                if not v == value:
                    if not len(self.dic[key]) == 0:
                        self.dic[key] = self.dic[key] + ','
                    self.dic[key] = self.dic[key] + v
        
    def sync(self, verbose=False, outfilename=""):
        filename = self.filename
        if len(outfilename) == 0:
            outfilename = filename

        if filename == outfilename:
            backup_filename = filename + ".bak"
            if os.path.isfile(backup_filename):
                os.remove(backup_filename)
            os.rename(filename, backup_filename)
            infilename = backup_filename
        else:
            infilename = filename

        fin = open(infilename, 'r')
        fout = open(outfilename, 'w')

        keys = self.dic.keys()[:]
        while True:
            line = fin.readline()

            if not line: # File End
                break;
            if line.strip().startswith('#'): # Comment Line
                fout.write(line)
                continue

            while line.strip().endswith('\\'): # Line is not end
                line_new =  fin.readline()
                if not line_new:
                    return
                line = line.strip().split('\\')[0] + line_new
                line_num = line_num+1

            if not len(line.strip()) > 0: # Line is empty
                fout.write(line)
                continue

            nv = line.strip().split(':')
            if len(nv) < 2:
                print 'Invalid Configuration in line %d' % line_num
                print '>>> ' + line
                return
            if len(nv) > 2: # If configuration value includes ':' like localhost:2809, connect.
                for v in nv[2:]:
                    nv[1] =  nv[1] + ':' + v

            if nv[0] in keys:
                fout.write(nv[0] + ':' + self.dic[nv[0]] + '\n')
                keys.remove(nv[0])
            else:
                # fout.write(line) # Do not sync
                pass


        for key in keys:
            fout.write(key + ':' + self.dic[key] + '\n')

        fin.close()
        if filename == outfilename:
            if os.path.isfile(backup_filename):
                os.remove(backup_filename)
        fout.close()

    def ext_check(self, verbose=False, autofix=False, interactive=False):
        rtcbins = [rtc.strip() for rtc in self['manager.modules.preload'].split(',') if not len(rtc.strip()) == 0]
        valid_bins = []
        for rtcbin in rtcbins:
            if not rtcbin.endswith(wasanbon.get_bin_file_ext()):
                if verbose or interactive:
                    sys.stdout.write(' - Detect invalid bin file expression (%s)\n' % rtcbin)
                valid_name = rtcbin[:rtcbin.rfind('.')] + wasanbon.get_bin_file_ext()
                if interactive or autofix:
                    res = []
                    if autofix:
                        res = 'yes'
                    else:
                        res = util.yes_no(' - Change file name from %s to %s?' % (rtcbin, valid_name))
                    if res == 'yes':
                        if verbose or interactive:
                            sys.stdout.write(' - Changed.\n')
                        valid_bins.append(valid_name)
                    else:
                        valid_bins.append(rtcbin)

        
        self['manager.modules.preload'] = ''
        for rtcbin in valid_bins:
            self.append('manager.modules.preload', rtcbin)
        pass

    def validate(self, verbose=False, autofix=False, interactive=False):
        if verbose:
            sys.stdout.write('Validating rtc.conf(%s)\n' % self.filename)
        
            #self.ext_check(verbose=verbose, autofix=autofix, interactive=interactive)
        pass
