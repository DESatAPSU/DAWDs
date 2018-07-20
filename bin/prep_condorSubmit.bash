# Prepare a script to submit WDmodel jobs to grid via condor for the Marriner 
#  reductions of the Dec2014 data...
#pnfsSpecDirName=/pnfs/des/persistent/WDmodel/Spectra/Summer2018/SOAR_Dec2014/ObservedData_Dec2014/MarrinerReductions
#pnfsSpecDirName=/pnfs/des/persistent/WDmodel/Spectra/Summer2018/SOAR_Oct2017/ObservedData_Oct2017/MarrinerReductions/Flm
pnfsSpecDirName=/pnfs/des/persistent/WDmodel/Spectra/Summer2018/SOAR_Aug2017/SOAR4m_Aug2017_JMarriner

bashScript=condorSubmit_Aug2017.bash

rm -f $bashScript.tmp
touch $bashScript.tmp

for fname in $pnfsSpecDirName/*.flm; do 
    specFile=${fname#/pnfs/des/persistent/WDmodel/Spectra/}
    outDir=${pnfsSpecDirName#/pnfs/des/persistent/WDmodel/Spectra/}
    ./createFermiGridScriptForWDmodel.py \
	--specRelPathName $specFile \
	--outDirRelPathName $outDir \
	--verbose 2 >> $bashScript.tmp
done

rm -f $bashScript
awk '$1=="condor_submit" {print $0"\nsleep 60"}' $bashScript.tmp > $bashScript
echo "echo Finis!" >> $bashScript

echo "Finis!"

