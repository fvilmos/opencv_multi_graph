import cv2
import numpy as np
import os
from utils.multigraph import RealTimeMultiGraph

IMG_W = 640
IMG_H = 240
IMG_CHANNEL = 3
NR_OF_GRAPHS = 4

# create multi graph
rtmg = RealTimeMultiGraph(shape=[IMG_H,IMG_W,IMG_CHANNEL],nr_of_graphs=NR_OF_GRAPHS)

# set properties
rtmg.set_color(0,[0,0,255])
rtmg.set_color(1,[0,255,255])
rtmg.set_color(2,[255,0,255])

rtmg.set_scale(1,10)
rtmg.set_offset(1,110)

rtmg.set_scale(2,30)
rtmg.set_offset(2,180)

rtmg.set_scale(3,10)
rtmg.set_offset(3,30)
rtmg.set_marker(3,value=5,size=2,color=[0,0,255])

rtmg.set_title_and_position(0,"sin/10",(10,10))
rtmg.set_title_and_position(1,"sin/2",(10,20))
rtmg.set_title_and_position(2,"random",(10,30))
rtmg.set_title_and_position(3,"random1",(10,40))

count = 0
y0,y1,y2,y3 = 0,0,0,0

# generate sample data
while True:

    # reset img
    img = np.zeros([IMG_H,IMG_W,IMG_CHANNEL], dtype=np.uint8)
    
    # create data points
    y0 = np.sin(count/10)
    y1 = np.sin(count/2)
    
    if count % 20 == 0:
        y2 = np.random.choice([0,1])
    
    if count % 10 == 0:
        y3 = np.random.choice([0,1,2,3,4,5])

    # update the graphs
    rtmg.update_data_point(0,img,[0,y0])
    rtmg.update_data_point(1,img,[0,y1])
    rtmg.update_data_point(2,img,[0,-y2])
    rtmg.update_data_point(3,img,[0,y3])

    k = cv2.waitKey(10)

    if k== 27:
        os._exit(1)
    cv2.imshow('Real-Time Multi graph', img)
    
    count +=1
