#!/usr/bin/env python
import numpy as np
import cv2
from primesense import openni2
from primesense import _openni2 as c_api
np.set_printoptions(threshold=np.inf)
dist ='/home/victor/software/OpenNI-Linux-x64-2.3/Redist'
openni2.initialize(dist)
if (openni2.is_initialized()):
    print "openNI2 initialized"
else:
    print "openNI2 not initialized"
dev = openni2.Device.open_any()
rgb_stream = dev.create_color_stream()
depth_stream = dev.create_depth_stream()
rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=640, resolutionY=480, fps=30))
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=640, resolutionY=480, fps=30))
rgb_stream.start()
depth_stream.set_mirroring_enabled(False)
depth_stream.start()
depth_stream.set_mirroring_enabled(False)
rgb_stream.set_mirroring_enabled(False)
def get_rgb():
    bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(480,640,3)
    rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    return rgb
def get_depth():
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(480,640)
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1)
    d4d = cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    d4d = 255 - d4d
    #print ("*******************yizhangtupian*************************")
    #print (dmap.shape)
    #print ("*******************yizhangtupian[0]gao*************************")
    #print (dmap.shape[0])
    #print ("*******************yizhangtupian[1]kuan*************************")
    #print (dmap.shape[1])
    return dmap, d4d
s=0
done = False
while not done:
    key = cv2.waitKey(1) & 255
    if key == 27:
        print "\tESC key detected!"
        done = True
    elif chr(key) =='s':
        print "\ts key detected. Saving image {}".format(s)
        cv2.imwrite("ex2_"+str(s)+'.png', rgb)
        cv2.imwrite("ex1_"+str(s)+'.png', d4d)
        np.savetxt("ex1dmap_"+str(s)+'.out',dmap)
    dmap,d4d = get_depth()
    rgb = get_rgb()
    #print (dmap)
    cv2.imshow('rgb', rgb)
    cv2.imshow('depth', d4d)
cv2.destroyAllWindows()
rgb_stream.stop()
openni2.unload()
print ("Terminated")
