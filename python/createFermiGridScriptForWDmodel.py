#!/usr/bin/env python

# Authors:   Douglas Tucker, Deborah Gulledge, Brian Yanny
#
# Updated:   16 July, 10 July 2018, 9 July 2018, 1 Aug 2017
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
    executableName = """wdmodel_%s_%s.sh""" % (specName,tstamp)

    # Create and save contents of executableName...
    fout = open(executableName,'w')
    fout.write("""#!/bin/bash\n""")
    fout.write("""\n""")
    fout.write("""# Suggestion from A Drlica-Wagner and B Yanny:\n""")
    fout.write("""OLDHOME=$HOME\n""")
    fout.write("""export HOME=$PWD\n""")
    fout.write("""\n""")
    fout.write("""# Setup EEUPS:\n""")
    fout.write("""source /cvmfs/des.opensciencegrid.org/eeups/startupcachejob21i.sh\n""")
    fout.write("""\n""")
    fout.write("""# Print out environment variables (in case of debugging):\n""")
    fout.write("""printenv\n""")
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
    fout.write("""mpirun -np 8 fit_WDmodel --specfile """+specFileName+""" --ignorephot --redo --outroot """+localOutputDirName+""" --ntemps 5 --nwalkers 100 --nprod 5000 --samptype pt --thin 10 --mpi\n""")
    fout.write("""\n""")
    fout.write("""# Tar up results from the fit:\n""")
    fout.write("""tar cvzf """+outputTarFile+""" """+localOutputDirName+"""\n""")
    fout.write("""\n""")
    fout.write("""# Copy tar file to PNFS:\n""")
    fout.write("""ifdh cp -D """+outputTarFile+""" """+outDirFullPathName+"""\n""")
    fout.write("""\n""")

    fout.write("""# NEW:  Delete extraneous files/directories on grid host:\n""")
    fout.write("""rm -f synphot?.tar.gz\n""")
    fout.write("""rm -rf ./grp\n""")
    fout.write("""rm -f """+outputTarFile+"""\n""")
    fout.write("""rm -rf """+localOutputDirName+"""\n""")
    fout.write("""\n""")

    fout.write("""# Suggestion from A Drlica-Wagner and B Yanny:\n""")
    fout.write("""export HOME=$OLDHOME\n""")
    fout.write("""\n""")

    fout.close()

    # Ensure executableName is executable (by user, by group, and by others)...
    os.chmod(executableName, 0775)


    # Create name of the condor submit script...
    condorSubmitScriptName = """submit_%s_%s""" % (specName,tstamp)

    # Create name of the script log file name...
    logName = """wdmodel_%s_%s.log""" % (specName,tstamp)

    # Create name of the script err log file name...
    errorlogName = """wdmodel_%s_%s.err""" % (specName,tstamp)

    # Create name of the script output file name...
    outputName = """wdmodel_%s_%s.out""" % (specName,tstamp)

    # Create and save contents of condorSubmitScriptName...
    fout = open(condorSubmitScriptName,'w')
    fout.write("""universe   = grid\n""")
    fout.write("""grid_resource = condor gpce04.fnal.gov gpce04.fnal.gov:9619\n""")
    fout.write("""executable = """+executableName+"""\n""")
    fout.write("""output = """+outputName+"""\n""")
    fout.write("""error = """+errorlogName+"""\n""")
    fout.write("""log = """+logName+"""\n""")
    fout.write("""#This is the RAM memory request (in 2 places) this is total for all 8 cores\n""")
    fout.write("""request_memory = 32 GB\n""")
    fout.write("""+maxMemory=32000\n""")
    fout.write("""#This is the cpu/core count (8 in this case)\n""")
    fout.write("""+xcount=8\n""")
    fout.write("""+JobClass="DES"\n""")
    fout.write("""Requirements = Target.IsDESNode == True\n""")
    fout.write("""#This is the scratch disk allocation\n""")
    fout.write("""request_disk = 50 GB\n""")
    fout.write("""ShouldTransferFiles = YES\n""")
    fout.write("""WhenToTransferOutput = ON_EXIT\n""")
    fout.write("""use_x509userproxy = true\n""")
    fout.write("""+Owner=undefined\n""")
    fout.write("""Queue\n""")
    fout.close()


    print "Ensure the ", executableName, "script is executable" 
    print "and, then, to submit it to FermiGrid, run the following command: "
    outputLine = """condor_submit %s""" % (condorSubmitScriptName)
    print outputLine
    
    return 0

##################################

if __name__ == "__main__":
    main()

##################################
