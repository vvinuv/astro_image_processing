#!/data2/home/ameert/python/bin/python2.5

import os
import sys

to_remove = ['OEM_*.fits', 'SO_*.fits', 'R_*.html', 'seg.fits', 'SegCat.cat',
             'index.html', 'restart.cat', 'P_*.png', 'pymorph.html',
             'E_*.txt', 'OE_*.txt', 'BackMask.fits','check.fits','config.pyc',
              ]#'O_*.fits']# , 'M*.fits', 'EM*.fits']

#tablename = sys.argv[1]
#model = sys.argv[2]
#count = sys.argv[3]

#os.system('/data2/home/ameert/catalog/scripts/count_neighbors.py full_dr7_neighborcount ser g %s' %count)
#os.system('/data2/home/ameert/catalog/scripts/compare_gin.py ser g %s' %count)

try:
    targetdir = int(sys.argv[1])
    targetdir = '%04d' %targetdir
except:
    targetdir = './'
    
thisdir = os.getcwd()

os.chdir(targetdir)
for del_file in to_remove:
    os.system('rm %s' %del_file)

os.chdir(thisdir)

