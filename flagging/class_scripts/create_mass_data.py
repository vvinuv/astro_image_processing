import numpy as np
import scipy as sc
import pyfits as pf
import pylab as pl
import pickle
import os
import sys 

from astro_image_processing.mysql import *
#from gal_panel import *

model = 'serexp'
uname = 'alan'
cursor = mysql_connect('catalog','pymorph','pymorph','')

for band in 'r':
    cmd = """select x.galcount, z.Hrad_corr,z.BT, 
    z.m_tot-x.extinction_{band},  
    z.r_bulge*sqrt(z.ba_bulge), z.n_bulge, 
    z.r_disk*sqrt(z.ba_disk),
    s.kpc_per_arcsec, z.m_bulge-x.extinction_{band}, 
    z.m_disk-x.extinction_{band}, c.flag, s.dismod,
    x.modelmag_g - x.extinction_g, x.modelmag_r - x.extinction_r, 
    x.modelmag_i - x.extinction_i, 
    -2.5*log10(x.fracdev_r*pow(10, -0.4*x.devmag_r) + (1.0-x.fracdev_r)*pow(10, -0.4*x.expmag_r)) as cmodel_r,
    -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, 
    s.kcorr_g, s.kcorr_r, s.kcorr_i,j.Mstar_med, 1.0/s.Vmax
    from 
    Flags_catalog as c,
    M2010 as m,  
    DERT as s,
    CAST as x,
    {band}_band_fit as y,
    {band}_band_{model} as z LEFT JOIN JHU_masses as j on z.galcount=j.galcount
     where 
    y.galcount = x.galcount and
    x.galcount = s.galcount and 
    x.galcount = z.galcount and 
    x.galcount = m.galcount and
    x.galcount = c.galcount and
    c.band = '{band}' and c.model = '{model}' and
    c.ftype = 'u' and j.Mstar_med>0 and s.Vmax>0
    order by 
    x.galcount;""".format(model = model, band = band)

    # , r_lackner_fit as a 
    # x.galcount = a.galcount and


    data = cursor.get_data(cmd)

    data = [np.array(d) for d in data]

    pos_dict = dict([(a[0],a[1]) for a in zip(['galcount', 'hrad_corr', 'BT',
                                          'mag', 'r_bulge','n_bulge',
                                          'r_disk', 'kpc_per_arcsec', 
                                          'm_bulge', 'm_disk', 
                                          'flag','dismod', 'modelg','modelr',
                                          'modeli', 'cmodelr',
                                               'ttype', 'kg', 'kr', 'ki',
                                               'mstar','vweight'
                                               ], data)])

    outfile = open('./mass_file_{band}.npz'.format(band=band), 'w')
    np.savez(outfile, **pos_dict)
    outfile.close()

