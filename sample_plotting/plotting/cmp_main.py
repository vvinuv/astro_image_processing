
# standard python code imports
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages

# my personal code imports 
from astro_image_processing.mysql import *
from cmp_functions import *
from astro_image_processing.MatplotRc import *
from plot_info import *
from get_data import *


options = get_options_main()

if options['model2']==None:
    options['model2']=options['model1']

cursor = mysql_connect('catalog','pymorph','pymorph','')

data = get_data(cursor, '%s_%s_%s' %(options['band1'], options['table1'],options['model1']), '%s_%s_%s' %(options['band2'], options['table2'],options['model2']), options['band1'],options['band2'],flags = options['use_flags'], flagmodel = options['flagmodel'], add_tables = options['add_tables'], conditions = options['conditions'])

print 'num_objects: ', len(data['galcount'])
print data[options['xchoice']+'_1'],data[options['ychoice']+'_1'],data[options['ychoice']+'_2']

# we want radial differences in percents
# this sets up the calculation so that the plotting below works
for name in ['hrad', 'rbulge', 'rdisk', 'petrorad']:
    data[name+'_2'] =  (data[name+'_2']/data[name+'_1'])-1.0 +data[name+'_1']
#    data[name+'_2'] =  1.0-(data[name+'_1']/data[name+'_2'])+data[name+'_1'] 

for posnum in ['1','2']:
    if options['model%s' %posnum] == 'dev':
        if options['table%s' %posnum] in ['sdss', 'lackner']:
            data['mtot_%s' %posnum] = data['mtot_%s' %posnum]-0.071648 #corrects for mag offset due to truncation
            data['mtot_abs_%s' %posnum] = data['mtot_abs_%s' %posnum]-0.071648
    if options['model%s' %posnum] == 'exp':
        if options['table%s' %posnum] in ['sdss', 'lackner']:
            data['mtot_%s' %posnum] = data['mtot_%s' %posnum]-0.0103 #corrects for mag offset due to truncation
            data['mtot_abs_%s' %posnum] = data['mtot_abs_%s' %posnum]-0.0103


    if options['model%s' %posnum] == 'devexp':
        if options['table%s' %posnum] in ['lackner']:
            data['mbulge_%s' %posnum] = data['mbulge_%s' %posnum]-0.071648 #corrects for mag offset due to truncation
            data['mdisk_%s' %posnum] = data['mdisk_%s' %posnum]-0.0103 #corrects for mag offset due to truncation

            data['mtot_%s' %posnum] = -2.5*np.log10(10**(-0.4*data['mdisk_%s' %posnum])+10**(-0.4*data['mbulge_%s' %posnum]))
            data['mtot_abs_%s' %posnum] = data['mtot_%s' %posnum] - data['magcorr%s' %posnum]
            data['surf_bright_%s' %posnum] = -2.5*np.log10(10**(-0.4*data['mtot_%s' %posnum])/(2.0*np.pi*data['hrad_%s' %posnum]**2))
    

data['sky_1'] =100.0*( 10.0**(-0.4*(data['sky_1']-data['sky_2']))-1) # quote sky in percent difference
data['sky_2'] = 0.0*data['sky_2'] # makes sky on the y axis work 

print data[options['xchoice']+'_1'],data[options['ychoice']+'_1'],data[options['ychoice']+'_2']

#do plot
oplot = outlier_fig()

if options['xtmaj']!=None:
    ticksx[options['key_x']][0] = options['xtmaj']
if options['xtmin']!=None:
    ticksx[options['key_x']][1] = options['xtmin']
if options['xtlab']!=None:
    ticksx[options['key_x']][2] = options['xtlab']
if options['ytmaj']!=None:
    ticksy[options['key_y']][0] = options['ytmaj']
if options['ytmin']!=None:
    ticksy[options['key_y']][1] = options['ytmin']
if options['ytlab']!=None:
    ticksy[options['key_y']][2] = options['ytlab']


oplot.set_ticks(ticksx[options['key_x']][0], ticksx[options['key_x']][1], ticksx[options['key_x']][2], 
                ticksy[options['key_y']][0], ticksy[options['key_y']][1], ticksy[options['key_y']][2])
#oplot.setdenselims(1,options['upper_dense'] )
#oplot.setminval(0.01*options['upper_dense'])
oplot.setdenselims(0.000025*len(data['galcount']),0.0025*len(data['galcount']))
oplot.setminval(0.00001*len(data['galcount']))
#oplot.makeplot(data[options['xchoice']+'_1'],data[options['ychoice']+'_1']-data[options['ychoice']+'_2'], xlims[options['xchoice']],

if options['xlims']!= None:
    xlims[options['xchoice']]=options['xlims']
if options['ylims']!= None:
    ylims[options['ychoice']]=options['ylims']

oplot.makeplot(data[options['xchoice']+'_1'],data[options['ychoice']+'_1']-data[options['ychoice']+'_2'], xlims[options['xchoice']],
              ylims[options['ychoice']]) 

if options['model1'] == 'ser':
    if options['ychoice'] == 'nbulge':
        ylabs[options['ychoice']]=ylabs[options['ychoice']].replace('bulge', 'ser')

if options['xlab']!= None:
    xlabs[options['xchoice']]=options['xlab']
if options['ylab']!= None:
    ylabs[options['ychoice']]=options['ylab']
if options['bins']!= None:
    bins[options['key_x']]=options['bins']

print bins[options['key_x']]

pl.xlabel(xlabs[options['xchoice']].replace('{band}', options['band1']), fontsize=10)
pl.ylabel(ylabs[options['ychoice']].replace('{band}', options['band2']), fontsize=10)
oplot.bin_it(bins[options['key_x']], bin_lims[options['key_x']][options['key_y']][0],
            bin_lims[options['key_x']][options['key_y']][1])
oplot.add_bars('r')
pl.plot(pl.xlim(), [0,0], 'k-')

if ">=" in options['title']:
    options['title'] = options['title'].replace(">=","$\\geq$")

pl.title(options['title'], fontsize=8)

pl.text(-16, 1.0, options['postfix'].split('_')[1], fontsize=12)
print '%s_%s_%s_%s_%s_%s_%s%s.eps' %(options['band1'], options['table1'],options['band2'],options['table2'], options['model2'], options['xchoice'], options['ychoice'], options['postfix'])
#pl.show()
oplot.savefig('%s_%s_%s_%s_%s_%s_%s%s.eps' %(options['band1'], options['table1'],options['band2'],options['table2'], options['model2'], options['xchoice'], options['ychoice'], options['postfix']))


