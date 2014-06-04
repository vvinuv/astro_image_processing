import pylab as pl
import numpy as np
from MatplotRc import *

#start_mysql -e "select c.petromag_r-c.extinction_r, c.z, a.n_bulge, f.flag from CAST as c, Flags_optimize as f, r_band_serexp as a where a.galcount=c.galcount and c.galcount = f.galcount and f.band='r' and f.ftype='u' and f.model='serexp';" > final_tab.txt

def get_hist(mags, flags, fchoice):
    mag_choice = np.extract(flags&fchoice>0,mags)
    vals, binedges = np.histogram(mag_choice, bins = 40, range=(14.0,18.0))
    vals = np.array(list(vals)+[0.0], dtype=float)
    return vals, binedges

fin_mag, finz, finn,flag = np.loadtxt('final_tab.txt', unpack =True, skiprows=1)
flag = flag.astype(int)

in_mag, inz = np.loadtxt('raw_tab.txt', unpack=True, skiprows=1)
in_vals,in_bin  = get_hist(in_mag, np.ones_like(in_mag).astype(int),1) 
in_vals[-1]=10000.0 # to make the step plot go to zero at the end.

figsize=get_fig_size()
figsize=(1.5*figsize[0],2.0*figsize[1])
fig = pl.figure(figsize=figsize)
ticks = pub_plots(xmaj=1,xmin=0.2,xstr='%d',ymaj=0.1,ymin=0.05,ystr='%0.1f')

outvals,outbin = get_hist(fin_mag, flag, 2**1+2**4+2**10+2**14+2**19)
pl.step(outbin, outvals/in_vals, color = 'k', ls='-', lw=2, 
label = 'fitted sample',where='post')

tmp_flag = np.where(finn>7.95, 1, 0)*(np.where(flag&2**1, 1, 0)|np.where(flag&2**10, 1, 0)|np.where(flag&2**10, 1, 0)|np.where(flag&2**14, 1, 0))

fclean = np.extract(tmp_flag==0,flag)
mclean = np.extract(tmp_flag==0,fin_mag)
 
outvals,outbin = get_hist(fin_mag, flag, 2**1+2**4+2**10+2**14)
pl.step(outbin, outvals/in_vals, color = 'r', ls=':', lw=2, 
label = 'full',where='post')

outvals,outbin = get_hist(fin_mag, flag, 2**1+2**4+2**10)
pl.step(outbin, outvals/in_vals, color = 'g', ls='-.', lw=2, 
label = 'intermediate',where='post')

outvals,outbin = get_hist(mclean, fclean, 2**1+2**4+2**10)
pl.step(outbin, outvals/in_vals, color = 'b', ls='--', lw=2, 
label = 'conservative',where='post')


#pl.title('completeness')
pl.xlim((14.0,17.8))
pl.ylim((0.35,1.0))
pl.xlabel('$m_{r,\ petro}$')
pl.ylabel('completeness')
ax = pl.gca()
ticks.set_plot(ax)
pl.subplots_adjust(left=0.15, right=0.95, bottom = 0.3)
pl.legend(loc='center',bbox_to_anchor=(0.75,0.25), fontsize=8)
pl.savefig('completeness.eps', bbox_inches='tight')
