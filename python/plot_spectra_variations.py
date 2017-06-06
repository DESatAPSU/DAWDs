#!/usr/bin/env python

#this script plots the a white-dwarf model and its four variations in 1 simga. 
#It accepts a text file will the model file names listed. 
#Slight modification is required on line 61 to scale the y-axis correctly. 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the text list of files to plot (starList.txt) into a python list

with open('starList.txt') as f:
    lines = f.readlines()

lines = [x.strip() for x in lines]



# loop stuff

listLength = len(lines)


count = 0

# this loop plots the original model and the 4 variations

while (count < listLength):

    inputString1 = lines[count]
    inputString2 = lines[count + 1]
    inputString3 = lines[count + 2]
    inputString4 = lines[count + 3]
    inputString5 = lines[count + 4]
    
    
    plotTitle = lines[count][:12]
    plotFileName = lines[count][:12] + ".pdf"

    array1 = np.genfromtxt(inputString1,names=['wave','flam'])
    array2 = np.genfromtxt(inputString2,names=['wave','flam'])
    array3 = np.genfromtxt(inputString3,names=['wave','flam'])
    array4 = np.genfromtxt(inputString4,names=['wave','flam'])
    array5 = np.genfromtxt(inputString5,names=['wave','flam'])

    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_title(plotTitle)

    axes.set_xlabel('Wavelength (A)')
    axes.set_ylabel('Flux (Flam)')

    axes.plot(array1['wave'],array1['flam'],label='Original',linewidth=1)
    axes.plot(array2['wave'],array2['flam'],label='tm, gm',linewidth=1)
    axes.plot(array3['wave'],array3['flam'],label='tm, gp',linewidth=1)
    axes.plot(array4['wave'],array4['flam'],label='tp, gm',linewidth=1)
    axes.plot(array5['wave'],array5['flam'],label='tp, gp',linewidth=1)
    

    axes.set_xlim([3000,11000])
    axes.set_ylim([0,array1['flam'][1208]])

    axes.legend(loc='upper right', shadow=True)

    plt.grid(True)
    plt.savefig(plotFileName)
    plt.clf()


    count = count + 5



exit()
