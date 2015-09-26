'''
Created on Nov 14, 2014

@author: Z88
'''


import sys , os

from ctypes import cdll
from ctypes import CDLL
from ctypes import pointer
from ctypes import c_int

user_id = c_int(0)

try :
    if sys.platform.startswith('win32'):     
        libEDK = cdll.LoadLibrary("edk.dll")
    if sys.platform.startswith('linux'):
        srcDir = os.getcwd()    
        libPath = srcDir + "/libedk.so.1.0.0"        
        libEDK = CDLL(libPath)
except :
    print 'Error : cannot load dll lib' 
    
def print_profile_detail(): 
    num_profile = libEDK.ELS_GetAllProfileName()
    print "Number of profiles : ", num_profile
    if num_profile > 0 :
        for i in range(num_profile) :
            print "Profile Id   : ", libEDK.ELS_ProfileIDAtIndex(i)
            print "Profile name : ", libEDK.ELS_ProfileNameAtIndex(i)
            if libEDK.ELS_ProfileTypeAtIndex(i) == 0:
                print "Profile type  : TRAINING "
            else :
                print "Profile type  : EMOKEY "     
                       
            print "Last modified : ",libEDK.ELS_ProfileLastModifiedAtIndex(i)
        #end for 
if (libEDK.ELS_Connect() == False) :
    print 'Cannot connect to the cloud'
    sys.exit(1);
else :        
    print 'Connect to the cloud successful!'
    print 'Sign in...'
    if libEDK.ELS_Login("jqk", "jqk", pointer(user_id)) == False :
        print ' Login fail!'
        sys.exit(1);
    else :
        print 'Login success!'        
        print "UserID : " , user_id.value
        print_profile_detail()
        if libEDK.ELS_UploadProfileFile("profile 1", "profile1.emu",0) == False :
            print " Fail to upload profile file !"
        else :
            print " Profile file was uploaded successfully! "
            print_profile_detail()
            num_id = libEDK.ELS_GetProfileId("profile 1")        
            if num_id >= 0 :
                libEDK.ELS_DownloadFileProfile(num_id, "profile1.emu")
                print " Delete profile ..."
                libEDK.ELS_DeleteProfileFile(num_id)
            #end if
            print " List profiles after delete: "
            print_profile_detail()
    #end else
#end    