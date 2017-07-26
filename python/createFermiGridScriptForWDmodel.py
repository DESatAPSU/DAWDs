#!/usr/bin/env python

# Authors:   Douglas Tucker and Deborah Gulledge
# Date:      26 July 2017


"""
    createFermiGridScriptForWDmodel.py

    Example:

    createFermiGridScriptForWDmodel.py --help

    createFermiGridScriptForWDmodel.py --specRelPathName SOAR4m/JohnMarriner/SSSJ0203-0459_sum.flm --verbose 2

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

    # Upper-level directory under which the .flm files go
    # (perhaps several sub-directories down)...
    pnfsSpecDir = '/pnfs/des/persistent/WDmodel/Spectra'
    
    # Extract values for specRelPathName and verbose from args...
    #  E.g., specRelPathName='SOAR4m/JohnMarriner/SSSJ0203-0459_sum.flm' and verbose=2
    specRelPathName = args.specRelPathName
    verbose = args.verbose
    
    # Build full path name from pnfsSpecDir and specRelPathName...
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

    # Create a timestamp in the form "YYYYMMDD_hhmmss"...
    #  E.g., 20170726_150104
    tstamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create FermiGrid output directory name
    outputDirName = """out_%s_%s""" % (specName,tstamp)

    # Create name of Fermilab output tar file...
    outputTarFile = """%s.tar.gz""" % (outputDirName)
    
    # Create name of script to be submitted to FermiGrid...
    scriptName = """wdmodel_%s_%s.sh""" % (specName,tstamp)

    # Create and save contents of scriptName...
    fout = open(scriptName,'w')

    fout.write("""#!/bin/bash\n""")
    fout.write("""\n""")
    fout.write("""source /cvmfs/des.opensciencegrid.org/eeups/startupcachejob21i.sh\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot1.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot2.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot3.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot4.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot5.tar.gz .\n""")
    fout.write("""ifdh cp -D /pnfs/des/persistent/WDmodel/SynphotData/synphot6.tar.gz .\n""")
    fout.write("""tar xzf synphot1.tar.gz\n""")
    fout.write("""tar xzf synphot2.tar.gz\n""")
    fout.write("""tar xzf synphot3.tar.gz\n""")
    fout.write("""tar xzf synphot4.tar.gz\n""")
    fout.write("""tar xzf synphot5.tar.gz\n""")
    fout.write("""tar xzf synphot6.tar.gz\n""")
    fout.write("""\n""")
    fout.write("""export CONDA_DIR=/cvmfs/des.opensciencegrid.org/fnal/anaconda2/\n""")
    fout.write("""export PATH=$CONDA_DIR/bin:$PATH\n""")
    fout.write("""source activate WDmodel\n""")
    fout.write("""\n""")
    fout.write("""export PYSYN_CDBS=./grp/hst/cdbs\n""")
    fout.write("""\n""")
    fout.write("""ifdh cp -D """+specFullPathName+""" .\n""")
    fout.write("""\n""")
    fout.write("""mkdir """+outputDirName+"""\n""")
    fout.write("""fit_WDmodel --specfile """+specFileName+""" --ignorephot --redo --outroot """+outputDirName+""" --ntemps 5 --nwalkers 100 --nprod 5000 --samptype pt\n""")
    fout.write("""\n""")
    fout.write("""tar cvzf """+outputTarFile+""" """+outputDirName+"""\n""")
    fout.write("""ifdh cp -D """+outputTarFile+""" /pnfs/des/persistent/WDmodel/output\n""")
    fout.write("""\n""")

    fout.close()

    print "Ensure the script is executable, and, then, to submit it to "
    print "FermiGrid, run the following command: "
    outputLine = """jobsub_submit -G des --resource-provides=usage_model=DEDICATED -M --OS=SL6 --expected-lifetime=12h file://%s""" % (scriptName)
    print outputLine
    
    return 0

##################################

if __name__ == "__main__":
    main()

##################################
