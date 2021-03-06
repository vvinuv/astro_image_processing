"""This script reads in a file 'ingals.txt' that contains galaxy identifiers
in the first column (i.e. galcount) and redshift in the second column
 and returns a corresponding list of null
locations to be used in the subtraction from the true correlated function"""


"""This is hard-coded to select between 0<dec<60 and 120<ra<240 which 
corresponds to SDSS sky coverage for now"""


import os
from astro_image_processing.mysql import *


def get_gals():
    """Returns the list of galaxy identifiers that we will generate 
random points for"""
    return np.loadtxt('ingals.txt', usecols=[0,1], comments='#', unpack=True)

def get_gals_sql():
    """Returns the list of galaxy identifiers extracted from SQL
 that we will generate random points for."""
    cursor = mysql_connect('catalog','pymorph','pymorph')
    gals, z = cursor.get_data('select thing_id, zspec from claudia_blanksky;') 
    return gals, z
    
def write_gals(gals, z, pos):
    """outputs the galaxy position combination for each galaxy"""
    outfile = open('null_pos.txt', 'w')
    outfile.write('# galcount ra_degrees dec_degrees\n')
    for outgal, outpos in zip(gals, pos):
        outfile.write('%d %6.3f %6.3f\n' %(outgal, outpos[0],outpos[1])) 
    outfile.close()
    return

def write_gals_sql(gals, z, pos, tablename):
    """outputs the galaxy position combination for each galaxy"""

    cursor = mysql_connect('catalog','pymorph','pymorph',autocommit=False)
    
    count = 0
    for outgal, outpos in zip(gals, pos):
        cmd = 'update %s set  ra_gal= %f, dec_gal = %f where thing_id = %d;' %(tablename,outpos[0],outpos[1], outgal)
    #print cmd
        cursor.execute(cmd)
        count+=1
        if count % 10000 ==0:
            print count
            cursor.Conn.commit()            
    cursor.Conn.commit()

import numpy as np


if __name__=="__main__":
    ingals,zgals = get_gals_sql()
    seed = 4059091349
    np.random.seed(seed)
    
    new_pos = np.random.rand(len(ingals), 2)
    
    #covert ra to radians
    new_pos[:,0] = (new_pos[:,0]+1.0)*2.0*np.pi/3.0 
    #convert dec to radians, 0.5 factor restricts to 60 degrees
    new_pos[:,1] = np.arccos(1.0-new_pos[:,1]*0.5)

    new_pos = np.degrees(new_pos)

    write_gals_sql(ingals, zgals,new_pos,'claudia_blanksky')
    




