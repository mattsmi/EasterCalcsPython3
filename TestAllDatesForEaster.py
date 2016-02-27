#!/usr/bin/env python
''' This script can be run as follows:
       python3 TestAllDatesForEaster.py 326 4099 > ListOfEasterDates.txt
    Running it in this way, sends the standard output to a file for checking.
'''
iMIN_VERSION = 3    #Minimum version of the Python for this script.

import os
import sys
import datetime

##Globals for the Easter functions
iEDM_JULIAN  = 1
iEDM_ORTHODOX  = 2
iEDM_WESTERN  = 3
iFIRST_EASTER_YEAR  = 326
iFIRST_VALID_GREGORIAN_YEAR  = 1583
iLAST_VALID_GREGORIAN_YEAR  = 4099


def xRunningCorrectPythonVersion(sMinimumVersion='3'):
    '''Assumes a version number returned from the system in a format similar to: '3.2.1' .
       We can check against (major), (major and minor), or (major, minor, and micro) release levels.
       The default minimum is a major release level of '3' .
       Input of type Integer or Long is converted to type String.
       
       Return value: True or False, whether the version is sufficient.
    '''
    
    import platform
    
    #Find length of version requested.
    #   The length can be between 1 and 5, e.g. between a version like '3' and '3.2.1' .
    #Cast input as string, in case an integer has been passed.
    sMinVer = str(sMinimumVersion)
    iVerLen = len(sMinVer)     
    if (iVerLen < 1) or (iVerLen > 5):
        raise ValueError('Release levels of 1 - 5 characters in length, only, are valid: e.g. \'3\' to \'3.2.1\' .')
    
    #Find the version of Python interpreting this script
    sPythonVersion = platform.python_version()
    
    #Check major release level
    if int(sPythonVersion[:1]) < int(sMinVer[:1]):
        return False
        
    #Check minor release level
    if len(sMinVer) > 2:
        if int(sPythonVersion[2:3]) < int(sMinVer[2:3]):
            return False
    
    #Check micro release level
    if len(sMinVer) > 4:
        if int(sPythonVersion[4:5]) < int(sMinVer[4:5]):
            return False
    
    #Having passed all checks, we are OK.
    return True

def pTestDatesForEaster(iStartYear, iFinishYear):
    '''  This script produces values for Easter for valid Easter dates (e.g. from AD 326 to AD 4099).
            Our calendar functions, however, limit us to dates later than the UNIX Epoch (1 January 1970).
            NB: (a) Easter calculation defined at the Council of Nicæa in AD 325.
                (b) Gregorian calendar defined and started in October AD 1582.
                (c) Revised Julian or Milanković calendar defined in May AD 1923.
         It should be executed from within a CLIPS shell by: (batch* "TestAllDatesForEaster.clp").
    '''


def pF15_CalcDateOfEaster(iYearToFind, iDatingMethod):
    # default values for invalid arguments
    imDay = 0
    imMonth = 0
    # intermediate results (all integers)
    iFirstDig = 0
    iRemain19 = 0
    iTempNum = 0
    # tables A to E results (all integers)
    iTableA = 0
    iTableB = 0
    iTableC = 0
    iTableD = 0
    iTableE = 0
    
    #  Calculate Easter Sunday date
    # first 2 digits of year (integer division)
    iFirstDig = iYearToFind // 100
    # remainder of year / 19
    iRemain19 = iYearToFind % 19

    if (iDatingMethod == iEDM_JULIAN) or (iDatingMethod == iEDM_ORTHODOX):
        #  calculate PFM date
        iTableA = ((225 - 11 * iRemain19) % 30) + 21

        #  find the next Sunday
        iTableB = (iTableA - 19) % 7
        iTableC = (40 - iFirstDig) % 7

        iTempNum = iYearToFind % 100 
        iTableD = (iTempNum + (iTempNum // 4)) % 7

        iTableE = ((20 - iTableB - iTableC - iTableD) % 7) + 1
        imDay = iTableA + iTableE
        
        # convert Julian to Gregorian date
        if iDatingMethod == iEDM_ORTHODOX:
           # 10 days were # skipped#  in the Gregorian calendar from 5-14 Oct 1582
            iTempNum  = 10
            # Only 1 in every 4 century years are leap years in the Gregorian
            # calendar (every century is a leap year in the Julian calendar)
            if iYearToFind > 1600 :
                iTempNum = iTempNum + iFirstDig - 16 - ((iFirstDig - 16) // 4)
            
            imDay = imDay + iTempNum
    else:
        #That is iDatingMethod == iEDM_WESTERN
        #  calculate PFM date
        iTempNum = ((iFirstDig - 15) // 2) + 202 - 11 * iRemain19
        lFirstList = [21, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35, 38]
        lSecondList = [33, 36, 37, 39, 40]
        if iFirstDig in lFirstList:
            iTempNum = iTempNum - 1
        elif iFirstDig in lSecondList:
            iTempNum = iTempNum - 2
            
        iTempNum = iTempNum % 30

        iTableA  = iTempNum + 21
        if iTempNum == 29 :
            iTableA = iTableA - 1
        if ((iTempNum == 28) and (iRemain19 > 10)):
            iTableA = iTableA - 1

        #  find the next Sunday
        iTableB = (iTableA - 19) % 7

        iTableC = (40 - iFirstDig) % 4
        if iTableC == 3 :
            iTableC = iTableC + 1
        if iTableC > 1 :
            iTableC = iTableC + 1

        iTempNum = iYearToFind % 100
        iTableD = (iTempNum + iTempNum // 4) % 7

        iTableE = ((20 - iTableB - iTableC - iTableD) % 7) + 1
        imDay = iTableA + iTableE

    #  return the date
    if imDay > 61 :
        imDay = imDay - 61
        imMonth = 5
        # for imMethod 2, Easter Sunday can occur in May
    elif imDay > 31 :
        imDay = imDay - 31
        imMonth = 4
    else:
        imMonth = 3

    return datetime.date(iYearToFind, imMonth, imDay)


def main(argv): 

    #Check two arguments: year and dating method, the second of which is optional
    if (len(argv) != 3): 
        sys.stderr.write("USAGE: %s <year, year to start calculating Easter> <final year to calculate Easter> \n" % (argv[0])) 
        return None
    elif len(argv) == 3:
        sStartYear = argv[1]
        sFinishYear = argv[2]

    
    #Confirm that the arguments are valid
    try:
        iStartYear = int(sStartYear)
    except Exception:
        sys.stderr.write("The first argument should be the year, in which we start calculating Easter.")
        return None
    try:
        iFinishYear = int(sFinishYear)
    except Exception:
        sys.stderr.write("The second argument should be the year, in which we finish calculating Easter.")
        return None
    #   Check that the years themselves are valid
    if (iStartYear < iFIRST_EASTER_YEAR) or (iStartYear > iLAST_VALID_GREGORIAN_YEAR):
        sys.stderr.write("The year requested is not valid. You used: %s .\n" % sYearToFind)
        return None
    
    #Loop through the years and produce the output in comma-delimited format.
    #   Standard output can be redirected to a file for later analysis.
    iCounter = iStartYear
    while (iCounter <= iFinishYear):
        dJulianEaster = pF15_CalcDateOfEaster(iCounter, 1)
        if (iCounter > 1923):
            dRevisedJulianEaster = pF15_CalcDateOfEaster(iCounter, 2)
            dGregorianEaster = pF15_CalcDateOfEaster(iCounter, 3)
            print(dJulianEaster.strftime("%Y-%m-%d").strip() + "," + dRevisedJulianEaster.strftime("%Y-%m-%d").strip() + "," + dGregorianEaster.strftime("%Y-%m-%d").strip())
        elif (iCounter > 1582):
            dGregorianEaster = pF15_CalcDateOfEaster(iCounter, 3)
            print(dJulianEaster.strftime("%Y-%m-%d").strip() + "," + ",", dGregorianEaster.strftime("%Y-%m-%d").strip())
        else:
            print(dJulianEaster.strftime("%Y-%m-%d").strip() + "," + ",")
        iCounter = iCounter + 1
 
    

if __name__ == "__main__":
    #Initially, check that we are running the correct version of the Python interpreter.
    if not xRunningCorrectPythonVersion(iMIN_VERSION):
        sys.exit('The minimum version of Python required is: ' + str(iMIN_VERSION) + ' .')
    #The main procedure accesses the web pages or files, based on the arguments supplied.
    sys.exit(main(sys.argv)) 
    

