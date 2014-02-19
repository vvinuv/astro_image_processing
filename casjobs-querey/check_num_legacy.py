#!/usr/bin/python

# We are going to clean our sample similar to Simard ...

from mysql_class import *
import numpy as np
from sdss_flags import *

in_table = 'CAST_raw'

cursor = mysql_connect('intermediate_tables', 'pymorph', 'pymorph')

# first remove any galaxies not in the Legacy survey
infile = open('../allrunsdr7db.par')

count_total = 0
for line in infile.readlines():
    if line[0] not in '#':
        try:
            line = line.split()
            run = line[1]
            rerun = line[2]
            field0 = int(line[7])
            nfield = int(line[8])
            use = line[12]

            if use != 'Legacy':
                cmd_stem = 'select count(*) from %s where run = %s and rerun = %s and field= ' %(in_table, run, rerun)

                for curf in range(field0, field0+nfield):
                    count = cursor.get_data(cmd_stem + str(curf) + ';')[0]
                    print 'exclude ', count
                    count_total +=count
        except:
            pass

infile.close()
print 'total_count = ', count_total
