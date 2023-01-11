#https://github.com/fvilmos/opencv_multi_graph
# Author: fvilmos

import cv2
import numpy as np

"""
Utility function to draw real time single / multi graph in opencv
Author: fvilmos
"""

class RealTimeGraph():
    """
    Draws a simple real time plot in opencv
    """
    def __init__(self,shape=[240,320,3],scale=120,offset=120) -> None:
        """
        Args:
            shape (list, optional): the size of the graph. Defaults to [240,320,3].
            scale (int, optional): graph scale. Defaults to 120.
            offset (int, optional): offset, usualy the half of the height. Defaults to 120.
        """
        self.shape = shape
        self.scale = scale
        self.offset = offset
        self.buffer = np.array([[i,offset] for i in range (self.shape[1])])
        self.color = [0,255,0]
        self.title = ''
        self.title_position=(10,10)
        self.marker_size=3
        self.marker_value=0
        self.maker_color=[0,255,0]
    
    def update_data_point(self,img,data):
        """
        add a data point to the graph
        Args:
            img (_type_): image to draw
            data (_type_): datapoint i.e. [0,10]
        """

        # shape data
        self.buffer = self.buffer.reshape((-1, 1, 2)).astype(np.int)
        
        #delete oldest, add newest
        self.buffer = np.delete(self.buffer,0,axis=0)
        self.buffer[:,:,0:1] = self.buffer[:,:,0:1] - 1

        data_point = np.array([self.shape[1]-1,data[1]*self.scale+self.offset]).reshape((-1, 1, 2)).astype(np.int)
        self.buffer = np.append(self.buffer,data_point).reshape((-1, 1, 2)).astype(np.int)
        
        # show title if available
        if self.title != '':
            self.puttext_bg(img,self.title, position=self.title_position,font_color=self.color)

        # add marker
        if self.marker_value != 0:
            scaled_arr = (self.buffer[:,:,1:2]-self.offset)//self.scale
            indx_list = np.argwhere(scaled_arr==self.marker_value)
            if len(indx_list)>0:
                for v in indx_list:
                    y = self.marker_value*self.scale+self.offset
                    cv2.circle(img,(v[0],y),self.marker_size,self.maker_color,-1)


        cv2.polylines(img, [self.buffer],False, self.color, 1)
    
    
    def puttext_bg(self,img,text='',position=(10,160), font_type=None, font_size=0.4, font_color=[0,255,0],bg_color=[0,0,0],font_thickness=1):
        """
        Text with background color
        Args:
            img (_type_): _description_
            text (str, optional): Defaults to ''.
            position (tuple, optional): Defaults to (10,160).
            font_type (_type_, optional): Defaults to None.
            font_size (float, optional): Defaults to 0.4.
            font_color (list, optional): Defaults to [0,255,0].
            bg_color (list, optional): Defaults to [0,0,0].
            font_thickness (int, optional): Defaults to 1.
        """

        if font_type is None:
            font_type = cv2.FONT_HERSHEY_SIMPLEX
        (t_w,t_h),_ = cv2.getTextSize(text, font_type, font_size, font_thickness)
        cv2.rectangle(img, position, (position[0] + t_w, position[1] + t_h), bg_color, -1)
        cv2.putText(img,text ,(position[0], int(position[1]+t_h+font_size-1)),font_type,font_size,font_color,font_thickness)


class RealTimeMultiGraph():
    """
    Draws a real time multi graph
    """
    def __init__(self,shape=[240,320,3],scale=120,offset=120,nr_of_graphs=1):
        """
        Init the graps
        Args:
            shape (list, optional): Defaults to [240,320,3].
            scale (int, optional):  Defaults to 120.
            offset (int, optional):  Defaults to 120.
            nr_of_graphs (int, optional): Defaults to 1.
        """
        self.nr_of_graphs = nr_of_graphs
        
        self.graphs_array = []
        for i in range (nr_of_graphs):
            self.graphs_array.append(RealTimeGraph(shape=shape,scale=scale,offset=offset))
    
    def __check_idenx_val(self,index):
        """
        Check if praph index is in the range

        Args:
            index (int): graph index

        Returns:
            boolean: True if index values is in range, else false
        """
        ret = False
        if index < len(self.graphs_array):
            ret = True

        return ret
    
    def update_data_point(self,index,img,data):
        """
        Update the data point on a specific graph using the index
        Args:
            index (int): Graph index. Defaults to 0.
            img (array): image to draw
            data (int): data point to draw. i.e. [0,255]
        """
        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].update_data_point(img,data)
    
    def set_scale(self,index,scale):
        """
        graph scale
        Args:
            index (int): graph number
            scale (int): graph scaleing factor
        """
        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].scale = scale
    
    def set_offset(self,index,offset):
        """
        Data offset, usually the haf of the height

        Args:
            index (int): graph number
            offset (int): int, usually the half of the height
        """
        
        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].offset = offset
        self.graphs_array[index].buffer = np.array([[i,offset] for i in range (self.graphs_array[index].shape[1])])
    
    def set_color(self,index, color):
        """
        Graph/text color
        Args:
            index (int): graph number
            color (list): i.e. [0,255,0] in BGR format
        """
        
        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].color = color
    
    def set_title_and_position(self,index,name='',postion=(10,10)):
        """
        Set graph title and position
        Args:
            index (int): graph number
            name (str, optional): set the name of the title. Defaults to ''.
            postion (tuple, optional): Defaults to (10,10).
        """
        
        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].title = name
        self.graphs_array[index].title_position = postion

    
    def set_marker(self,index,value=0, size=3, color=[0,255,0]):
        """
        Set a circle on the graph to mark a value
        Args:
            index (int): graph number
            value (int, optional): The value whre the marker will be activated. Defaults to 0.
            size (int, optional): Marker is a circle, the size define the radius. Defaults to 3.
        """

        if self.__check_idenx_val(index)==False:
            print ('\n==graph index {} out of range!!!==\n'.format(int(index)))

        self.graphs_array[index].marker_size=size
        self.graphs_array[index].marker_value=value
        self.graphs_array[index].maker_color=color


