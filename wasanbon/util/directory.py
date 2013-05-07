import os, sys


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
