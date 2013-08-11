#!/usr/bin/env python
import os, sys

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

    def __getitem__(self, key):
        return self.dic.get(key, "")

    def __setitem__(self, key, value):
        self.dic[key] = value
        
    def append(self, key, value):
        if not key in self.dic.keys():
            self.dic[key] = value
        elif len(self.dic[key].strip()) == 0:
            self.dic[key] = value
        else:
            values = [v.strip() for v in self.dic[key].split(',')]
            if not value in values:
                self.dic[key] = self.dic[key] + ',' + value

    def remove(self, key, value):
        if not key in self.dic.keys():
            return
        elif len(self.dic[key].strip()) == 0:
            return
        else:
            values = [v.strip() for v in self.dic[key].split(',')]
            self.dic[key] = ''
            for v in values:
                if not v == value:
                    if not len(self.dic[key]) == 0:
                        self.dic[key] = self.dic[key] + ','
                    self.dic[key] = self.dic[key] + v
        
    def sync(self):
        if os.path.isfile(self.filename + ".bak"):
            os.remove(self.filename + ".bak")
        os.rename(self.filename, self.filename + '.bak')
        fin = open(self.filename + '.bak', 'r')
        fout = open(self.filename, 'w')

        keys = self.dic.keys()[:]
        while True:
            line = fin.readline()
            if not line:
                break;
            if line.strip().startswith('#'):
                fout.write(line)
                continue

            while line.strip().endswith('\\'):
                line_new =  fin.readline()
                if not line_new:
                    return
                line = line.strip().split('\\')[0] + line_new
                line_num = line_num+1

            if not len(line.strip()) > 0:
                fout.write(line)
                continue

            nv = line.strip().split(':')
            if len(nv) < 2:
                print 'Invalid Configuration in line %d' % line_num
                print '>>> ' + line
                return
            if len(nv) > 2:
                for v in nv[2:]:
                    nv[1] =  nv[1] + ':' + v

            if nv[0] in keys:
                fout.write(nv[0] + ':' + self.dic[nv[0]] + '\n')
                keys.remove(nv[0])
            else:
                fout.write(line)

        for key in keys:
            fout.write(key + ':' + self.dic[key] + '\n')

        fin.close()
        os.remove(self.filename + '.bak')
        fout.close()
