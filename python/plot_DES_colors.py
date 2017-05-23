#!/usr/bin/env python

# This script plots color-color diagrams from a csv file.
# This should be run in the directory containing your csv magnitude files.
# Modification is required on lines 14, 34-38, 40-44, 53, 69, 77, 91, 99, 113, 122, & 136 depending on the particular dataset.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import glob

filenameList = sorted(glob.glob('*.csv'))
starnameList = [x.split('.mags') for x in filenameList]

for i in range (len(filenameList)):



    df = pd.read_csv(filenameList[i])

    #create color columns in dataframe

    df['u-g'] = df['u'] - df['g']
    df['g-r'] = df['g'] - df['r']
    df['r-i'] = df['r'] - df['i']
    df['i-z'] = df['i'] - df['z']
    df['z-Y'] = df['z'] - df['Y']

    #print df['r-i']

    #set masks for model variations
    
    best = starnameList[i][0] + '_123b'
    tpgp = starnameList[i][0] + '_123b.tp.gp'
    tpgm = starnameList[i][0] + '_123b.tp.gm'
    tmgp = starnameList[i][0] + '_123b.tm.gp'
    tmgm = starnameList[i][0] + '_123b.tm.gm'

    bestMask = (df['STARNAME']== best)
    tpgpMask = (df['STARNAME']== tpgp)
    tpgmMask = (df['STARNAME']== tpgm)
    tmgpMask = (df['STARNAME']== tmgp)
    tmgmMask = (df['STARNAME']== tmgm)


    #plotting


    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_title(starnameList[i][0] + ' (DES) No Reddening')

    #plot u-g vs. g-r

    axes.set_xlabel('u-g')
    axes.set_ylabel('g-r')

    axes.scatter(df[tmgpMask]['u-g'],df[tmgpMask]['g-r'],label='tm gp',color='#759EFF',alpha=0.7)
    axes.scatter(df[tmgmMask]['u-g'],df[tmgmMask]['g-r'],label='tm gm',color='#004DFF',alpha=0.7)
    axes.scatter(df[tpgpMask]['u-g'],df[tpgpMask]['g-r'],label='tp gp',color='#FF2525',alpha=0.7)
    axes.scatter(df[tpgmMask]['u-g'],df[tpgmMask]['g-r'],label='tp gm',color='#FF8080',alpha=0.7)
    axes.scatter(df[bestMask]['u-g'],df[bestMask]['g-r'],label='Best Fit',color='#42f448')

    axes.legend(loc='best', shadow=True)

    plt.grid(True)
    plt.savefig(starnameList[i][0] + '_DES_ug-gr.pdf')
    plt.close()

    #plot g-r vs. r-i

    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_title(starnameList[i][0] + ' (DES) No Reddening')

    axes.set_xlabel('g-r')
    axes.set_ylabel('r-i')

    axes.scatter(df[tmgpMask]['g-r'],df[tmgpMask]['r-i'],label='tm gp',color='#759EFF',alpha=0.7)
    axes.scatter(df[tmgmMask]['g-r'],df[tmgmMask]['r-i'],label='tm gm',color='#004DFF',alpha=0.7)
    axes.scatter(df[tpgpMask]['g-r'],df[tpgpMask]['r-i'],label='tp gp',color='#FF2525',alpha=0.7)
    axes.scatter(df[tpgmMask]['g-r'],df[tpgmMask]['r-i'],label='tp gm',color='#FF8080',alpha=0.7)
    axes.scatter(df[bestMask]['g-r'],df[bestMask]['r-i'],label='Best Fit',color='#42f448')

    axes.legend(loc='best', shadow=True)

    plt.grid(True)
    plt.savefig(starnameList[i][0] + '_DES_gr-ri.pdf')
    plt.close()

    #plot r-i vs. r-z

    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_title(starnameList[i][0] + ' (DES) No Reddening')

    axes.set_xlabel('r-i')
    axes.set_ylabel('i-z')

    axes.scatter(df[tmgpMask]['r-i'],df[tmgpMask]['i-z'],label='tm gp',color='#759EFF',alpha=0.5)
    axes.scatter(df[tmgmMask]['r-i'],df[tmgmMask]['i-z'],label='tm gm',color='#004DFF',alpha=0.5)
    axes.scatter(df[tpgpMask]['r-i'],df[tpgpMask]['i-z'],label='tp gp',color='#FF2525',alpha=0.5)
    axes.scatter(df[tpgmMask]['r-i'],df[tpgmMask]['i-z'],label='tp gm',color='#FF8080',alpha=0.5)
    axes.scatter(df[bestMask]['r-i'],df[bestMask]['i-z'],label='Best Fit',color='#42f448')

    axes.legend(loc='best', shadow=True)

    plt.grid(True)
    plt.savefig(starnameList[i][0] + '_DES_ri-iz.pdf')

    plt.close()

    #plot i-z vs. z-Y

    fig = plt.figure()
    axes = fig.add_subplot(111)

    axes.set_title(starnameList[i][0] + ' (DES) No Reddening')

    axes.set_xlabel('i-z')
    axes.set_ylabel('z-Y')

    axes.scatter(df[tmgpMask]['i-z'],df[tmgpMask]['z-Y'],label='tm gp',color='#759EFF',alpha=0.5)
    axes.scatter(df[tmgmMask]['i-z'],df[tmgmMask]['z-Y'],label='tm gm',color='#004DFF',alpha=0.5)
    axes.scatter(df[tpgpMask]['i-z'],df[tpgpMask]['z-Y'],label='tp gp',color='#FF2525',alpha=0.5)
    axes.scatter(df[tpgmMask]['i-z'],df[tpgmMask]['z-Y'],label='tp gm',color='#FF8080',alpha=0.5)
    axes.scatter(df[bestMask]['i-z'],df[bestMask]['z-Y'],label='Best Fit',color='#42f448')

    axes.legend(loc='best', shadow=True)

    plt.grid(True)
    plt.savefig(starnameList[i][0] + '_DES_iz-zY.pdf')

    plt.close()




exit()
