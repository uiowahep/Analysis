
import os, re, subprocess

def mkdir(Dir):

    nSlash = Dir.count('/')
    iSlash = 1*(Dir.startswith('/'))

    if (nSlash == 0):
        if not os.path.exists(Dir):
            subprocess.call('mkdir %s' % d, shell=True)
        return

    for i in range(iSlash+1, Dir.count('/')+1):
        idxs   = [x.start() for x in re.finditer('/', Dir)]
        Subdir = Dir[0:idxs[i-1]]
        if not os.path.exists(Subdir):
            subprocess.call('mkdir %s' % Subdir, shell=True)
    if not os.path.exists(Dir):
        subprocess.call('mkdir %s' % Dir, shell=True)
