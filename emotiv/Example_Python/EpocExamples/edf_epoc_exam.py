'''
Created on jul 03 , 2014
 *  edf_epoc_exam.py
 *  This program is used to record EEG data into an EDF file and load EEG data
 *  from an EDF file. 
 *  
 *  EDF file is released in the following shape:
 *  File name  : you input
 *  PartientID : "EDFTest"  
 *  RecordID   : "0"
 *  Date       : "07.03.2013"
 *  Time       : "00:00:00"
@author: s-300pmu favorite2 + buk-m2e + pantsyr-s1
'''

import sys,os
import time
import ctypes

from ctypes import *

try :
    if sys.platform.startswith('win32'):     
        libEDK = cdll.LoadLibrary("edk.dll")
    if sys.platform.startswith('linux'):
        srcDir = os.getcwd()    
        libPath = srcDir + "/libedk.so.1.0.0"        
        libEDK = CDLL(libPath)
except :
    print 'Error : cannot load dll lib'
    
write = sys.stdout.write
 
userID = c_uint(0)
user = pointer(userID)
option = c_int(0)
state = c_int(0)
connected = False
readytocollect = False
nSamples   = c_uint(0)
nSamplesTaken  = pointer(nSamples)
fileInput = None
fileOutput = None
  
EE_EmoEngineEventCreate = libEDK.EE_EmoEngineEventCreate
EE_EmoEngineEventCreate.restype = c_void_p
eEvent = EE_EmoEngineEventCreate()
  
EE_EmoStateCreate = libEDK.EE_EmoStateCreate
EE_EmoStateCreate.restype = c_void_p
eState = EE_EmoStateCreate()
  
EE_DataCreate = libEDK.EE_DataCreate
EE_DataCreate.restype = c_void_p
hData = EE_DataCreate()
 
print " ====================================================================="
print " Example  to show how to record and load the EEG data "
print " ====================================================================="
 
' connect to emoengine'
if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
    print "Emotiv Engine start up failed."
    connected = False
else :
    connected = True
    
while ( connected ) :
    state = libEDK.EE_EngineGetNextEvent(eEvent)
    if state == 0:
        eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
        libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
        
        if eventType == 16 : #libEDK.EE_Event_enum.EE_UserAdded :
            print " User Added"
            libEDK.EE_DataAcquisitionEnable(userID,True)
            readytocollect = True;
    elif state != 1536 : #libEDK.EE_Event_enum.EDK_NO_EVENT :
        print "Internal error in Emotiv Engine!"
    if readytocollect :            
        libEDK.EE_DataUpdateHandle(0, hData)
        libEDK.EE_DataGetNumberOfSample(hData,nSamplesTaken) 
        print " sample : %d " %nSamplesTaken[0]
        
        if nSamplesTaken[0] != 0:
            print "\n ===================================================================";
            print "\n Press '1' to record EEG data into EDF file "
            print "\n Press '2' to load data from EDF file "
            print "\n Press '3' to exit "
            print"\n Option : "
            option = int(raw_input())
            
            if option == 1 :  
                fileInput = raw_input("Please input filename : ")
                libEDK.EE_EdfStartSaving( userID , fileInput,"edfTest", "0", "07.03.2014", "00:00:00");
                
                'work something here'
                for i in range(0, 10) :
                    print " Saving eeg data..."
                    time.sleep(1)
                
                libEDK.EE_EdfStopSavingAll()
                print " Saving success. "
                connected = True                    
            if option == 2 :                    
                if connected == True :
                    libEDK.EE_EngineDisconnect()
                    readytocollect = False
                    time.sleep(1)
                    
                fileOutput = raw_input("Please input filename : ")
                if libEDK.EE_EngineLocalConnect( fileOutput ) != 0 :
                    print "Emotiv Engine with EDF file start up failed. "
                else :    
                    'start playback EDF file'
                    print "loading..."
                    libEDK.EE_EdfStart()
                    time.sleep(1)
                    print "load success!"
                    connected = True
            if option == 3 :
                print " Bye !"
                connected = False   
            
libEDK.EE_EngineDisconnect()
libEDK.EE_EmoStateFree(eState)
libEDK.EE_EmoEngineEventFree(eEvent)




