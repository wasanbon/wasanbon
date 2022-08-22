import os
import sys
import subprocess
import types
import time
import threading
import wasanbon
# from . import download, install, archive, svn#, git


def choice(alts, callback, msg='Choice', choice_msg='Choice?:', noquit=False):
    if not noquit:
        alts.append('Quit(Q)')
    while True:
        print(msg)
        for i in range(0, len(alts)):
            sys.stdout.write(' - %s:%s\n' % (i + 1, alts[i]))
        i = input(choice_msg)  # Input
        try:
            if i == 'q' or i == 'Q':  # if chice is 'q', quit.
                sys.stdout.write('Quit.\n')
                break
            ans = int(i)
        except ValueError as e:
            sys.stdout.write(' - ValueError.\n')
            continue
        if ans < 1 or ans > len(alts):
            sys.stdout.write(' - RangeError.\n')
            continue
        if ans == len(alts):
            sys.stdout.write(' - Quit.\n')
            break
        # Callback Function
        retval = callback(ans - 1)
        if type(retval) == list:
            ans = retval[0]
            alts = retval[1]
            alts.append('Quit(Q)')
        else:
            ans = retval

        # if callback function returns True, quit.
        if ans:
            sys.stdout.write(' - Quit.\n')
            break


def yes_no(msg):
    while True:
        sys.stdout.write('%s (Y/n)' % msg)
        c = input()
        if len(c) == 0:
            return 'yes'
        elif c[0] == 'y' or c[0] == 'Y':
            return 'yes'
        elif c[0] == 'n' or c[0] == 'N':
            return 'no'


def no_yes(msg):
    while True:
        sys.stdout.write('%s (y/N)' % msg)
        c = input()
        if len(c) == 0:
            return 'no'
        elif c[0] == 'y' or c[0] == 'Y':
            return 'yes'
        elif c[0] == 'n' or c[0] == 'N':
            return 'no'


def search_file(rootdir, filename):
    found_files_ = []
    if type(filename) is list:
        for file_ in filename:
            found_files_ = found_files_ + search_file(rootdir, file_)
        return found_files_

    files = os.listdir(rootdir)

    for file_ in files:
        fullpath_ = os.path.join(rootdir, file_)
        if os.path.isdir(fullpath_):
            found_files_ = found_files_ + search_file(fullpath_, filename)
        else:
            if file_ == filename:
                found_files_.append(fullpath_)
    return found_files_
