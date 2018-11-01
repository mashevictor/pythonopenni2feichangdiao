#!/usr/bin/env python
import numpy as np
import cv2
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

dist ='/home/victor/software/OpenNI-Linux-x64-2.3/Redist'

## Initialize openni and check
openni2.initialize(dist) #
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"

## Register the device
dev = openni2.Device.open_any()

## Create the streams stream
depth_stream = dev.create_depth_stream()

## Configure the depth_stream -- changes automatically based on bus speed
#print 'Get b4 video mode', depth_stream.get_video_mode() # Checks depth video configuration
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320, resolutionY=240, fps=30))

## Check and configure the mirroring -- default is True
# print 'Mirroring info1', depth_stream.get_mirroring_enabled()
depth_stream.set_mirroring_enabled(False)


## Start the streams
depth_stream.start()

## Use 'help' to get more info
# help(dev.set_image_registration_mode)

def get_depth():
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240,320)  # Works & It's FAST
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    # Shown unknowns in black
    d4d = 255 - d4d    
    return dmap, d4d
#get_depth


## main loop
s=0
done = False
while not done:
    key = cv2.waitKey(1)
    ## Read keystrokes
    key = cv2.waitKey(1) & 255
    ## Read keystrokes
    if key == 27: # terminate
        print "\tESC key detected!"
        done = True
    elif chr(key) =='s': #screen capture
        print "\ts key detected. Saving image and distance map {}".format(s)
        cv2.imwrite("ex1_"+str(s)+'.png', d4d)
        np.savetxt("ex1dmap_"+str(s)+'.out',dmap)
        #s+=1 # uncomment for multiple captures   
    #if
    
    ## Streams    
    #DEPTH
    dmap,d4d = get_depth()
    #print 'Center pixel is {}mm away'.format(dmap[119,159])
    #print (d4d)
    ## Display the stream syde-by-side
    cv2.imshow('depth', d4d)
# end while

## Release resources 
cv2.destroyAllWindows()
depth_stream.stop()
openni2.unload()
print ("Terminated")
