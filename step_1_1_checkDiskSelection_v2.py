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
from numpy import zeros, sqrt, where, pi, average, arange
import ImageFont, ImageDraw, Image
import glob
import re
import os
import shutil

files = glob.glob('*.jpg')  # get *.JPG in a list (not sorted!)

#diskId = 'd07_70um'
#diskId = 'd06_70um'
#diskId = 'd05_60um'
#diskId = 'd03_40um'
#diskId = 'd02_30um'
diskId = 'd06_70um'
tmp = '30.0K'
external_feed=diskId+"_Coordinates_Hyst_"+tmp+"_20x_01"
external_bkg=diskId+"_Hyst_"+tmp+"_20x_01_bkgId_2"

#Drawing options
flag_draw_material =0
flag_draw_profile=1#profile parametrizado
flag_draw_circle =1 #encierra el circulo
flag_draw_calculated_profile =1# muestra el perfil calculado o sea la linea h y v
flag_draw_bkg =1 #el background
flag_draw_material_circunscripto =1 #sobre el que promedia
#External parameters input 
flag_external =1

#ax =145
#by =77
#cx =241
#dy =170
#bkgx = 323 
#bkgy = 81
#averaged background area!
#dbkg_x = 50
#dbkg_y = 50
#param_n_x=0.50 #pertentage of diameter in x dir param_n_x=0.30 is the 30%
#param_n_y=0.50 #pertentage of diameter in y dir param_n_x=0.30 is the 30%

#param_m_x=2 #integer times of radius for making profile in x dir 
#param_m_y=1.5 #integer times of radius for making profile in y dir

disk_bounds = zeros(4)
bkg_bounds = zeros(2)
#disk_bounds = [ax,by,cx,dy]
#bkg_bounds = [bkgx, bkgy]

if(flag_external):
	params01   = np.loadtxt(external_feed+'.dat')
	params_bkg   = np.loadtxt(external_bkg+'.dat')
	#disk_id
	#x0
	#y0
	#x1
	#y1
	#param_n_x
	#param_n_y
	#param_m_x
	#param_m_y
	disk_bounds =[params01[1], params01[2], params01[3], params01[4]]
	param_n_x = params01[5]
	param_n_y = params01[6]
	param_m_x = params01[7]
	param_m_y = params01[8]
	bkg_bounds = [params_bkg[0], params_bkg[1]]
	dbkg_x = params_bkg[2]
	dbkg_y = params_bkg[3]

	#choose positions in PX
d_disk = [disk_bounds[2]-disk_bounds[0],disk_bounds[3]-disk_bounds[1]]
area_square = d_disk[0]*d_disk[1]*param_n_x*param_n_y
disk_size_av = (d_disk[0]+d_disk[1])*0.5
#draw the disk box
xcm=(disk_bounds[0]+d_disk[0]/2)
ycm=(disk_bounds[1]+d_disk[1]/2)

ex,ey= d_disk[0]/2,d_disk[1]/2
bbox = (xcm-ex, ycm-ey,	xcm+ex, ycm+ey)

ex_profile,ey_profile= d_disk[0]*param_m_x/2,d_disk[1]*param_m_x/2
bbox_profile = (xcm-ex_profile, ycm-ey_profile,	xcm+ex_profile, ycm+ey_profile)
#print bbox_profile
print files
#files.sort()                # sort the list _in place_
cnt = 1                    # start new names 

#font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf",40)

#tcolor = (255,0,0)


for f in files:
    original = f      
    img = Image.open(f)  # save the original file name
    print f
    y = f.split(';')
    #print y[0],y[1]
    #intval = int(y[0])
    #y1 = y[1].split('G')
    #text = "%s" % y1[0]+"Oe"
    #text1 = "Laboratoire des Solides Irradies. Ecole Polytechnique, France"
    #text2 = "Low Temperatures Laboratory. CAB, Argentina"
    width, height = img.size
    #print "w x h: ",width, height
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf",25)
    #font1 = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansCondensed-Bold.ttf",25)
    #draw.text(text_pos, text, font=font,fill="black")
    #draw.text(text_pos1, text1, font=font1,fill="black")
    #draw.text(text_pos2, text2, font=font1,fill="black")
    text_pos = [150,300]
    draw.text(text_pos, "area medida: %d px^2 ( %.1f um^2 )"%(area_square,(area_square*0.493*0.493)), font=font,fill="black")
    text_pos1 = [150,350]
    draw.text(text_pos1, "diam : %d px  ( %.1f um ) diam2 : %d px ( %.1f um )"%(d_disk[0],(d_disk[0]*0.493),d_disk[1],(d_disk[1]*0.493)), font=font,fill="black")
    #text_pos2 = [150,400]
    #draw.text(text_pos2, "diam : %d um"%, font=font,fill="black")
  
    ##
    if(flag_draw_material):
		draw.line((disk_bounds[0], disk_bounds[1], disk_bounds[0], disk_bounds[1]+d_disk[1]),fill="green")
		draw.line((disk_bounds[0], disk_bounds[1], disk_bounds[0]+d_disk[0], disk_bounds[1]),fill="green")
		draw.line((disk_bounds[0]+d_disk[0], disk_bounds[1],disk_bounds[0]+d_disk[0], disk_bounds[1]+d_disk[1]),fill="green")
		draw.line((disk_bounds[0], disk_bounds[1]+d_disk[1],disk_bounds[0]+d_disk[0], disk_bounds[1]+d_disk[1]),fill="green")
    
    if(flag_draw_profile):
		r_01 = [bbox_profile[0],bbox_profile[1]]
		r_02 = [bbox_profile[2],bbox_profile[1]]
		r_03 = [bbox_profile[0],bbox_profile[3]]
		r_04 = [bbox_profile[2],bbox_profile[3]]
		draw.line((r_01[0],r_01[1],r_02[0],r_02[1]),fill="green")
		draw.line((r_03[0],r_03[1],r_04[0],r_04[1]),fill="green")
		draw.line((r_01[0],r_01[1],r_03[0],r_03[1]),fill="green")
		draw.line((r_02[0],r_02[1],r_04[0],r_04[1]),fill="green")
		#draw.rectangle([(130,140),(170,220)],fill=None)
		print "Profile"
		print "rprof_1:",r_01
		print "rprof_2:",r_04
		if(flag_draw_calculated_profile):
			r_01 = [bbox_profile[0],ycm]
			r_02 = [bbox_profile[2],ycm]
			r_03 = [xcm,bbox_profile[1]]
			r_04 = [xcm,bbox_profile[3]]
			draw.line((r_01[0],r_01[1],r_02[0],r_02[1]),fill="green")
			draw.line((r_03[0],r_03[1],r_04[0],r_04[1]),fill="green")
			#draw.line((r_01[0],r_01[1],r_03[0],r_03[1]),fill="green")
			#draw.line((r_02[0],r_02[1],r_04[0],r_04[1]),fill="green")
			
		
    
    #
    if(flag_draw_bkg):
		r_01 = [bkg_bounds[0], bkg_bounds[1]]
		r_02 = [bkg_bounds[0], bkg_bounds[1]+dbkg_y]
		r_03 = [bkg_bounds[0]+dbkg_x,bkg_bounds[1]]
		r_04 = [bkg_bounds[0]+dbkg_x,bkg_bounds[1]+dbkg_y]
		draw.line((r_01[0],r_01[1],r_02[0],r_02[1]),fill="green")
		draw.line((r_03[0],r_03[1],r_04[0],r_04[1]),fill="green")
		draw.line((r_01[0],r_01[1],r_03[0],r_03[1]),fill="green")
		draw.line((r_02[0],r_02[1],r_04[0],r_04[1]),fill="green")
		print "background"
		print "rbkg_1:",r_01
		print "rbkg_2:",r_04
    if(flag_draw_circle):
		draw.ellipse(bbox,fill=None)
    if(flag_draw_material_circunscripto):
		alpha = d_disk[0]*param_n_x*0.5
		beta = d_disk[1]*param_n_y*0.5
		r_01 = [disk_bounds[0]+alpha,disk_bounds[1]+beta]
		r_02 = [disk_bounds[0]+d_disk[0]-alpha,disk_bounds[1]+beta]
		r_03 = [disk_bounds[0]+alpha,disk_bounds[1]+d_disk[1]-beta]
		r_04 = [disk_bounds[0]+d_disk[0]-alpha,disk_bounds[1]+d_disk[1]-beta]
		draw.line((r_01[0],r_01[1],r_02[0],r_02[1]),fill="green")
		draw.line((r_03[0],r_03[1],r_04[0],r_04[1]),fill="green")
		draw.line((r_01[0],r_01[1],r_03[0],r_03[1]),fill="green")
		draw.line((r_02[0],r_02[1],r_04[0],r_04[1]),fill="green")
		print "Sobre la region que promedia"
		print "r_av_1:",r_01
		print "r_av_1:",r_04
		#draw.line((profile_bounds[0], profile_bounds[1], profile_bounds[0], profile_bounds[1]+d_profile[1]),fill="rgb(255,0,0)")
		#draw.line((profile_bounds[0], profile_bounds[1], profile_bounds[0]+d_profile[0], profile_bounds[1]),fill="#ff0000")
		#draw.line((profile_bounds[0]+d_profile[0], profile_bounds[1],profile_bounds[0]+d_profile[0], profile_bounds[1]+d_profile[1]),fill="#ff0000")
		#draw.line((profile_bounds[0], profile_bounds[1]+d_profile[1],profile_bounds[0]+d_profile[0], profile_bounds[1]+d_profile[1]),fill="#ff0000")
		#if(flag_draw_calculated_profile):
			#draw.line((profile_bounds[0], profile_bounds[1]+d_profile[1]/2.0, profile_bounds[0]+d_profile[0], profile_bounds[1]+d_profile[1]/2.0),fill="green")
			#draw.line((profile_bounds[0]+d_profile[0]/2.0, profile_bounds[1], profile_bounds[0]+d_profile[0]/2.0, profile_bounds[1]+d_profile[1]),fill="green")
    del draw
    fn = f.split('.')
    gn = external_feed.split('_')
    hn=gn[0].split('d')
    #img.save(fn[0]+"."+fn[1]+"_bkgid_"+external_bkg+"_disk_id_"+hn[1]+".jpg","JPEG")
    img.save(f,"JPEG")



