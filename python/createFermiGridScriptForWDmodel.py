#!/usr/bin/env python

# Authors:   Douglas Tucker and Deborah Gulledge
#
# Updated:    10 July 2018, 9 July 2018, 1 Aug 2017
# Created:   26 July 2017


"""
    createFermiGridScriptForWDmodel.py

    Example:

    createFermiGridScriptForWDmodel.py --help

    createFermiGridScriptForWDmodel.py --specRelPathName SOAR4m/JohnMarriner/SSSJ0203-0459_sum.flm --outDirRelPathName SOAR4m/JohnMarriner --verbose 2

    """

##################################

def main():

    import argparse
    import time

    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__, \
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--specRelPathName', \
                        help='name spectrum .flm file in /pnfs/des/persistent/WDmodel/Spectra', \
                        default='SOAR4m/JohnMarriner/SSSJ0203-0459_sum.flm')
    parser.add_argument('--outDirRelPathName', \
                        help='relative path of output directory in /pnfs/des/persistent/WDmodel/output', \
                        default='SOAR4m/JohnMarriner')
    parser.add_argument('--verbose', help='verbosity level of output to screen (0,1,2,...)', \
                        default=0, type=int)
    args = parser.parse_args()

    if args.verbose > 0: print args

    status = createFermiGridScriptForWDmodel(args)
    
    return status


##################################
# createFermiGridScriptForWDmodel

def createFermiGridScriptForWDmodel(args):

    import os
    import sys
    import stat
    import datetime    

    # Upper-level pnfs directory under which the .flm files go
    # (perhaps several sub-directories down)...
    pnfsSpecDir = '/pnfs/des/persistent/WDmodel/Spectra'
    
    # Upper-level pnfs directory under which the output files go
    # (perhaps several sub-directories down)...
    pnfsOutDir = '/pnfs/des/persistent/WDmodel/output'

    # Extract values for specRelPathName, outDirRelPathName, and verbose from args...
    #  E.g., specRelPathName='SOAR4m/JohnMarriner/SSSJ0203-0459_sum.flm',
    #        outDirRelPathName='SOAR4m/JohnMarriner', and verbose=2
    specRelPathName = args.specRelPathName
    outDirRelPathName = args.outDirRelPathName
    verbose = args.verbose
    
    # Build full spectra dir path name from pnfsSpecDir and specRelPathName...
    specFullPathName = os.path.join(pnfsSpecDir, specRelPathName)

    #if (not os.path.isfile(specFullPathName)):
    #    print """Can't find %s""" % (specFullPathName)
    #    print 'Exiting now...'
    #    return 1
    
    # Base file name (minus the (sub)directories)...
    #  E.g., specFileName='SSSJ0203-0459_sum.flm'
    specFileName = os.path.basename(specRelPathName)

    # Spectrum name (minus the .flm extension)...
    #  E.g., specName='SSSJ0203-0459_sum'
    specName = os.path.splitext(specFileName)[0]

    # Build full pnfs output dir path name from pnfsOutDir and outDirRelPathName...
    outDirFullPathName = os.path.join(pnfsOutDir, outDirRelPathName)

    #if (not os.path.isfile(outDirFullPathName)):
    #    print """Can't find %s""" % (outDirFullPathName)
    #    print 'Exiting now...'
    #    return 1
    
    # Create a timestamp in the form "YYYYMMDD_hhmmss"...
    #  E.g., 20170726_150104
    tstamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create FermiGrid local machine output directory name
    localOutputDirName = """out_%s_%s""" % (specName,tstamp)

    # Create name of Fermilab output tar file...
    outputTarFile = """%s.tar.gz""" % (localOutputDirName)
    
    # Create name of script to be submitted to FermiGrid...
    scriptName = """wdmodel_%s_%s.sh""" % (specName,tstamp)


    # Create and save contents of scriptName...
    fout = open(scriptName,'w')
    fout.write("""#!/bin/bash\n""")
    fout.write("""\n""")
    fout.write("""# Suggestion from A Drlica-Wagner and B Yanny:\n""")
    fout.write("""OLDHOME=$HOME\n""")
    fout.write("""export HOME=$PWD\n""")
    fout.write("""\n""")
    fout.write("""# Grabbed the following block from\n""")
    fout.write("""#  /cvmfs/des.opensciencegrid.org/users/kadrlica/gridsetup.sh\n""")
    fout.write("""export PRODUCTS=/cvmfs/fermilab.opensciencegrid.org/products/common/prd/\n""")
    fout.write("""export PATH=$PATH:$PRODUCTS/cpn/v1_7/NULL/bin\n""")
    # Strictly speaking, should not need jobsub_client *within* grid process...
    fout.write("""export PATH=$PATH:$PRODUCTS/jobsub_client/v1_1_9_1/NULL/\n""")
    # Ken Herner recommends using ifdhc v2_1_0 or newer:
    #fout.write("""export PATH=$PATH:$PRODUCTS/ifdhc/v2_0_1/Linux64bit-2-6-2-12/bin\n""")
    #fout.write("""export PYTHONPATH=$PYTHONPATH:$PRODUCTS/ifdhc/v2_0_1/Linux64bit-2-6-2-12/lib/python\n""")
    fout.write("""export PATH=$PATH:$PRODUCTS/ifdhc/v1_8_9/Linux64bit-2-6-2-12/bin\n""")
    fout.write("""export PYTHONPATH=$PYTHONPATH:$PRODUCTS/ifdhc/v1_8_2/Linux64bit-2-6-2-12/lib/python\n""")
    # Strictly speaking, should not need jobsub_client *within* grid process...
    fout.write("""export PYTHONPATH=$PYTHONPATH:$PRODUCTS/jobsub_client/v1_1_3/NULL\n""")
    fout.write("""export IFDH_NO_PROXY=1\n""")
    fout.write("""\n""")
    fout.write("""# Copy synphot tar files from PNFS:\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot1.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot2.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot3.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot4.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot5.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot6.tar.gz .\n""")
    fout.write("""\n""")
    fout.write("""# Extract data from synphot tar files:\n""")
    fout.write("""tar xzf synphot1.tar.gz\n""")
    fout.write("""tar xzf synphot2.tar.gz\n""")
    fout.write("""tar xzf synphot3.tar.gz\n""")
    fout.write("""tar xzf synphot4.tar.gz\n""")
    fout.write("""tar xzf synphot5.tar.gz\n""")
    fout.write("""tar xzf synphot6.tar.gz\n""")
    fout.write("""\n""")
    fout.write("""# Activate WDmodel conda environment:\n""")
    fout.write("""export CONDA_DIR=/cvmfs/des.opensciencegrid.org/fnal/anaconda2/\n""")
    fout.write("""export PATH=$CONDA_DIR/bin:$PATH\n""")
    fout.write("""source activate WDmodel\n""")
    fout.write("""\n""")
    fout.write("""# Point PYSYN_CDBS environment variable to the synphot CDBS data directory:\n""")
    fout.write("""export PYSYN_CDBS=./grp/hst/cdbs\n""")
    fout.write("""\n""")
    fout.write("""# Copy FLM spectrum file:\n""")
    fout.write("""ifdh cp -D """+specFullPathName+""" .\n""")
    fout.write("""\n""")
    fout.write("""# Create output directory:\n""")
    fout.write("""mkdir """+localOutputDirName+"""\n""")
    fout.write("""\n""")
    fout.write("""# Run fit_WDmodel:\n""")
    fout.write("""fit_WDmodel --specfile """+specFileName+""" --ignorephot --redo --outroot """+localOutputDirName+""" --ntemps 5 --nwalkers 100 --nprod 5000 --samptype pt --thin 10\n""")
    fout.write("""\n""")
    fout.write("""# Tar up results from the fit:\n""")
    fout.write("""tar cvzf """+outputTarFile+""" """+localOutputDirName+"""\n""")
    fout.write("""\n""")
    fout.write("""# Copy tar file to PNFS:\n""")
    #fout.write("""ifdh cp -D """+outputTarFile+""" /pnfs/des/persistent/WDmodel/output\n""")
    fout.write("""ifdh cp -D """+outputTarFile+""" """+outDirFullPathName+"""\n""")
    fout.write("""\n""")
    fout.write("""# Suggestion from A Drlica-Wagner and B Yanny:\n""")
    fout.write("""export HOME=$OLDHOME\n""")
    fout.write("""\n""")

    fout.close()

    # Ensure scriptName is executable (by user, by group, and by others)...
    os.chmod(scriptName, 0775)

    print "Ensure the script is executable, and, then, to submit it to "
    print "FermiGrid, run the following command: "
    outputLine = """jobsub_submit -G des --resource-provides=usage_model=DEDICATED,OPPORTUNISTIC,OFFSITE -M --OS=SL6 --expected-lifetime=48h file://%s""" % (scriptName)
    print outputLine
    
    return 0

##################################

if __name__ == "__main__":
    main()

##################################
