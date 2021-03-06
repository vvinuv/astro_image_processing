#!/usr/bin/python

import sys



import os
import itertools
import pyfits
import datetime
import string
import numpy as np
import healpy as hp
from optparse import OptionParser, OptParseError

from generate_table import *
from create_healpy_map import *


def load_cat(filename):
    ra, dec = np.loadtxt(filename, usecols=[0,1], unpack=True)
    rowcount = np.arange(0,ra.size)
    return rowcount, ra, dec

def write_metadata(outfile, options):
    outfile.write("""#++++++++++++++++++++++++++++++++++++++++++++++++++
# Matching generated by crossmatch_external.py
#
# catalog 1: {cat1}
# catalog 2: {cat2}
# maximum galaxy separation: {maxsep} arcsec
# healpix nside: {nside}
# output filename (this file): {outfile}
# date: {today}
#
# Columns:
#   1: the row from catalog 1 (zero-indexed)
#   2: the row from catalog 2 (zero-indexed)
#   3: the separation in arcseconds (.2f format)
#--------------------------------------------------
""".format(cat1=options.incat1,cat2=options.incat2,
           maxsep=options.maxdist ,nside=options.nside , 
           outfile=options.outfile ,today = datetime.date.today().isoformat()))
    return

usage = """crossmatch-external.py OPTIONS"""
desc = """This program will crossmatch two input catalogs of ra/dec coordinates  and output the results

In general, you need to specify the input tables, and output file."""

parser = OptionParser(usage=usage, description = desc)
parser.add_option("-f","--first-cat", action="store", type="string",
                      dest="incat1", default = 'test.incat',
                      help="first input catalog")
parser.add_option("-s","--second-cat", action="store", type="string",
                      dest="incat2", default = 'test.incat',
                      help="second input catalog")

parser.add_option("-d","--max-distance", action="store", type="float",
                      dest="maxdist", default =3.0,
                      help="the maximum separation in arcsecs that any source may have.")

parser.add_option("-o","--output-file", action="store", type="string",
                      dest="outfile", default = './output.txt',
                      help="output file for crossmatched catalog")

parser.add_option("-n", "--nside",  action="store", type="int",
                      dest="nside", default = 256,
                      help="nside parameter used to construct healpix map")

# parses command line aguments for pymorph
(options, args) = parser.parse_args()


print "Loading and Mapping First catalog"    
galcount1, ra1, dec1 = load_cat(options.incat1)
cat1 = catalog(galcount1, ra1, dec1, NSIDE=options.nside)
cat1.map_sample()
print "First catalog loaded/mapped!!!"

print "Loading and Mapping Second catalog"    
galcount2, ra2, dec2 = load_cat(options.incat2)
cat2 = catalog(galcount2, ra2, dec2, NSIDE=options.nside)
cat2.map_sample()
print "Second catalog loaded/mapped!!!"

print "now matching!!!"
formatch = cat1.forward_match(cat2, options.maxdist)
backmatch = cat2.forward_match(cat1, options.maxdist)

print "now cross-matching!!!"
matches = get_crossmatch(formatch, backmatch)
print "catalogs matched!!!"

print "%d matches found...continuing" %(len(matches))
print "writing table to text file"

outfile = open(options.outfile, 'w')
write_metadata(outfile, options)
for match in matches:
    outfile.write("%d %d %.2f\n" %(match[0], match[1], match[2]))
print "matches written"
outfile.close()

print "completed table available at %s" %options.outfile


    
