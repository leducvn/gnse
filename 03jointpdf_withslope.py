#!/usr/bin/env python3
import sys, os, shutil, re
from numpy import *

def plot_jointpdf(p):
   nf, np = p.shape
   bottom = -3.; top = 3.
   left = -3.; right = 3.
   dx = '1.'; dy = '1.'
   
   os.system('gmtset PAPER_MEDIA a3')
   os.system('gmtset X_ORIGIN 3c')
   os.system('gmtset Y_ORIGIN 3c')
   os.system('gmtset BASEMAP_TYPE PLAIN')
   os.system('gmtset TICK_LENGTH 0')
   os.system('gmtset ANNOT_FONT_SIZE 18p')
   os.system('gmtset LABEL_FONT_SIZE 20p')
   os.system('gmtset LABEL_OFFSET 0.1c')
   os.system('gmtset MEASURE_UNIT inch')
   os.system('psbasemap -R'+str(left)+'/'+str(right)+'/'+str(bottom)+'/'+str(top)+' -JX6i/6i -Ba'+\
              dx+'g'+dx+':"Observation":/a'+dy+'g'+dy+':"Simulation":WeSn -Gwhite -K > graph.ps')
   
   graph_file=open('graph.txt', 'w')
   for i in range(np): graph_file.write(str(p[0,i])+' '+str(p[1,i])+'\n')
   graph_file.close()
   os.system('psxy graph.txt -R -J -O -K -SC0.1 -Gblue >> graph.ps')
   graph_file=open('graph.txt', 'w')
   graph_file.write('-3 0\n')
   graph_file.write('3 0\n')
   graph_file.close()
   os.system('psxy graph.txt -R -J -O -K -Wthick,black >> graph.ps')
   graph_file=open('graph.txt', 'w')
   graph_file.write('0 -3\n')
   graph_file.write('0 3\n')
   graph_file.close()
   os.system('psxy graph.txt -R -J -O -K -Wthick,black >> graph.ps')
   
   #os.system('echo "'+str(0.5*(left+right))+' '+str(top)+' 26 0 4 CB '+text+'" | pstext -R -J -O -K -Dj0./0.1 -Gblue -N >> graph.ps')
   os.system('echo "'+str(left)+' '+str(top)+' 26 0 4 LT '+text+'" | pstext -R -J -O -K -Dj0.1/0.1 -Gblue -N >> graph.ps')
   #os.system('echo "'+str(right)+' '+str(bottom)+' 36 0 4 RB ('+label+')" | pstext -R -J -O -K -Dj0.1/0.1 -Gblack -N >> graph.ps')
   os.system('ps2raster -Tf graph.ps')
   os.system('convert -trim +repage +rotate 90 '+density+' graph.pdf graph.'+format)

# Test the pdf of truth, obs, fcst
# Parameters
np = 800
sigmao = 1.; meanf = meano = 0.; rho = 0.9
#text = 'Joint distribution @~r@~ = 0.9'
a = 0.5; label = 'a'
a = 1.0; label = 'b'; text2 = '@~s@~@-f@- = 1.0@~s@~@-o@-'
a = 2.0; label = 'c'; text2 = '@~s@~@-f@- = 2.0@~s@~@-o@-'
#sigmaf = a*sigmao/rho
text = '@~r@~ = '+'%3.1f'%rho+', a = '+'%3.1f'%a
color = ['red', 'blue', 'orange', 'green', 'magenta', 'cyan', 'darkyellow']
symbol = ['C', 'S', 'T', 'A', 'T', 'A', 'I', 'D', 'N', 'H']
format = 'png'
density = '-density 300'

root_dir = '/home/leduc/paper'
output_dir = root_dir+'/nse'
work_dir = root_dir+'/work'
current_dir = os.getcwd()
os.chdir(work_dir)
os.system('rm -rf *')

bias = meanf - a*meano
sigmam = sqrt(1./rho**2-1.)*a*sigmao
p = zeros((3,np))
p[0] = random.normal(meano,sigmao,np) # obs
p[2] = bias + random.normal(0.,sigmam,np) # noise
p[1] = a*p[0] + p[2] # fcst
plot_jointpdf(p)
shutil.move('graph.'+format, output_dir+'/fig03'+label+'.'+format)
