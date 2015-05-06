import os, sys, subprocess, urllib


def download_url(url, verbose=False, force=False, path='downloads'):
    cur_dir = os.getcwd()
    dir = os.path.join(cur_dir, path)
    if not os.path.isdir(dir): os.mkdir(dir)
    file = os.path.join(dir, os.path.basename(url))

    if not os.path.isfile(file):
        class DownloadReport(object):
            def __init__(self):
                pass

            def __call__(self, read_blocks, block_size, total_bytes):
                end = read_blocks * block_size / float(total_bytes) * 100.0
                sys.stdout.write('\r# Progress %3.2f [percent] ended' % end)
                sys.stdout.flush()
            pass

        
        if verbose: sys.stdout.write('# Downloading url:%s\n' % url)
        urllib.urlretrieve(url, file+'.part', DownloadReport())
        os.rename(file+'.part', file)
        if verbose: sys.stdout.write('# Saved to %s\n' % file)

    return file
