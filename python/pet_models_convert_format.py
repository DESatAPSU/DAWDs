# To run:  
#   python pet_models_convert_format.py WDC0224-0301_123b.txt WDC0224-0301_123b.newformat.txt

import os
import sys

# inputFile is the first argument in the argument list; 
# outputFile is the second...
inputFile = sys.argv[1]
outputFile = sys.argv[2]

# Check to see if file exists and is readable...
if os.path.isfile(inputFile)==False:
    print """%s does not exist!  Exiting now! """ % (inputFile)
    exit

# Read in full contents of the inputFile...
fin = open(inputFile, 'r')
linesList = fin.readlines()
fin.close()

# Number of lines in the file...
nlines = len(linesList)

# Number of wavelengths in the spectrum...
nwave = int(linesList[0].strip())

# Initialize a dataList to contain all the data 
#  elements from the inputFile...
dataList = []

# We start with line "1", since line "0"
#  just contains the number of elements
#  in the spectrum...
for i in range(1,nlines):

    line = linesList[i].strip().split()

    # There's a line, in between the list
    #  of wavelengths and the list of flams,
    #  that lists the teff, logg, and y
    #  for the model.  Its "zeroth" element
    #  is the word "Effective"...
    if line[0]=='Effective':
        teff = float(line[3])
        logg = float(line[6])
        y = float(line[9])
        print teff, logg, y
        continue

    for elem in line:
        value = float(elem)
        dataList.append(value)
        

# Split dataList in half.
#  The first half is the list of wavelengths.
#  The second half is the list of fnu
waveList = dataList[:nwave]
fnuList = dataList[nwave:]

# Output the reformatted data...
fout = open(outputFile, 'w')

for i in range(0,nwave):

    wave = waveList[i]
    # The following line converts from fnu to Flam
    Factor = 2.99792458e18 / (wave**2)
    flam = fnuList[i] * Factor

    outputLine = """%.2f %.5e\n""" % (wave, flam) 
    fout.write(outputLine)

# Close outputFile...
fout.close()

# End of script...
print "That's all, folks!"

