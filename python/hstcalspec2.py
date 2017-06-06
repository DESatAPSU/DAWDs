# These statements import python modules that will be used below...
import glob
import os
import string
from pyraf import iraf
from shutil import copyfile

import pyfits

# Load necessary IRAF (pyraf) modules...
iraf.stsdas()
iraf.hst_calib()
iraf.synph

# cd to current working directory
iraf.cd(os.getcwd())

# This creates a list of filter file names...
print "Here is the list of CCDs:"
filterFileNameList = glob.glob('des_band_20150601a_syn.average.list')
#filterFileNameList += glob.glob('des_band_20150601a_syn.ccd*.list')
#filterFileNameList += glob.glob('des_band_20150601a_syn.ccd*_amp1.list')
#filterFileNameList += glob.glob('des_band_20150601a_syn.ccd*_amp2.list')
filterFileNameList.sort()
print filterFileNameList

# This is the file containing the list of calspec files,
#  which you created previously using the pyraf "files"
#  command (see top of this script)...
calspecListFileName='calspec3.list'

# Open and the calspec list file...
fd = open(calspecListFileName,'r')
line = fd.readline()

# Loop through the calspec list file...
while line != "":
	
	# This is the name of the calspec star file we are working on now...
	calspecFileName=string.strip(line)
	# Create an output file based on the original filter file name...
	outFileName='des_'+calspecFileName
	#index6 = calspecFileName.find("uk_")
	#index7 = calspecFileName.find(".fits")	
	#picklesnum = str(int(calspecFileName[index6+3:index7]))
	#outFileName = 'des_pickles_' + picklesnum + '.fits'
	print outFileName
	# If a file with this name already exists, delete the old one...
	iraf.imdel(outFileName)
	
	#This loop cycles through each of the ccds on the focal plane
	for i in range(len(filterFileNameList)):
		
		# This is the particular filter file we will work on now...
		filterFileName = filterFileNameList[i]
		
		# Open the filter list file...
		fd1 = open(filterFileName,'r')
		line1 = fd1.readline()

		while line1 != "":		
			
			# This is the name of the calspec star file we are working on now...
			filterBandFileName=string.strip(line1)
			
			# This loop finds the right band name...
			if "average" in filterBandFileName:   
  				print "average"
				index = filterBandFileName.find("average")
				baseName=filterBandFileName[:index-1]
				ccdint = 0
				ampint = 0
				newBandFileName="""%s.ccd%02d.amp%1d.fits""" % (baseName, ccdint, ampint)
			elif "amp" in filterBandFileName:
				print "amp"
				index1 = filterBandFileName.find("ccd")
				index2 = filterBandFileName.find("amp")
				index3 = filterBandFileName.find(".fits")
				baseName = filterBandFileName[:index1-1]
				ccdint = int(filterBandFileName[index1+3:index2-1])
				ampint = int(filterBandFileName[index3-1:index3])
				newBandFileName="""%s.ccd%02d.amp%1d.fits""" % (baseName, ccdint, ampint)
			elif "ccd" in filterBandFileName:
				print "ccd"
				index1 = filterBandFileName.find("ccd")
				index3 = filterBandFileName.find(".fits")
				baseName = filterBandFileName[:index1-1]
				ccdint= int(filterBandFileName[index1+3:index3])
				ampint = 0
				newBandFileName="""%s.ccd%02d.amp%1d""" % (baseName, ccdint, ampint)
			else:
				print "Unrecognized file format"

			#This copies the file into a more organized way
			copyfile(filterBandFileName, newBandFileName)

			#This does the redshifting
			for angstroms in [0]:			
				#This creates a temporary file which we will use for the calcphot				
				angstromnum=str(angstroms)				
				tmpFilterFileName = newBandFileName + '_redshift' + angstromnum + '.fits'
   				print tmpFilterFileName
  				hdulist = pyfits.open(newBandFileName)
    				hdulist[1].data['WAVELENGTH'] = hdulist[1].data['WAVELENGTH'] + angstroms
    				hdulist.writeto(tmpFilterFileName, clobber=True)
    				hdulist.close()

				#This will prevent crashes
				try:
					#This does the calcphot
					print newBandFileName 
					print calspecFileName
					print outFileName
					iraf.calcphot(tmpFilterFileName, calspecFileName, 'abmag', out=outFileName, append='yes')
				except:
					print "****Calcphot failed for star " + calspecFileName + "****"
				
				#end for

			#This deletes the file we made
			os.remove(newBandFileName)
	
			#This continues the loop
			line1 = fd1.readline()

		#end while	

	#end for
	
	#This sorts the table before looping
		

	#This keeps the while loop going	
	line = fd.readline()

#end while
