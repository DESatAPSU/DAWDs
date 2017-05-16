# Deals with updated format from most recent (20170515) models...
# To run:  
#   python pet_models_convert_format_20170515.py SSSJ0710-4144_sum5.txt SSSJ0710-4144_sum5.newformat.txt

import os
import sys
import numpy as np

# inputFile is the first argument in the argument list; 
# outputFile is the second...
inputFile = sys.argv[1]
outputFile = sys.argv[2]

# Check to see if file exists and is readable...
if os.path.isfile(inputFile)==False:
    print """%s does not exist!  Exiting now! """ % (inputFile)
    exit

# Read in contents of the inputFile as a numpy array...
in_array = np.genfromtxt(inputFile,names=['wave','fnu'],skip_header=1)

# Extract wavelength and Fnu 1D arrays...
wave = in_array['wave']
fnu = in_array['fnu']

# Create an Flam 1D array from the wavelength and Fnu arrays...
flam = fnu * (2.99792458e18 / (wave*wave) )

# Combine wavelength and Flam 1D arrays into a 2D output arrray...
out_array = np.column_stack((wave,flam))

# Save 2D output array as an ASCII text file...
np.savetxt( outputFile, out_array )

# End of script...
print "That's all, folks!"

