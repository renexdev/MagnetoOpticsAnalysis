#!/usr/bin/env python
s = "Rene Cejas Bolecek\n\
reneczech@gmail.com / ncejas@cab.cnea.gov.ar\n\
Low Temperatures Laboratory, Centro Atomico Bariloche\n\
Instituto Balseiro, Universidad Nacional de Cuyo\n\
Avenida Bustillo 9500, 8400 Bariloche, Rio Negro, Argentina\n\
MIT License\n\
"
s1 = "Graphs: profiles for increasing a decreasing field + B vs H + Magnetization loops\n\
Output: save B vs H + Magnetization loops for selected points\n\
Input: matlab profiles\n"
#libraries
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from numpy.random import uniform, seed
from numpy import zeros, sqrt, where, pi, average, arange
import pylab


#Choose units
flag_px = 1 #pxunits
flag_um = 0 #umunits
#moves relative scale to 0 (set as 1)
flag_absolute_scale = 0
#enable some prints
flag_initial_print = 1
flag_debugging = 1
flag_external =1
#Offset for printing
offset_y_inf = -10
offset_y_sup = 10
#filenames
tempID = "08.0"
discoId = "1"
diskSize= "_50um"
profile_direction="v" #h: horizontal, v=vertical
filename01=tempID+"K_20x_01_d"+discoId+"_gauss_"+profile_direction+"_01"
filename02=tempID+"K_20x_01_d"+discoId+"_gauss_"+profile_direction+"_02"
external_feed="d0"+discoId+diskSize+"_Coordinates_Hyst_"+tempID+"K_20x_01"

#20x Leica magnification 
px2um = 0.493  


#IF U DONT HAVE EXTERNAL FILE set flag_external to 0 and fill these vectors
#choose disk boundaries in PX
p_disk = [140, 260]  #JUST an initial value
#choose positions in PX
p0 = [170.0, 193.0,216.0]   #JUST an initial value
#fraction of disk?
#p0= [p_disk[0]+delta_disk_size,p_disk[0]+2*delta_disk_size,p_disk[0]+3*delta_disk_size]
#choose colors
colors = ["blue","green","red"]

####################################################################################################################
#Some debugging & prints
if(flag_initial_print):
	print s
	print s1
if(flag_absolute_scale == 1):
	print "You have turned ON relative scale"
if(flag_external == 1):
	print "You have turned ON external parameters use input.dat"

if ((flag_px==1) and (flag_um==flag_px)):
	raise  RuntimeError ("Choose one length scale: px or um not both in 1")
if ((flag_px==0) and (flag_um==flag_px)):
	raise  RuntimeError ("Choose one length scale: px or um. One option has to be setted with value 1")


############################################################################################################
fn = filename01.split('_')
data01   = np.loadtxt(filename01+'.dat')
data02   = np.loadtxt(filename02+'.dat')

if(flag_external):
	params01   = np.loadtxt(external_feed+'.dat')
	print params01
	#0: disk_ID
	#1: x0
	#2: y0
	#3: x1
	#4: y1
	#5: param_n_x
	#6: param_n_x
	#7: param_m_x
	#8: param_m_y
	if(profile_direction=="h"):
		p_disk = [params01[1], params01[3]] 
	if(profile_direction=="v"):
		p_disk = [params01[2], params01[4]] 
	if(profile_direction == "h"):
		print "with HORIZONTAL direction"
		print "disk_left (px):",p_disk[0]
		print "disk_rigth (px):",p_disk[1]
	if(profile_direction == "v"):
		print "with VERTICAL direction"
		print "disk_up (px):",p_disk[0]
		print "disk_down (px):",p_disk[1]
	delta_disk_size = (p_disk[1]-p_disk[0])/4.0
	p0= [int(p_disk[0]+delta_disk_size),int(p_disk[0]+2*delta_disk_size),int(p_disk[0]+3*delta_disk_size)]
	print "VER ACA: ",p0
	#choose positions in PX

if (flag_debugging):
	print "row length",len(data01[0,:]) #row length 
	print "column length",len(data01[:,0]) #columns length

Ha01 = zeros(len(data01[0,:])-1)
x01 = zeros(len(data01[:,0])-1)
B01 = zeros((len(data01[:,0])-1,len(data01[0,:])-1),float)

Ha02 = zeros(len(data02[0,:])-1)
x02 = zeros(len(data02[:,0])-1)
B02 = zeros((len(data02[:,0])-1,len(data02[0,:])-1),float)



for i01 in range(1,len(data01[0,:])):
	Ha01[i01-1] = data01[0,i01]

for i01 in range(1,len(data01[:,0])):
	x01[i01-1] = data01[i01,0]
print x01
decimal_correction = x01[0]-int(x01[0])

if(flag_debugging):
	print "decimal correction:",decimal_correction

if(flag_um==1):
	x01*= px2um
#initializ
x01_offset =0
x02_offset = 0

if(flag_absolute_scale==1):
	x01_offset=min(x01)
	x01 = x01 - min(x01)
		
mag_inf01 = 0
mag_sup01 = 0

for i01 in range(1,len(data01[:,0])):
	for i02 in range(1,len(data01[0,:])):
		B01[i01-1,i02-1] = data01[i01,i02]

		
for i01 in range(1,len(data02[0,:])):
	Ha02[i01-1] = data02[0,i01]
for i01 in range(1,len(data02[:,0])):
	x02[i01-1] = data02[i01,0]


if(flag_um==1):
	x02 *= px2um
			

if(flag_absolute_scale==1):
	x02_offset=min(x02) #same as x01_offset
	if(x02_offset!=x01_offset):
		raise  RuntimeError ("Different files token")
		
	x02 -= x02_offset
mag_inf02 = 0
mag_sup02 = 0
	
for i01 in range(1,len(data02[:,0])):
	#for i02 in range(1,2):
	for i02 in range(1,len(data02[0,:])):
		B02[i01-1,i02-1] = data02[i01,i02]

		#print B[i01-1,i02-1]


if(flag_um):
	for i01 in range(len(p_disk)):
		p_disk[i01] *= px2um
if(flag_absolute_scale):
	for i01 in range(len(p_disk)):
		p_disk[i01] -= x01_offset

disk_size = p_disk[1]-p_disk[0]
print "disk size:",disk_size

for i01 in range(len(p0)):
		p0[i01] += decimal_correction
if(flag_um):
	for i01 in range(len(p0)):
		p0[i01] *= px2um
if(flag_absolute_scale):
	for i01 in range(len(p0)):
		p0[i01] -= x01_offset
		
#initialization

sol01 =zeros(len(p0))
sol02 =zeros(len(p0))
############################################################################################################
######Profiles increasing field
f1 = pylab.figure()
ax1 = f1.add_subplot(111)
if(flag_um):
	pylab.title(fn[0]+'\n'+'Increasing $H_a$: %.2f - %.2f' % (Ha01[0] ,Ha01[len(Ha01)-1])+'\n'+'size: %.2f $\mu m$' %(disk_size))
	pylab.xlabel('Position $\mu m$')
if(flag_px):
	pylab.title(fn[0]+'\n'+'Increasing $H_a$: %.2f - %.2f' % (Ha01[0] ,Ha01[len(Ha01)-1])+'\n'+'size: %.2f px' %(disk_size))
	pylab.xlabel('Position px')

pylab.ylabel('B (Gauss)')
for i01 in range(len(p0)):
	ax1.plot([p0[i01],p0[i01]],[-500,500],lw=1.5,c = colors[i01])
	#print p0[i01]
for i01 in range(len(p_disk)):
	ax1.plot([p_disk[i01],p_disk[i01]],[-500,500],color="black",lw=1.5)
	#print p_disk[i01]

			
for i01 in range(0,len(B01[0,:])):
	if(flag_um):
		ax1.plot(x01,B01[:,i01],lw=1.5)
	if(flag_px):
		ax1.plot(x01,B01[:,i01],lw=1.5)
print x01
ax1.set_xlim(min(x01),max(x01))
ax1.set_ylim(-100,500)		
f1.savefig(filename01+"_profiles.png")
############################################################################################################
######Profiles increasing field
f2 = pylab.figure()
ax2 = f2.add_subplot(111)
for i01 in range(len(p0)):
	ax2.plot([p0[i01],p0[i01]],[-500,500],lw=1.5)

if(flag_um):	
	pylab.title(fn[0]+'\n'+'Decreasing $H_a$: %.2f - %.2f' % (Ha01[len(Ha01)-1],Ha01[0])+'\n'+'size: %.2f $\mu m$' %(disk_size))
	pylab.xlabel('Position $\mu m$')
for i01 in range(0,len(B02[0,:])):
	ax2.plot(x02,B02[:,i01],lw=1.5)

ax2.set_xlim(min(x02),max(x02))
ax2.set_ylim(-100,500)		
f2.savefig(filename02+"_profiles.png")
for i01 in range(len(p0)):
		ax2.plot([p0[i01],p0[i01]],[-500,500],lw=1.5,c = colors[i01])
for i01 in range(len(p_disk)):
		ax2.plot([p_disk[i01],p_disk[i01]],[-500,500],color="black",lw=1.5)	
if(flag_px):

	pylab.title(fn[0]+'\n'+'Decreasing $H_a$: %.2f - %.2f' % (Ha01[len(Ha01)-1],Ha01[0])+'\n'+'size: %.2f px' %(disk_size))
	pylab.xlabel('Position px')
	for i01 in range(0,len(B02[0,:])):
		ax2.plot(x02,B02[:,i01],lw=1.5)
	ax2.set_xlim(min(x02),max(x02))
	ax2.set_ylim(-100,500)		
pylab.ylabel('B (Gauss)')	
f2.savefig(filename02+"_profiles.png")
############################################################################################################
######Magnetization looops
f3 = pylab.figure()
ax3 = f3.add_subplot(111)

ax3.plot([0,500],[0,0], c ="black",lw=0.5)
ax3.plot([0,500],[0,-500], c ="black",lw=0.5)

h_inf = 0
h_sup = 0 
b_inf= 0
b_sup= 0
m_inf=0
m_sup =0
delta_px = 1 #sensitivity in px
print "p0",p0,"len: ",len(p0)
for i01 in range(3):
	print i01
	if(flag_um):
		f_write_03 = open(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"_pos_%d"%p0[i01]+"um_offset_%d"%x01_offset+"um.dat", "w")
	if(flag_px):
		f_write_03 = open(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"_pos_%d"%p0[i01]+"px_offset_%d"%x01_offset+"px.dat", "w")
	for i02 in range(len(x01)):
		#print "x0:",x01[i02]
		if(x01[i02]==p0[i01]):
			sol01[i01]=i02
			if(flag_debugging):
				print "Index:",i02
				print "x01[",i02,"]",x01[i02]
				print "p0[",i01,"]",p0[i01]
			
	if(flag_um):
		ax3.plot(Ha01,B01[sol01[i01],:]-Ha01, marker ='o',c =colors[i01],lw=1.5,label='%s $\mu m$' %(p0[i01]))
	if(flag_px):
		ax3.plot(Ha01,B01[sol01[i01],:]-Ha01, marker ='o',c =colors[i01],lw=1.5,label='%s px' %(p0[i01]))
	#marker ='o'
	#markerfacecolor='None'
	#alpha=0.3
	#linestyle='--'
	for i04 in range(len(Ha01)):
		f_write_03.write("%f %f\n" % ((Ha01[i04],B01[sol01[i01],i04]-Ha01[i04])))
		if(h_inf>Ha01[i04]):
			h_inf=Ha01[i04]
		if(h_sup<Ha01[i04]):
			h_sup=Ha01[i04]
		if(b_inf>B01[sol01[i01],i04]):
			b_inf=B01[sol01[i01],i04]
		if(b_sup<B01[sol01[i01],i04]):
			b_sup=B01[sol01[i01],i04]
		if(m_inf>B01[sol01[i01],i04]-Ha01[i04])	:
			m_inf=B01[sol01[i01],i04]-Ha01[i04]
		if(m_sup<B01[sol01[i01],i04]-Ha01[i04])	:
			m_sup=B01[sol01[i01],i04]-Ha01[i04]
	for i03 in range(len(x02)):
		if(x02[i03]==p0[i01]):
			if(flag_debugging):
				print "Index:",i03
				print "x02[",i03,"]",x02[i03]
			sol02[i01]=i03
	
	ax3.plot(Ha02,B02[sol02[i01],:]-Ha02,marker ='o',ms=8,c = colors[i01],lw=1.5)
	ax3.plot(Ha02,B02[sol02[i01],:]-Ha02, marker ='o',ms=5,c="white",lw=0)
	for i04 in range(len(Ha02)):
		f_write_03.write("%f %f\n" % ((Ha02[len(Ha02)-1-i04],B02[sol02[i01],len(Ha02)-1-i04]-Ha02[len(Ha02)-1-i04])))
		if(h_inf>Ha02[len(Ha02)-1-i04]):
			h_inf=Ha02[len(Ha02)-1-i04]
		if(h_sup<Ha02[len(Ha02)-1-i04]):
			h_sup=Ha02[len(Ha02)-1-i04]
		if(b_inf>B02[sol02[i01],len(Ha02)-1-i04]):
			b_inf=B02[sol02[i01],len(Ha02)-1-i04]
		if(b_sup<B02[sol02[i01],len(Ha02)-1-i04]):
			b_sup=B02[sol02[i01],len(Ha02)-1-i04]
		if(m_inf>B02[sol02[i01],len(Ha02)-1-i04]-Ha02[len(Ha02)-1-i04]):	
			m_inf=B02[sol02[i01],len(Ha02)-1-i04]-Ha02[len(Ha02)-1-i04]
		if(m_sup<B02[sol02[i01],len(Ha02)-1-i04]-Ha02[len(Ha02)-1-i04]):	
			m_sup=B02[sol02[i01],len(Ha02)-1-i04]-Ha02[len(Ha02)-1-i04]	
	pylab.title(fn[0])
	ax3.set_xlim(0,550)
	ax3.set_ylim(m_inf+offset_y_inf,m_sup+offset_y_sup)
	pylab.legend()
	pylab.xlabel('H (Oe)')
	pylab.ylabel('B (Gauss) - H (Oe)')
	f_write_03.close()

f3.savefig(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"_loops.png")
############################################################################################################
######BvsH
f4 = pylab.figure()
ax4 = f4.add_subplot(111)

ax4.plot([0,500],[0,500], c ="black",lw=0.5)

for i01 in range(len(p0)):
	if(flag_um):
		f_write_04 = open(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"BvsH_pos_%d"%p0[i01]+"um_offset_%d"%x02_offset+"um.dat", "w")
	if(flag_px):
		f_write_04 = open(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"BvsH_pos_%d"%p0[i01]+"um_offset_%d"%x02_offset+"um.dat", "w")
	
	for i02 in range(len(x01)):
		if(x01[i02]==p0[i01]):
			if(flag_debugging):
				print "Index:",i02
				print "x01[",i02,"]",x01[i02]
			sol01[i01]=i02
	if(flag_um):
		ax4.plot(Ha01,B01[sol01[i01],:], marker ='o',c =colors[i01],lw=1.5,label='%s $\mu m$' %(p0[i01]))
	if(flag_px):
		ax4.plot(Ha01,B01[sol01[i01],:], marker ='o',c =colors[i01],lw=1.5,label='%s px' %(p0[i01]))

	for i04 in range(len(Ha01)):
		f_write_04.write("%f %f\n" % ((Ha01[i04],B01[sol01[i01],i04])))
	for i03 in range(len(x02)):
		if(x02[i03]==p0[i01]):
			if(flag_debugging):
				print "Index:",i03
				print "x02[",i03,"]",x02[i03]
			sol02[i01]=i03
	ax4.plot(Ha02,B02[sol02[i01],:], marker ='o',ms=8,c = colors[i01],lw=1.5)
	ax4.plot(Ha02,B02[sol02[i01],:], marker ='o',ms=5,c="white",lw=0)

	for i04 in range(len(Ha02)):
		f_write_04.write("%f %f\n" % ((Ha02[len(Ha02)-1-i04],B02[sol02[i01],len(Ha02)-1-i04])))

	pylab.title(fn[0])
	ax4.set_xlim(0,500)
	ax4.set_ylim(b_inf,b_sup)
	pylab.legend()
	pylab.xlabel('H (Oe)')
	pylab.ylabel('B (Gauss)')
	f_write_04.close()

f4.savefig(fn[0]+fn[1]+fn[2]+fn[3]+fn[4]+"_BvsH.png")
if(flag_debugging):
	print "sol01:",sol01
	print "sol02:",sol02
############################################################################################################
#Show results

pylab.show()	



