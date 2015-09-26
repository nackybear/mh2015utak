'''
Created on jul 03 , 2014
 *  edf_insight_exam.py
 *  This program is used to record EEG data into an EDF file and load EEG data
 *  from an EDF file. 
 *  
 *  Note: You have to following these steps to run this program with eclipse:
 *  Entering Run Configurations->environments->new then adding 
 *  LD_LIBRARY_PATH( in Linux ) / PATH ( in Window ) 
 *  and leading it to folder containing libraries. 
 *  
 *  EDF file is released in the following shape:
 *  File name  : you input
 *  PartientID : "EDFTest"  
 *  RecordID   : "0"
 *  Date       : "07.03.2013"
 *  Time       : "00:00:00"
@author: s-300pmu favorite2 + buk-m2e + pantsyr-s1
'''

import sys , os
import time
import ctypes

from ctypes import CDLL
from ctypes import c_void_p
from ctypes import c_int
from ctypes import c_uint
from ctypes import pointer
from ctypes import c_float

'load the library'
if sys.platform.startswith('linux2'):
    # libEDK = ctypes.CDLL("libedk.so.1.0.0")
    srcDir = os.getcwd()
    libPath = srcDir + "/libedk.so.1.0.0"
    # print libPath
     
    libEDK = CDLL(libPath)
    print "libedk load successfully"
elif sys.platform.startswith('win32') :
    libEDK = CDLL(".\\edk.dll")
    
write = sys.stdout.write
 
userID = c_uint(0)
user = pointer(userID)
option = c_int(0)
state = c_int(0)
connected = False
readytocollect = False
nSamples   = c_uint(0)
nSamplesTaken  = pointer(nSamples)
fileName = None
  
IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.restype = c_void_p
eEvent = IEE_EmoEngineEventCreate()
  
IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()
  
IEE_DataCreate = libEDK.IEE_DataCreate
IEE_DataCreate.restype = c_void_p
hData = IEE_DataCreate()
 
print " ====================================================================="
print " Example  to show how to record and load the EEG data "
print " ====================================================================="
 
' connect to emoengine'
if libEDK.IEE_EngineConnect("Emotiv Systems-5") != 0:
    print "Emotiv Engine start up failed."
    connected = False
else :
    connected = True
    
    while ( connected ) :
        state = libEDK.IEE_EngineGetNextEvent(eEvent)
        if state == 0:
            eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
            libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
            
            if eventType == 16 : #libEDK.IEE_Event_enum.IEE_UserAdded :
                print " User Added"
                libEDK.IEE_DataAcquisitionEnable(userID,True)
                readytocollect = True;
        elif state != 1536 : #libEDK.IEE_Event_enum.EDK_NO_EVENT :
            print "Internal error in Emotiv Engine!"
        if readytocollect :            
            libEDK.IEE_DataUpdateHandle(0, hData)
            libEDK.IEE_DataGetNumberOfSample(hData,nSamplesTaken) 
            print " sample : %d " %nSamplesTaken[0]
            
            if nSamplesTaken[0] != 0:
                print "\n ===================================================================";
                print "\n Press '1' to record EEG data into EDF file "
                print "\n Press '2' to load data from EDF file "
                print "\n Press '3' to exit "
                print"\n Option : "
                option = int(raw_input())
                
                if option == 1 :  
                    fileName = raw_input("Please input filename : ")
                    libEDK.IEE_EdfStartSaving( userID , fileName,"edfTest", "0", "07.03.2014", "00:00:00");
                    
                    'work something here'
                    for i in range(0, 10) :
                        print " Saving eeg data..."
                        time.sleep(1)
                    
                    libEDK.IEE_EdfStopSavingAll()
                    print " Saving success. "
                    connected = True                    
                if option == 2 :                    
                    if connected == True :
                        libEDK.IEE_EngineDisconnect()
                        readytocollect = False
                    
                    fileName = raw_input("Please input filename : ")
                    if libEDK.IEE_EngineLocalConnect(fileName) != 0 :
                        print "Emotiv Engine with EDF file start up failed. "
                    else :    
                        'start playback EDF file'
                        print "loading..."
                        libEDK.IEE_EdfStart()
                        time.sleep(1)
                        print "load success!"
                    connected = True
                if option == 3 :
                    print " Bye !"
                    connected = False   
            
libEDK.IEE_EngineDisconnect()
libEDK.IEE_EmoStateFree(eState)
libEDK.IEE_EmoEngineEventFree(eEvent)




