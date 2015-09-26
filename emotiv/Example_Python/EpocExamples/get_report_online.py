'''
Created on Oct 27, 2014

@author: Z88
'''

import sys,os
import time
 
from ctypes import cdll
from ctypes import CDLL
from ctypes import c_int
from ctypes import c_uint
from ctypes import pointer
from ctypes import c_char_p
 
userID = c_uint(0)
state = c_int(0)
connected = False
 
try :
    if sys.platform.startswith('win32'):     
        libEDK = cdll.LoadLibrary("edk.dll")
    if sys.platform.startswith('linux'):
        srcDir = os.getcwd()    
        libPath = srcDir + "/libedk.so.1.0.0"        
        libEDK = CDLL(libPath)
except :
    print 'Error : cannot load dll lib'   

class Reporter:
    '''
    class performs getting report online from the cloud       
    ''' 

    def __init__(self):
        '''
        Constructor
        '''
    def get_report_online(self, arg) :
        self.arg = c_uint(0)
        user_id = c_int(0)
        experimentID = c_int(0)
        protocolID = c_int(0)
        sessionID = c_char_p("")
        
        engagement = c_int(0)
        excitement = c_int(0)
        stress = c_int(0)
        relax = c_int(0)
        interest = c_int(0)
        hasReport = True
        
        print 'Getting report online : '
        if (libEDK.ELS_Connect() == False) :
            print 'Cannot connect to the cloud'
            sys.exit(1);
        else :
            print 'Connect to the cloud successful!'
            print 'Sign in...'
            clientID = ""
            clientSecret = ""
            libEDK.ELS_SetClientSecret(clientID, clientSecret)
            if libEDK.ELS_Login("jqk", "jqk", pointer(user_id)) == False :
    			print ' Login fail!'
    			#sys.exit(1);
            else :
    			print 'Login success!'
    			
			print "UserID : " , user_id.value
			print "Create protocol... "
			libEDK.ELS_CreateProtocol("new protocol", pointer(protocolID))
			print "ProtocolID : " , protocolID.value
			print "Create Experiment... "
			libEDK.ELS_CreateExperiment("test", "des", pointer(experimentID))
			print "Experiment : " , experimentID.value
			print 'Create Headset ...'
			libEDK.ELS_CreateHeadset(userID)
			print "Create Session... "
			# libEDK.ELS_CreateSession()                
			print "Session ID : " , libEDK.ELS_CreateRecordingSession()
			print "Start Record..."
			libEDK.ELS_StartRecordData()
			
			print "Create Marker..."
			libEDK.ELS_Marker_EyeOpenStart()                
			time.sleep(3)
			print "Create Marker..."
			libEDK.ELS_Marker_EyeOpenEnd()
			time.sleep(1)
			print "Create Marker..."
			libEDK.ELS_Marker_EyeClosedStart()
			time.sleep(3)
			print "Create Marker..." 
			libEDK.ELS_Marker_EyeClosedEnd()
			time.sleep(1)            
			print "Create Marker..." 
			libEDK.ELS_Marker_RecordingStart()
			time.sleep(5)
			print "Stop Record..."
			if libEDK.ELS_StopRecordData() == True :
				print "Success!"
				while hasReport :
					libEDK.ELS_GetReportOnline(pointer(engagement), pointer(excitement), pointer(stress), pointer(relax), pointer(interest))
					if engagement.value != 0 :
						print "Report is : " , engagement.value , excitement.value , stress.value , relax.value , interest.value
						hasReport = False
					else :
						print "Waiting for Report..."
					time.sleep(5)
			libEDK.ELS_Disconnect()                  
# end class Reporter       

if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
    print "Emotiv Engine start up failed."
    connected = False
else :
    print 'Emotiv Engine connected !'
    eEvent = libEDK.EE_EmoEngineEventCreate()       
    while True :
        state = libEDK.EE_EngineGetNextEvent(eEvent)
        if state == 0:
            eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
            libEDK.EE_EmoEngineEventGetUserId(eEvent, pointer(userID))
            if eventType == 16:  # libEDK.EE_Event_enum.EE_UserAdded:
                print "User added"
                # libEDK.EE_DataAcquisitionEnable(userID, True)
                connected = True
        if connected :
            reporter = Reporter()
            reporter.get_report_online(userID)
            break
        else :
            print 'Please connect to the headset'
        time.sleep(1)       
    'end while'                    
          
print "Exit..." 
