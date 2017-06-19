'''
Julian Smoller ~ 2017

This module contains a Timeline class, which can plot time ranges 
as horizontal lines on an image.
'''
from PIL import Image
import pandas as pd
import numpy as np
from datetime import datetime


class Timeline:
    def __init__(self,time_ranges,x_pixels=1000):
        '''Given a dataframe of time ranges with start times and end times, 
        create a timeline image with horizontal lines for each time range:
        Initialize with min time (time_0), max time (time_1), and the number of pixels
        in the x dimension (x_pixels) that we can use for the width of the image'''
        self.time_ranges = time_ranges[['start_time','end_time']].copy().reset_index(drop=True)
        self.time_0 = self.time_ranges['start_time'].min()
        self.time_1 = self.time_ranges['end_time'].max()
        self.x_pixels = x_pixels
        self.time_range = self.time_1-self.time_0
        self.time_per_pixel = self.time_range/self.x_pixels 
        self.time_ranges_mapped = False # flag
    def log(self):
        '''Print out the object properties'''
        print(self.time_0)
        print(self.time_1)
        print(self.x_pixels)
        print(self.time_range)
        print(self.time_per_pixel)
    def map_time_to_x(self,t):
        '''Given a time within the timeline range, convert to x pixel coordinates'''
        if t>=self.time_0 and t<=self.time_1:
            x = int(((t-self.time_0)/self.time_range)*self.x_pixels)
            return x
        else:
            print(t)
            raise Exception('Time value outside of timeline range')
    def map_time_ranges(self,y_pixel_increment = 3,y_pixel_width=2):
        '''Iterate through the set of time ranges and map each start time and 
        end time to corresponding pixel coordinates (x0 and x1); set y values to space out the 
        time ranges vertically, and give each line some width (y_pixel_width)'''
        self.y_pixel_increment = y_pixel_increment
        self.y_pixel_width = y_pixel_width
        self.time_ranges['x0'] = self.time_ranges['start_time'].map(lambda t: self.map_time_to_x(t))
        self.time_ranges['x1'] = self.time_ranges['end_time'].map(lambda t: self.map_time_to_x(t))
        self.time_ranges['y0'] = self.time_ranges.index.map(lambda i: 
                                                           (i+1)*self.y_pixel_increment+i*self.y_pixel_width)
        self.time_ranges['y1'] = self.time_ranges['y0'].map(lambda y: y+self.y_pixel_width)
        self.time_ranges_mapped = True
    def plot(self):
        '''Generate a timeline image and plot the time ranges as horizontal lines'''
        if not self.time_ranges_mapped:
            self.map_time_ranges()
        x_max = self.x_pixels
        y_max = self.time_ranges['y1'].max()+self.y_pixel_increment
        self.image = Image.new('RGB',(x_max,y_max),'white')
        for time_range in self.time_ranges.iterrows():
            for x in range(time_range[1]['x0'],time_range[1]['x1']):
                for y in range(time_range[1]['y0'],time_range[1]['y1']):
                    self.image.putpixel((x,y),(0,0,0))
        return self.image