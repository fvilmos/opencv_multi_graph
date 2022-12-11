# https://github.com/fvilmos/opencv_multi_graph/edit/master/test_multigraph.py
# Author: fvilmos
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
rtmg.graphs_array[0].set_color([0,0,255])
rtmg.graphs_array[1].set_color([0,255,255])
rtmg.graphs_array[2].set_color([255,0,255])

rtmg.graphs_array[1].set_scale(10)
rtmg.graphs_array[1].set_offset(110)

rtmg.graphs_array[2].set_scale(30)
rtmg.graphs_array[2].set_offset(180)

rtmg.graphs_array[3].set_scale(10)
rtmg.graphs_array[3].set_offset(30)
rtmg.graphs_array[3].set_marker(value=5,size=2,color=[0,0,255])


rtmg.graphs_array[0].set_title_and_position("sin/10",(10,10))
rtmg.graphs_array[1].set_title_and_position("sin/2",(10,20))
rtmg.graphs_array[2].set_title_and_position("random",(10,30))
rtmg.graphs_array[3].set_title_and_position("random1",(10,40))



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
    rtmg.update_data_point(img,[0,y0],0)
    rtmg.update_data_point(img,[0,y1],1)
    rtmg.update_data_point(img,[0,-y2],2)
    rtmg.update_data_point(img,[0,y3],3)

    k = cv2.waitKey(10)

    if k== 27:
        os._exit(1)
    cv2.imshow('Real-Time Multi graph', img)
    
    count +=1
