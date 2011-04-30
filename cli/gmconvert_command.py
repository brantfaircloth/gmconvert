#!/usr/bin/python

#-----------------------------------------------------------------------------------------------|
# GeneMapperConvert - command line version for Python                                           |
# available from http://gallus.forestry.uga.edu/lab/software.php                                |
#                                                                                               |
# Copyright (C) 2005-2006 Brant C. Faircloth.                                                   |                                                                                   
#                                                                                               |                                                                             
# This program is free software; you can redistribute it and/or modify it under the terms of the|
# GNU General Public License as published by the Free Software Foundation; either version 2 of  | 
# the License, or (at your option) any later version.                                           |
#                                                                                               |
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;     |
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     |
# See the GNU General Public License for more details.                                          |
#                                                                                               |
# You should have received a copy of the GNU General Public License along with this program; if |
# not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA     |
# 02111-1307, USA.                                                                              |
#-----------------------------------------------------------------------------------------------|

import string, getopt, sys, os

def Usage():
    print "\nGM_convert_cl.py -i 'src_file' [-f <options> | -o 'dest_file' | -h]\n\nwhere options for -f are:\n'cervus'\n'genepop'\n'gerud'\n\nDo Not Include Single Quotes!\n\nExample:  GM_convert_cl.py -i ~/Data/my_abi_file.txt -o ~/Data/outfile.txt -f genepop\n\n-f and -o are optional.  If not included, they will be set to defaults:\n(1) cervus for format\n(2) output.csv saved in the folder where the input file is located.\n\nBobwhite!\n"
    sys.exit()

def getOutFileFormat(input, output, programFormat):
    #-----------------------------------
    # set default file format for cervus
    #-----------------------------------
    if programFormat=='cervus' or not programFormat:  
        ###set default outfile name, null character and allele format (1/2 alleles)
        if not output:
            output=os.path.join(os.path.dirname(input),'output_cervus.csv')
            print (('\nNo output directory specified.  Using \'%s\'.') % (output))
        nullCharacter='*'
        ###alleleFormat=2 #options {1,2}
    #--------------------------
    # other file format options
    #--------------------------
    elif programFormat=='genepop':
        ###set default outfile name, null character and allele format (1/2 alleles)
        print 'Program format is Genepop'
        if not output:
            output=os.path.join(os.path.dirname(input),'output_genepop')
            print (('\nNo output directory specified.  Using \'%s\'.') % (output))
        nullCharacter='000'
        ###alleleFormat=2 #options {1,2}
    elif programFormat=='gerud':
        ###set default outfile name, null character and allele format (1/2 alleles)
        print 'Program format is Gerud'
        if  not output:
            output=os.path.join(os.path.dirname(input),'output_gerud.txt')
            print (('\nNo output directory specified.  Using \'%s\'.') % (output))
        nullCharacter='Nulls Not Allowed!'
        ###alleleFormat=2 #options {1,2}
    return output, nullCharacter

def getUserFiles():
    optlist, list = getopt.getopt(sys.argv[1:], 'i:o:f:h')
    output = ''                                                 #set output to empty
    verbose = 'N'
    i=0
    output, format = '',''
    if optlist:
        for opt in optlist:
            if opt[0] == '-i':
                input=opt[1]
            elif opt[0] == '-o':
                output=opt[1]
            elif opt[0] == '-f':
                format=opt[1]
            elif opt[0] == '-h':
                Usage()
        try:
            fileList = os.path.abspath(string.strip(input))        #have to strip whitespace characters
        except:
            print 'File not found.'
        if not format:
            format = 'cervus'
            print '\nFile format not found.  Using cervus format for output file.'
        elif format not in ['cervus','genepop','gerud']:
            print format
            print 'You have chosen an output format that is not available!'
            sys.exit()
        if not output:
            output, nullCharacter = getOutFileFormat(input, output, format)
        else:
            try:
                os.path.isdir(os.path.dirname(os.path.abspath(output)))
                nullCharacter = getOutFileFormat(input, output, format)[1]
            except:
                print 'This is not a valid path.  Make sure you have entered the path correctly.'
                sys.exit()
            #print ('\nOutput file written to %s') % (os.path.abspath(output))
    else:
        print 'GeneMapperConvert v0.2, Copyright (2005-2006) Brant C. Faircloth.  GeneMapperConvert comes with ABSOLUTELY NO WARRANTY; for details type show w.  This is free software, and you are welcome to redistribute it under certain conditions; type show c for details.\n'
        license = raw_input('For GPL license or conditions, type \'GPL\' or \'warranty\' (Enter for \'no\'):  ')
        if license == 'GPL':
            f=open('gpl.txt','r')
            gplContents=f.read()
            print gplContents
            print '\n\n'
            f.close()
            sys.exit()
        elif license == 'warranty':
            f=open('NO_WARRANTY.txt','r')
            gplWarranty=f.read()
            print gplWarranty
            print '\n\n'
            f.close()
            sys.exit()
        else:
            input = raw_input('\nEnter absolute/relative path to GeneMapper file:  ')
            try:
                input = os.path.abspath(string.strip(input))        #have to strip whitespace characters for dragging folders
                fileList=input
                #fileList=getFiles(input)                            #calls function above
            except:
                print 'The file does not exist '
                return 0
        format = raw_input('Enter format for output file \'cervus\'|\'genepop\'|\'gerud\' (Enter for default=cervus):  ')
        if not format:
            format = 'cervus'
            print (('\nOutput file format is %s\n') % (format))
        elif format not in ['cervus','genepop','gerud']:
            print 'You have chosen an output format that is not available!'
            sys.exit()
        output = raw_input('Enter absolute/relative path and filename for output file (Enter for default):  ')
        if not output:
            #output=''
            output, nullCharacter = getOutFileFormat(input, output, format)
        else:
            try:
                os.path.isdir(os.path.dirname(os.path.abspath(output)))
                nullCharacter = getOutFileFormat(input, output, format)[1]
            except:
                print 'This is not a valid path.  Make sure you have entered the path correctly.'
                sys.exit()
        #print ('\nOutput file written to %s') % (os.path.abspath(output))
    return fileList, output, format, nullCharacter



def getData(inputFile):
    dataPositionDict = {}         ###dict to hold positions of important keys
    #dataDict = {}         ##dont think we need this one
    abiFile = open(inputFile)
    abiHeader = abiFile.readline().split('\t')
    abiHeader = abiHeader[:-1]
    #-------------------------------------------------
    # columns we want to keep from the ABI data infile
    #-------------------------------------------------     
    importantStuff = {'Sample File':[], 'Sample Name':[], 'Marker':[], 'Allele 1':[], 'Allele 2':[], 'GQ':[]}
    abiHeaderCount = 0
    for i in abiHeader:
        if i in importantStuff.keys():
            dataPositionDict[i] = abiHeaderCount
            #print 'positionDict = ', dataPositionDict
            abiHeaderCount += 1
        else:
            abiHeaderCount += 1
    #--------------------------------
    # create list for marker names.  
    #--------------------------------
    markerList = []          
    for line in abiFile:
        splitLine = line.split('\t')
        #----------------------------------------------------------------------
        # Decided to get rid of what i thought was extraneous data (Panel, Dye)
        #----------------------------------------------------------------------
        id,nam,mark,all1,all2,g = splitLine[dataPositionDict['Sample File']], splitLine[dataPositionDict['Sample Name']], splitLine[dataPositionDict['Marker']], splitLine[dataPositionDict['Allele 1']], splitLine[dataPositionDict['Allele 2']], splitLine[dataPositionDict['GQ']]
        importantStuff['Sample File'] += [id]        ##abbrev. must be in brackets to append to list
        importantStuff['Sample Name'] += [nam]
        importantStuff['Marker'] += [mark]
        if all1 == '?':
            importantStuff['Allele 1'] += ['!!!Bin!!!']
        elif all1 == '':
            importantStuff['Allele 1'] += ['null']
        else:
            importantStuff['Allele 1'] += [int(all1)]
        if all2 == '?':
            importantStuff['Allele 2'] += ['!!!Bin!!!']
        elif all2 == '':
            importantStuff['Allele 2'] += ['null']
        else:
            importantStuff['Allele 2'] += [int(all2)]        
        importantStuff['GQ'] += [float(g)]        
        #--------------------------------------------------------------------------------------
        # list for unique marker names.  also implies marker names must be same (e.g. spelling)
        #--------------------------------------------------------------------------------------
        if mark not in markerList:        
            markerList.append(mark)         
    abiFile.close()                                 ###close the abi infile to make it happy
    uniqueSampleList=[]                             ###create empty dict for unique sample ID
    for item in importantStuff['Sample Name']:
        if item not in uniqueSampleList:
			uniqueSampleList.append(item)  
    return importantStuff, markerList, uniqueSampleList

def prepData(importantStuff, markerList, uniqueSampleList, nullCharacter, alleleFormat):
    #----------------------------------------------
    # build the generic individual/locus dictionary
    #----------------------------------------------
    locusDict={}
    for item in uniqueSampleList:        
        for element in markerList:
            if item not in locusDict.keys():
                locusDict[item]={element:['Null','Null']}
            else:
                locusDict[item][element]=['Null','Null']
    #-------------------------------------------------------------------------------------
    # fill in the actual data we are re-arraying on a per individual and per marker basis.
    #-------------------------------------------------------------------------------------
    i=0
    while i < len(importantStuff['Sample Name']):
        indiv=importantStuff['Sample Name'][i]
        marker=importantStuff['Marker'][i]
        #-------------------------------------------------------
        # replace nulls with null charac. and screen out GQ<0.75
        #-------------------------------------------------------
        if importantStuff['Allele 1'][i] != 'null' and importantStuff['GQ'][i] > 0.75:  ###replace nulls with null charac. and screen out GQ<0.75
            locusDict[indiv][marker][0] = importantStuff['Allele 1'][i]
        else:
            locusDict[indiv][marker][0] = nullCharacter
        #-------------------------------------------------------
        # replace nulls with null charac. and screen out GQ<0.75
        #-------------------------------------------------------
        if importantStuff['Allele 2'][i] != 'null' and importantStuff['GQ'][i] > 0.75:  ###replace nulls with null charac. and screen out GQ<0.75
            locusDict[indiv][marker][1] = importantStuff['Allele 2'][i]
        elif importantStuff['Allele 2'][i] == 'null' and importantStuff['Allele 1'][i] != 'null' and importantStuff['GQ'][i] > 0.75:
            locusDict[indiv][marker][1] = importantStuff['Allele 1'][i]
        else:
            locusDict[indiv][marker][1] = nullCharacter
        i+=1
    return locusDict, markerList
    
def formatOutFile(locusDict, markerList, programFormat, nullCharacter, output):
    #-----------------------------------------------------------------------------------------------------------------------
    # CERVUS formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
    #-----------------------------------------------------------------------------------------------------------------------
    if programFormat == 'cervus':
        headerString=['individual_id']
        markerList.sort()
        for item in markerList:
            headerString.append(item + 'A')        ###append A and B for 2 alleles for cervus format
            headerString.append(item + 'B')        ###append A and B for 2 alleles for cervus format
        outFile=open(output,'w')        ###this will be our handy data out file
        for item in headerString:
            outFile.write(('%s,') % (item))
        outFile.write('\r\n')
        #print 'locusDict keys', locusDict.keys()
        locusDictKeys=locusDict.keys()
        locusDictKeys.sort()
        #print 'sorted locusDict keys', data
        for item in locusDictKeys:
		    #print 'this is the locusDict item', item
		    outFile.write(('%s,') % (item))
		    for element in markerList:
		        #print element
		        outFile.write(('%s, %s,') % (locusDict[item][element][0], locusDict[item][element][1]))
		    outFile.write('\r\n')
        outFile.close()
    #------------------------------------------------------------------------------------------------------------------------
    # GENEPOP formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
    #------------------------------------------------------------------------------------------------------------------------
    if programFormat == 'genepop':
        headerString=['This GENEPOP input file was generated by GeneMapperConvert.  Yeah!']
        markerList.sort()
        for item in markerList:
            headerString.append(item)        ###
        outFile=open(output,'w')        ###this will be our handy data out file
        for item in headerString:
            outFile.write(('%s\r\n') % (item))
        outFile.write('POP\r\n')
        locusDictKeys=locusDict.keys()
        locusDictKeys.sort()
        for item in locusDictKeys:
    	    outFile.write(('%s\t,\t') % (item))
    	    for element in markerList:
    	        outFile.write(('%s%s\t') % (locusDict[item][element][0], locusDict[item][element][1]))
    	    outFile.write('\r\n')
        outFile.close()
    #----------------------------------------------------------------------------------------------------------------------
    # GERUD formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
    #----------------------------------------------------------------------------------------------------------------------
    if programFormat == 'gerud':
        locusDictKeys=locusDict.keys()
        locusDictKeys.sort()
        numberOfIndivs = len(locusDictKeys)
        numberOfLoci = len(markerList)
        outFile=open(output,'w')        ###this will be our handy data out file
        outFile.write(('%s embryos (or offspring or whatever)\r\n') % (numberOfIndivs))
        outFile.write(('%s loci (loci can be replaced by any other word as well)\r\n') % (numberOfLoci))
        markerList.sort()
        for item in markerList:
            outFile.write(('\t%s') % (item))
        outFile.write('\r\n')
        for item in locusDictKeys:
    	    outFile.write(('%s\t') % (item))
    	    for element in markerList:
    	        outFile.write(('%s/%s\t') % (locusDict[item][element][0], locusDict[item][element][1]))
    	    outFile.write('\r\n')
        outFile.close()
    


inputFile, outputFile, programFormat, nullCharacter = getUserFiles()
#fileFormat=getOutFileFormat(programFormat)
toPrepData=getData(inputFile)
locusData=prepData(toPrepData[0], toPrepData[1], toPrepData[2], nullCharacter,programFormat)
formatOutFile(locusData[0],locusData[1], programFormat, nullCharacter, outputFile)


