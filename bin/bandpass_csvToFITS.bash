# Converts CSV files containing (wavelengths, throughputs)
#  for the DES standard bandpasses to a FITS table format
#  ingestible by the synphot calcphot task. 
#
# To run:
#    source bandpass_csvToFITS.bash
# in the same directory as the bandpass CSV files.
# Assumes that STILTS is installed on your machine
# ( http://www.star.bris.ac.uk/~mbt/stilts/ ).

# Change this to where STILTS is on your machine...
STILTS_DIR=/Users/dtucker/Software/STILTS/latest

# Assumes that the filenames are called
#  ${FILTER_SET_NAME}_${filtername}.csv
FILTER_SET_NAME=y3a2_std_passband

# Loop through each filter bandpass...
for f in g r i z Y; do

    echo $f
    infile=$FILTER_SET_NAME\_$f.csv
    outfile=$FILTER_SET_NAME\_$f.fits

    echo $infile
    echo $outfile
    
    # if there is a pre-existing version of $outfile, save it to $outfile~
    if [ -f $outfile ]; then 
	mv $outfile $outfile~
    fi

    $STILTS_DIR/stilts tpipe \
		       in=$infile ifmt=csv \
		       omode=out out=$outfile ofmt=fits \
		       cmd='colmeta -name WAVELENGTH -units Angstroms 1' \
		       cmd='colmeta -name THROUGHPUT 2'

done
