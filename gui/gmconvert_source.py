#!/usr/local/bin/pythonw

#-----------------------------------------------------------------------------------------------|
# GeneMapperConvert - source for GUI                                                            |
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

import string, sys, os
import wx
 
idAbout = wx.NewId()
idOpen  = wx.NewId()
idExit  = wx.NewId()
 
class userVar:
    def __init__(self,input,format,output):
        self.input = input
        self.format = format
        self.output = output

class abiData(userVar):
    def getOutFileFormat(self):
        #-----------------------------------------
        # set nullCharacter for cervus (default)
        #-----------------------------------------
        if self.format == 'cervus':  
            self.nullCharacter = '*'
        #----------------------------
        # other nullCharacter options
        #----------------------------
        elif self.format == 'genepop':
            self.nullCharacter = '000'
        elif self.format == 'gerud':
            self.nullCharacter = 'Nulls Not Allowed!'
        else:
            self.nullCharacter = '*'
        self.getData()                  #call getData() function
        #return self.nullCharacter

    def getData(self):
        dataPositionDict = {}         ###dict to hold positions of important keys
        #print self.input
        abiFile = open(self.input,'r')
        abiHeader = abiFile.readline()
        abiHeader = abiHeader.strip('\r\n').split('\t')
        #print abiHeader        
        #-------------------------------------------------
        # columns we want to keep from the ABI data infile
        #-------------------------------------------------
        importantStuff = {'Sample File':[], 'Sample Name':[], 'Marker':[], 'Allele 1':[], 'Allele 2':[], 'GQ':[]}
        abiHeaderCount = 0
        for i in abiHeader:
            if i in importantStuff.keys():
                dataPositionDict[i] = abiHeaderCount
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
        self.prepData(importantStuff, markerList,uniqueSampleList)
        #print importantStuff,markerList,uniqueSampleList
        #return importantStuff, markerList, uniqueSampleList

    def prepData(self,importantStuff, markerList, uniqueSampleList): #removed nullCharacter and programFormat
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
            if importantStuff['Allele 1'][i] != 'null' and importantStuff['GQ'][i] > 0.75:  
                locusDict[indiv][marker][0] = importantStuff['Allele 1'][i]
            else:
                locusDict[indiv][marker][0] = self.nullCharacter
            #-------------------------------------------------------
            # replace nulls with null charac. and screen out GQ<0.75
            #-------------------------------------------------------
            if importantStuff['Allele 2'][i] != 'null' and importantStuff['GQ'][i] > 0.75:  
                locusDict[indiv][marker][1] = importantStuff['Allele 2'][i]
            elif importantStuff['Allele 2'][i] == 'null' and importantStuff['Allele 1'][i] != 'null' and importantStuff['GQ'][i] > 0.75:
                locusDict[indiv][marker][1] = importantStuff['Allele 1'][i]
            else:
                locusDict[indiv][marker][1] = self.nullCharacter
            i+=1
        #print locusDict, markerList
        self.formatOutFile(locusDict,markerList)
        #return locusDict, markerList

    def formatOutFile(self,locusDict, markerList): #removed programFormat, nullCharacter, output
        #-----------------------------------------------------------------------------------------------------------------------
        # CERVUS formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
        #-----------------------------------------------------------------------------------------------------------------------
        if self.format == 'cervus' or self.format == '':
            headerString=['individual_id']
            markerList.sort()
            for item in markerList:
                headerString.append(item + 'A')         ###append A and B for 2 alleles for cervus format
                headerString.append(item + 'B')         ###append A and B for 2 alleles for cervus format
            outFile=open(self.output,'w')                    ###this will be our handy data out file
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
    		        outFile.write(('%s,%s,') % (locusDict[item][element][0], locusDict[item][element][1]))
    		    outFile.write('\r\n')
            outFile.close()
        #------------------------------------------------------------------------------------------------------------------------
        # GENEPOP formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
        #------------------------------------------------------------------------------------------------------------------------
        if self.format == 'genepop':
            headerString=['This GENEPOP input file was generated by GeneMapperConvert.  Yeah!']
            markerList.sort()
            for item in markerList:
                headerString.append(item)        ###
            outFile=open(self.output,'w')        ###this will be our handy data out file
            for item in headerString:
                outFile.write(('%s\r\n') % (item))
            outFile.write('POP\r\n')
            locusDictKeys=locusDict.keys()
            locusDictKeys.sort()
            #print 'locusDict is', locusDict
            for item in locusDictKeys:
        	    outFile.write(('%s\t,\t') % (item))
        	    for element in markerList:
        	        outFile.write(('%s%s\t') % (locusDict[item][element][0], locusDict[item][element][1]))
        	    outFile.write('\r\n')
            outFile.close()
        #----------------------------------------------------------------------------------------------------------------------
        # GERUD formatting section (sections for individual programs will be kept seperate to minimize confusion - mostly mine)
        #----------------------------------------------------------------------------------------------------------------------
        if self.format == 'gerud':
            locusDictKeys=locusDict.keys()
            locusDictKeys.sort()
            numberOfIndivs = len(locusDictKeys)
            numberOfLoci = len(markerList)
            outFile=open(self.output,'w')        ###this will be our handy data out file
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



#---------------------------------
# GUI class for wxPython (windows)
#---------------------------------
class GMConvertFrame(wx.Frame):
    """Main wxPython class for GMConvert"""
    title = "gmconvert"
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,-1,self.title,size=(350,250), style=wx.DEFAULT_FRAME_STYLE)
        #wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(350, 250)) #old init subclass
        color=(255,255,255)
        self.SetBackgroundColour(color)
        wx.StaticText(self, -1, self.frameText())
        self.CreateStatusBar()
        self.SetStatusText("")
        
        #create the file menu
        menu1 = wx.Menu()
        menu1.Append(idOpen, "&Convert...\tCtrl-C","Open a file for conversion")
        
        #and the help menu
        menu2 = wx.Menu()
        menu2.Append(idAbout, "&About\tCtrl-H", "Display Help")
        
        #add menu items to menubar
        menuBar = wx.MenuBar()
        menuBar.Append(menu1, "&File");
        menuBar.Append(menu2, "&Help") 
        self.SetMenuBar(menuBar)
        
        #setup events
        self.Bind(wx.EVT_MENU, self.OnAbout, id=idAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=idOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, id=idExit)
         
    def frameText(self):
        version = 'GMCONVERT 0.32\n'
        license = 'Released Under the Gnu Public License v2\n\n'
        instruct   = '  Instructions:\n'
        firstStep  = '    1)  Choose File > Convert...\n'
        secondStep = '    2)  Select File to Convert\n'
        thirdStep  = '    3)  Select Conversion Format\n'
        fourthStep = '    4)  Select Location to Save File and Filename\n'
        fifthStep  = '    5)  Enjoy'
        text = (('%s %s %s %s %s %s %s %s') % (version, license, instruct, firstStep, secondStep, thirdStep, fourthStep, fifthStep))
        return text
        
    
    def OnAbout(self, event):
        messageText = 'This program converts exported data files from Applied Biosystems (TM) GeneMapper (TM) Software to several popular formats'
        windowTitle = 'GMConvert'
        dlg = wx.MessageDialog(self, messageText, windowTitle, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def runConversion(self):
        abiData(self.infile,self.selection,self.outfile).getOutFileFormat()

    def saveFile(self):
        messageText = 'Choose a Location to Save the Output File'
        dlg = wx.FileDialog(self, messageText)
        dlg.SetStyle(wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.outfile = dlg.GetPath()
            self.runConversion()
            dlg.Destroy()
        else:
            messageText = 'You must specify an output file!'
            windowTitle = 'Error'
            error = wx.MessageDialog(self, messageText, windowTitle, wx.OK | wx.ICON_INFORMATION)
            error.ShowModal()
            error.Destroy()
            dlg.Destroy()

    def userChoice(self):
        choices = [ 'cervus', 'genepop', 'gerud','','','']
        messageText = 'Format for Outfile:'
        windowTitle = 'Conversion Format'
        style = (wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.OK | wx.CENTRE)                       
        # Create the dialog
        dlg = wx.SingleChoiceDialog (None, messageText, windowTitle, choices, style)
        # Show the dialog
        #dlg.ShowModal()
        if dlg.ShowModal() == wx.ID_OK:
            self.selection = dlg.GetStringSelection() #get user response
            self.saveFile()
        # Destroy the dialog
        dlg.Destroy()

    def OnOpen(self,event):
        dlg = wx.FileDialog(self, 'Choose a File for Conversion')
        dlg.SetStyle(wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.infile = dlg.GetPath()                                                       
            self.userChoice()
            dlg.Destroy()  
        else:
            messageText = 'You must specify an input file!'
            windowTitle = 'Error'
            error = wx.MessageDialog(self, messageText, windowTitle, wx.OK | wx.ICON_INFORMATION)
            error.ShowModal()
            error.Destroy()        
            dlg.Destroy()
        
       
    def OnExit(self, event):
        self.Close()

#---------------------------------
# Main class for wxPython interface
#---------------------------------
class GMConvert(wx.App):
    def OnInit(self):
        frame = GMConvertFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
 
if __name__ == '__main__':
    app = GMConvert(redirect=True)
    app.MainLoop()  