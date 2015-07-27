#
import os

filename = 'MANIFEST.in'
data_files = []
wasanbon_dir = 'wasanbon'

for dirpath, dirnames, filenames in os.walk(wasanbon_dir):
    # Ignore dirnames that start with '.'
    #for i, dirname in enumerate(dirnames):
    #    if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pass
    elif filenames:
        data_files.append((dirpath.replace('\\', '/'), [os.path.join(dirpath, f).replace('\\', '/') for f in filenames]))


fout = open(filename, 'w')
for d, files in data_files:
    for f in files:
        fout.write('include %s\n' % f)

fout.close()
