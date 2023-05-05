#!/usr/bin/env python3
import sys, os, shutil, re
from numpy import *

def plot_nsekge(x, y):
   nf, nx = y.shape
   bottom = 0.; top = 1.
   left = 0.; right = 1.
   dx = '0.1'; dy = '0.1'
   
   os.system('gmtset PAPER_MEDIA a3')
   os.system('gmtset X_ORIGIN 3c')
   os.system('gmtset Y_ORIGIN 3c')
   os.system('gmtset BASEMAP_TYPE PLAIN')
   os.system('gmtset TICK_LENGTH 0')
   os.system('gmtset ANNOT_FONT_SIZE 18p')
   os.system('gmtset LABEL_FONT_SIZE 20p')
   os.system('gmtset LABEL_OFFSET 0.1c')
   os.system('gmtset MEASURE_UNIT inch')
   os.system('psbasemap -R'+str(left)+'/'+str(right)+'/'+str(bottom)+'/'+str(top)+' -JX7i/7i -Ba'+\
              dx+'g'+dx+':"@~r@~":/a'+dy+'g'+dy+':"Score Values":WeSn -Gwhite -K > graph.ps')
   
   for j in range(nf):
      graph_file=open('graph.txt', 'w')
      for i in range(nx):
         graph_file.write(str(x[i])+' '+str(y[j,i])+'\n')
      graph_file.close()
      os.system('psxy graph.txt -R -J -O -K -S'+symbol[j]+'0.1 -G'+color[j]+' >> graph.ps')
      os.system('psxy graph.txt -R -J -O -K -Wthickest,'+color[j]+' >> graph.ps')
   graph_file=open('graph.txt', 'w')
   graph_file.write(str(1/sqrt(2.))+' 0.\n')
   graph_file.write(str(1/sqrt(2.))+' 1.\n')
   graph_file.close()
   os.system('psxy graph.txt -R -J -O -K -Wthickest,black >> graph.ps')
   
   lgd_file = open('graph.lgd','w')
   lgd_file.write('C blue\n')
   for j in range(nf):
      lgd_file.write('S 0.1i '+symbol[j]+' 0.2i '+color[j]+' 0.20p 0.3i '+text[j]+'\n')
   lgd_file.close()
   os.system('pslegend -R -J -O -K -C0.05i/0.05i -D'+str(left)+'/'+str(top)+'/2.0i/2.0i/LT graph.lgd >> graph.ps')
   
   #os.system('echo "'+str(right)+' '+str(bottom)+' 36 0 4 RB (a)" | pstext -R -J -O -K -Dj0.1/0.1 -Gblack -N >> graph.ps')
   os.system('ps2raster -Tf graph.ps')
   os.system('convert -trim +repage +rotate 90 '+density+' graph.pdf graph.'+format)

# Test the functional forms of NSE and KGE
# Parameters
color = ['blue', 'red', 'green', 'orange', 'magenta', 'cyan', 'darkyellow']
symbol = ['C', 'S', 'T', 'A', 'T', 'A', 'I', 'D', 'N', 'H']
format = 'png'
density = '-density 300'

root_dir = '/home/leduc/paper'
output_dir = root_dir+'/nse'
work_dir = root_dir+'/work'
current_dir = os.getcwd()
os.chdir(work_dir)
os.system('rm -rf *')

nx = 100
x = linspace(0.01,1.,nx)
y = zeros((3,nx))
text = []
y[0] = 2. - 1./x**2
text.append('NSE@-u@-')
y[1] = x**2
text.append('NDE@-u@-')
y[2] = 1.-sqrt((x-1)**2+(1/x-1)**2)
text.append('KGE@-u@-')
plot_nsekge(x, y)
shutil.move('graph.'+format, output_dir+'/fig02.'+format)
