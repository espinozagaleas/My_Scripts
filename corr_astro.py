import subprocess
import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

obsid = sys.argv[1]
par1 = sys.argv[2]
par2 = sys.argv[3]
row = sys.argv[4]
#obsid = 1012010101
#par1 = 'time'
#par2 = 'MPU_A_TEMP'
#row = '0,1,2'
par1 = par1.upper()
par2 = par2.upper()
rows=row.split(',')
path_hk = './'+str(obsid)+'/xti/hk/'

fig = plt.figure()

for n in rows:
    cmd_hk = path_hk+'ni'+str(obsid)+'_0mpu'+n+'.hk.gz'
    hk = fits.open(cmd_hk)
    data_hk = hk[1].data
    par1_hk = data_hk[par1]
    par2_hk = data_hk[par2]
    unit_par1 = data_hk.columns[par1].unit
    unit_par2 = data_hk.columns[par2].unit
    plt.plot(par1_hk,par2_hk,label='mpu'+n)
    if not unit_par1:
        unit_par1='no\, units'
    if not unit_par2:
        unit_par2='no\, units'
    plt.xlabel(par1+' ($'+unit_par1+'$)')
    plt.ylabel(par2+' ($'+unit_par2+'$)')
    plt.legend()

path_cl = './'+str(obsid)+'/xti/event_cl/'

if par1 == 'TIME':
    opt_lc = raw_input('Do you want to plot light curve? (yes/no)')
    if opt_lc == 'yes':
        xselect=subprocess.Popen(['xselect'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        xselect.stdin.write('session1\n')
        xselect.stdin.write('read events '+path_cl+'ni'+str(obsid)+'_0mpu7_cl.evt\n')
        xselect.stdin.write('./\n')
        xselect.stdin.write('yes\n')
        xselect.stdin.write('extract curve\n')
        xselect.stdin.write('save curve '+path_cl+'ni'+str(obsid)+'.lc\n')
        xselect.stdin.write('exit\n')
        xselect.stdin.write('no\n')
        xselect.wait()

        cmd_lc = path_cl+'ni'+str(obsid)+'.lc'
        lc = fits.open(cmd_lc)
        tstart = lc[1].header['TSTART']
        data_lc = lc[1].data
        time_lc = tstart + data_lc['TIME']
        unitrate = '$'+data_lc.columns['RATE'].unit+'$'
        rate_lc = data_lc['RATE']
        subprocess.Popen('rm '+path_cl+'ni'+str(obsid)+'.lc',shell=True)
        plt.twinx()
        plt.ylabel('RATE ('+unitrate+')')
        plt.plot(time_lc,rate_lc,'--',c='k',label='lc')
        plt.legend(loc=2)
        
plt.title('HK File PLOT')
plt.show()
opt_eps = raw_input('Do you want to make a EPS file? (yes/no)')
if opt_eps == 'yes':
    fig.savefig('HK_PLOT.eps')
