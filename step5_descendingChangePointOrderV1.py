#!/usr/bin/python
import matplotlib.pyplot as plt
#import scipy.io.array_import
import pylab
from numpy import zeros, sqrt, where, pi, average, arange, histogram,log, exp
import numpy as np
from scipy import stats
from scipy.stats import norm
import sys
from numpy import zeros, sqrt, where, pi, average, arange, histogram,log
from scipy.optimize import leastsq


####################################################################################################################################
filename = 'd01_Hyst_12.6K_20x_01_IvsH_bkgId_2_02'
filenameOut = 'd01_Hyst_12.6K_20x_01_IvsH_bkgId_2_02_sorted'
dataIn = np.loadtxt(filename+".dat")
####################################################################################################################################
#writeIt1 = open(filenameOut+"_odd.dat", "w")	
#writeIt2 = open(filenameOut+"_even.dat", "w")	

writeIt = open(filenameOut+".dat", "w")	

len1 = dataIn.shape[0]
tmp = 0

for i in range(len1):
		writeIt.write("%.8e\t %.8e\n" % (dataIn[len1-1-i,0],dataIn[len1-1-i,1])) #800
writeIt.close()
