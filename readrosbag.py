#!/usr/bin/env python
#!/usr/bin/python

import rospy
import pygame
import sys
from pygame.locals import *
from sensor_msgs.msg import CompressedImage,Image
import numpy as np
import cStringIO




pygame.init()
windowSurfaceObj = pygame.display.set_mode((320*3,240))
pygame.display.set_caption('SDC Viewer')
yellow = pygame.Color(245,210,0)
windowSurfaceObj.fill(pygame.Color(0,0,0))
pygame.display.update()

imgleft = pygame.surface.Surface((320,240),0,24).convert()
imgcenter = pygame.surface.Surface((320,240),0,24).convert()
imgright = pygame.surface.Surface((320,240),0,24).convert()

def scale_image(data):
    RGB_str = np.fromstring(data,dtype='uint8').reshape((640*480),3)[:,(2,1,0)].tostring()
    img = pygame.transform.scale(pygame.image.fromstring(RGB_str,(640,480),'RGB'),(320,240))
    return img

def compressedImageCB(ros_data):
    if ros_data._connection_header['topic'] == '/left_camera/image_color':
        imgleft = scale_image(ros_data.data)
        windowSurfaceObj.blit(imgleft,(0,0))
    elif ros_data._connection_header['topic'] == '/center_camera/image_color':
        imgcenter = scale_image(ros_data.data)
        windowSurfaceObj.blit(imgcenter,(320,0))
    elif ros_data._connection_header['topic'] == '/right_camera/image_color':
        imgright = scale_image(ros_data.data)
        windowSurfaceObj.blit(imgright,(640,0))
    
    pygame.display.update()


def listener():
    rospy.init_node('master',anonymous=True)
    rospy.Subscriber("/left_camera/image_color", Image, compressedImageCB)
    rospy.Subscriber("/center_camera/image_color",Image, compressedImageCB)
    rospy.Subscriber("/right_camera/image_color", Image, compressedImageCB)
    rospy.spin()


if __name__ == "__main__":
    listener()
