import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import stats
import sys
sys.path.append("./modules/")
####################################################################################################################################
filename = '30.0K_20x_01_d1_intensity_h_01'
filename = '30.0K_20x_01_d1_intensity_v_01'
filename = '30.0K_20x_01_d1_intensity_h_02'
#filename = '30.0K_20x_01_d1_intensity_v_02'
##OUTPUTS

filenameOut = '30.0K_20x_01_d1_gauss_h_01'
filenameOut = '30.0K_20x_01_d1_gauss_v_01'
filenameOut = '30.0K_20x_01_d1_gauss_h_02'
#filenameOut = '30.0K_20x_01_d1_gauss_v_02'
dataIn = np.loadtxt(filename+".dat")
print "Run twice. First to determine value of correction w flag first. Then take the correction value an change flag"
flag = "first"
flag = ""
corrMin = 0
if (flag!="first"): corrMin = 34471.0

#corrMin = 34509.0 #1h
#corrMin = 34979.0 #1v
#corrMin = 34471.0 #2h
#corrMin = 34874.0 #2v
print corrMin

####################################################################################################################################
writeIt = open(filenameOut+".dat", "w")	

relPath = "./"
#Calibration curve
#filename = 'd01_Hyst_30.0K_20x_01_IvsH_bkgId_2_01'
filename = 'd01_Hyst_30.0K_20x_01_IvsH_bkgId_2_02_sorted'
calCurve = np.loadtxt(relPath+filename+".dat")

Int = np.array([calCurve[i,0] for i in range(len(calCurve[:,0]))])
Ha = np.array([calCurve[i,1] for i in range(len(calCurve[:,0]))])

correction = 0

if (flag!="first"): correction = min(Int)-corrMin

print "correction: ", correction
Int=Int-correction

tck = interpolate.splrep(Int, Ha, s=0)
yPy = interpolate.splev(Int, tck, der=0)

#last points
IntLast = Int[-9:]
HaLast = Ha[-9:]
slope, intercept, r_value, p_value, std_err = stats.linregress(IntLast,HaLast)

linearFit = lambda x: slope*x+intercept

lenRow = dataIn.shape[0]
lenCol = dataIn.shape[1]

minVals = []
spline3MinVals = []

maxVals = []
spline3MaxVals = []
linearMaxVals = []

print Int[1]-Int[0]
for j in range(lenCol):
	writeIt.write("%.2f\t" % (dataIn[0,j])) #800
writeIt.write("\n")
for i in range(1,lenRow):
	writeIt.write("%.2f\t" % (dataIn[i,0])) #800
	for j in range(1,lenCol):
		if(dataIn[i,j]<min(Int)):
			minVals.append(dataIn[i,j])
			spline3MinVals.append(interpolate.splev(dataIn[i,j], tck, der=0))
		 	print "MIN %d %d (%.2f G) - value %d- min %d - dif %d"%(i,j,dataIn[0,j],dataIn[i,j],min(Int),dataIn[i,j]-min(Int))
		if(dataIn[i,j]>max(Int)):
			maxVals.append(dataIn[i,j])
			spline3MaxVals.append(interpolate.splev(dataIn[i,j], tck, der=0))
			print "MAX %d %d (%.2f G) - value %d- max %d - dif %d"%(i,j,dataIn[0,j],dataIn[i,j],max(Int),dataIn[i,j]-max(Int))
		if(dataIn[i,j]>min(Int) and dataIn[i,j]<max(Int)):
			writeIt.write("%.4f\t" % (interpolate.splev(dataIn[i,j], tck, der=0))) #800	
		if(dataIn[i,j]>max(Int)):
			writeIt.write("%.4f\t" % (linearFit(dataIn[i,j]))) #800	
			print linearFit(dataIn[i,j])
			linearMaxVals.append(linearFit(dataIn[i,j]))
			#writeIt.write("%.4f\t" % (interpolate.splev(dataIn[i,j], tck, der=0))) #800
	writeIt.write("\n")
writeIt.close()
if(len(minVals)!=0): print min(minVals)

plt.plot(Int, Ha, 'o',Int, yPy , 'b',minVals,spline3MinVals ,'ko' ,maxVals,spline3MaxVals ,'go',maxVals,linearMaxVals ,'ro')
plt.legend(['data', 'cubic spline python'], loc='best')


plt.show()