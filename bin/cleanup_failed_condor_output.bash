# Name of the pnfs output directory where the failed results are saved:
#pnfsOutDir=/pnfs/des/persistent/WDmodel/output/Summer2018/SOAR_Jan2018/ObservedData_Jan2018/MarrinerReductions/Flm
#pnfsOutDir=/pnfs/des/persistent/WDmodel/output/Summer2018/SOAR_Dec2014/ObservedData_Dec2014/MarrinerReductions
pnfsOutDir=/pnfs/des/persistent/WDmodel/output/Summer2018/SOAR_Oct2017/ObservedData_Oct2017/MarrinerReductions/Flm

# Needed for ifdh:
source /cvmfs/des.opensciencegrid.org/eeups/startupcachejob21i.sh
setup ifdhc


# if the condor_q_failed.txt already exists, 
#  rename the current versino to condor_q_failed.txt~:
if [ -e  condor_q_failed.txt ]; then
    mv condor_q_failed.txt condor_q_failed.txt~
fi


# Find all the failed condor output files in the pnfs output directory...
#  Note that the piped sed command trims off extraneous ANSI ESC codes...
# * * * THIS MIGHT NEED IMPROVEMENT TO AVOID FALSE POSITIVES AND MISS FALSE NEGATIVES ! ! ! * * * 
#ls -l $pnfsOutDir/out_*.tar.gz | awk '$5<1000 {print $9}'  | awk -F"/" '{print $NF}' | sed 's/\x1b\[[0-9;]*[JKmsu]//g' > condor_q_failed.txt
# For Oct17, we add a date constraint ($7>=18) as well, to avoid earlier processes...
ls -l $pnfsOutDir/out_*.tar.gz | awk '$5<1000 && $7>=18 {print $9}'  | awk -F"/" '{print $NF}' | sed 's/\x1b\[[0-9;]*[JKmsu]//g' > condor_q_failed.txt


# Loop through list of failed and remove failed output files
#  from the pnfs output directory...
for f in  `cat condor_q_failed.txt`; do 
    echo $f
    ifdh rm $pnfsOutDir/$f; done


# Loop through list of failed and rename failed output files
#  in the local output directory...
for f in `cat condor_q_failed.txt`; do 
    fn=${f%.tar.gz}
    fnn=${fn#out_}
    echo $fnn
    fname=wdmodel_$fnn.out; if [ -e $fname ]; then mv $fname $fname.old; fi
    fname=wdmodel_$fnn.err; if [ -e $fname ]; then mv $fname $fname.old; fi
    fname=wdmodel_$fnn.log; if [ -e $fname ]; then mv $fname $fname.old; fi
done 


# Generate new condor submit bash script...
#
# if condorReSubmit.bash already exists, 
#  rename the current version to  condorReSubmit.bash~:
if [ -e  condorReSubmit.bash ]; then
    mv condorReSubmit.bash condorReSubmit.bash~
fi
# Create empty condorReSubmit.bash file...
touch condorReSubmit.bash
# Loop through condor_q_failed.txt and generate condor submit commands...
for f in `cat condor_q_failed.txt`; do 
    fn=${f%.tar.gz}
    fnn=${fn#out_}
    echo condor_submit submit_$fnn >> condorReSubmit.bash
    echo "sleep 60" >> condorReSubmit.bash
done 
echo "Finis!" >> condorReSubmit.bash


# Done!
echo "Finis!"
