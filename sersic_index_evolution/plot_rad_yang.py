import pylab as pl
import numpy as np
from mysql_class import *
from bin_stats import *
from MatplotRc import *
from matplotlib.font_manager import FontProperties
dba = 'catalog'
usr = 'ameert'
pwd = 'al130568'

cursor = mysql_connect(dba, usr, pwd)


size = get_fig_size()
size[0] *=2
size[1] *=6 

fig = pl.figure(figsize=size, frameon=True)
ticks = pub_plots(xmaj = 1,xmin=0.5,xstr= '%d',ymaj = 1,ymin = 0.25,ystr='%d')
#pl.subplots_adjust(left = 0.2, right = 0.95, bottom = 0.35,top = 0.87, wspace = 0.15, hspace = 0.15) 
pl.subplots_adjust(left = 0.1, right = 0.9, bottom = 0.1,top = 0.92, wspace = 0.15, hspace = 0.4) 


gals = {}
delta_M = 0.5
save_stem = 'massive'

for add_con, pos, title in zip(['', ' and d.groupID >0 and d.most_massive = 1 and d.group_counts > 1 ',' and d.groupID >0 and d.most_massive = 2  and d.group_counts > 1 '],[1,2,3],['all', 'centrals', 'satellites']):
    fig.add_subplot(3,1,pos)
    for mrange, color in zip(np.arange(11.0, 15.01, delta_M), ['k', 'b','c','g','y', 'm','#FFA500','r']):
        try:
            cmd = "select a.galcount, log10(a.re_kpc*sqrt(a.eb)), log10(b.re_kpc*sqrt(a.eb)), log10(c.re_kpc*sqrt(a.eb)), m.probaE, m.probaEll, m.probaS0, m.probaSab, m.probaScd, d.brightest, d.most_massive, d.L_group, d.Mstar_group,d.HaloMass_1, d.HaloMass_2, f.Mstar_med_shift from full_dr7_g_ser as a,full_dr7_r_ser as b,full_dr7_i_ser as c, M2010 as m, yang.yang_groupsC as d, JHU.JHU_masses as f where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = f.galcount and b.z<0.09 and b.manual_flag = 0 and b.fitflag = 0 and  m.probaE >=0.8 and abs(d.group_Z - b.z) <= 0.01 and d.fedge>=0.6 %s and d.HaloMass_1 between %f and %f;" %(add_con, mrange, mrange+delta_M)
#            cmd = "select a.galcount, log10(a.re_kpc),log10(b.re_kpc*b.hrad_pix_baavg/b.re_pix),log10(c.re_kpc), m.probaE, m.probaEll, m.probaS0, m.probaSab, m.probaScd, d.brightest, d.most_massive, d.L_group, d.Mstar_group,d.HaloMass_1, d.HaloMass_2, f.Mstar_med_shift from full_dr7_g_ser as a,full_dr7_r_ser as b,full_dr7_i_ser as c, M2010 as m, yang.yang_groupsC as d, JHU.JHU_masses as f where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = f.galcount and b.z<0.09 and b.manual_flag = 0 and b.fitflag = 0 and  m.probaE >=0.8 and abs(d.group_Z - b.z) <= 0.01 and d.fedge>=0.6 %s and d.HaloMass_1 between %f and %f;" %(add_con, mrange, mrange+delta_M)

            print cmd
            data = cursor.get_data(cmd)

        except IndexError:
            continue
    
        for d, dname in zip(data, ['galcount','n_g', 'n_r', 'n_i', 'PEarly', 
                                   'PEll','PS0',
                                   'PSab','PScd','brightest', 'most_massive', 
                                   'L_group','Mstar_group','HaloMass_1', 
                                   'HaloMass_2', 'logMstar']):
            gals[dname] = np.array(d)
        print len(gals['galcount'])
        gals['PLate'] = gals['PSab']+gals['PScd']
        gals['P1'] = np.array([1])

        for ckey,ls in zip(['P1','PEll','PS0'],['-']):#,'--', ':']):
            a = bin_stats(gals['logMstar'],gals['n_r'],
                          np.arange(7.0,16.01,0.5), -1.0,3.0, weight = gals[ckey], 
                          err_type = 'median')
            a.plot_ebar('median', '68n', marker = 'o',color = color, ms = 1, 
                        markerfacecolor = color,  ecolor = color, capsize = 5, 
                        linestyle = ls, elinewidth = 2, barsabove=True, 
                        zorder = 1, label='%.1f<M$_{halo}$<%.1f'%(mrange, mrange+delta_M))
            a.lay_bounds(color=color, sigma_choice = [68])
            for b1,b2,b3 in zip(a.bin_ctr,a.bin_median,a.bin_number):
                print 1.5*np.log(float(b3))
                pl.plot(b1,b2,marker = 'o', color = color, 
                        ms = 1.5*np.log(float(b3)))
    
    for size in [10,100,1000,10000]:
        pl.plot(-100,-100,marker = 'o', color = 'r', 
                 ms = 1.5*np.log(float(size)), label = str(size))

    pl.title(title)
    ax = fig.gca()
    ax.set_aspect('auto')
    ticks.set_plot(ax)
    pl.xlabel('log$_{10}$(M$_{*}$/M$_{sun}$)')
    pl.ylabel('log$_{10}$R$_{r,\ kpc}$')
    pl.xlim((9,12))
    pl.ylim((0,1.5))
    
handles, labels = ax.get_legend_handles_labels()
legend_font_props = FontProperties()
legend_font_props.set_size('small')
l1 = pl.legend(handles[0:-4:1],labels[0:-4:1], bbox_to_anchor=(0, 0,1, 1), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':6})
l2 = pl.legend(handles[-4::1],labels[-4::1], bbox_to_anchor=(0, .8,.2, .2), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':10}, numpoints = 1)
pl.gca().add_artist(l1)
pl.savefig("./rad_yang_%s_few.eps" %save_stem, format = 'eps')
pl.close(fig)





 
