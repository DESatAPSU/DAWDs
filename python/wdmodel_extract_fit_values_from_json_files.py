#!/usr/bin/env python

"""
    wdmodel_extract_fit_values_from_json_files.py

    Example:

    wdmodel_extract_fit_values_from_json_files.py --help

    wdmodel_extract_fit_values_from_json_files.py --mainDir ./SOAR_Oct2017/BasicParameters_Oct2017 --outputCSVFile fitValues_BasicParameters_Oct2017.csv --verbose 2

    """



##################################

def main():

    import argparse
    import time

    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__, \
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--mainDir', \
                        help='name of the upper-level WDmodel results directory under which to search for result.json files')
    parser.add_argument('--outputCSVFile', \
                        help='name of the CSV file to output')
    parser.add_argument('--verbose', help='verbosity level of output to screen (0,1,2,...)', \
                        default=0, type=int)
    args = parser.parse_args()

    if args.verbose > 0: print args

    status = wdmodel_extract_bestfit_model_from_hdf5(args)
    
    return status


##################################
# wdmodel_extract_bestfit_model_from_hdf5

def wdmodel_extract_bestfit_model_from_hdf5(args):

    import sys
    import os
    import glob
    from shutil import copyfile
    import pandas as pd
    import json

    # mainDir is the upper level directory.
    # The "glob.glob" command looks for files with names ending in "_result.json"
    #  in all the sub-sub-directories of mainDir.
    # Note that, as currently written, files with names ending in "_result.json"
    #  that are NOT in a subdirectory two levels down from mainDir will NOT be
    #  found.  I.e., as currently written, the "glob.glob" command below expects
    #  a certain directory structure under the main directory, in order to find
    #  the "_result.json" files...
    mainDir = args.mainDir
    fileList = glob.glob(mainDir+'/*/*/*_result.json')
    
    outputFile = args.outputCSVFile
    fout = open(outputFile, 'w')

    # Loop through list of _result.json files in fileList...
    iflag = 0
    for gn_json in fileList:
    
        name = os.path.basename(gn_json)
        # Remove '_result.json' from the end of name...
        name = name.rstrip('_result.json')
        # Remove '_sum' from the end of name (if present)...
        name = name.rstrip('_sum')

        # Read json file into a pandas DataFrame...
        df_json = pd.read_json(gn_json,orient='index')

        # if this is the first file in the list, first print out a header line...
        if iflag == 0: 
            outputLine = ""
            for index in df_json.index:
                outputLine = """%s,%s,%s_errp,%s_errm,%s_fixed""" % (outputLine,index,index,index,index)
            outputLine = "name"+outputLine
            if verbose > 0:  print outputLine
            fout.write(outputLine+'\n')
            iflag = 1
        
        # Extract value, error_p, error_m, and fixed for each parameter
        #  from the json file...
        outputLine = ""
        for index in df_json.index:
            value = df_json.loc[index].value
            error_p = df_json.loc[index].errors_pm[0]
            error_m = df_json.loc[index].errors_pm[1]
            fixed = df_json.loc[index].fixed
            outputLine = """%s,%g,%g,%g,%d""" % (outputLine, value, error_p, error_m, fixed)
        outputLine = name+outputLine
        fout.write(outputLine+'\n')
        if verbose > 0:  print outputLine
    

    fout.close()

    return 0


##################################

if __name__ == "__main__":
    main()

##################################
