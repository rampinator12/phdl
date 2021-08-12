"""
Created on Fri Jul 30 15:18:33 2021

@author: dsr1
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 08:57:33 2021
​
@author: danar
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math

def parallel_pt_displacement(x1, x2, y1, y2,w): #gives x/y displacement from initial point of line
                                                # need to add these values to the left point to get the line                                    
    y_theta = y2-y1                             # essentially a vector length w perpendicular to original
    x_theta = x2-x1                             # line segment
    if y_theta > 0:
        if x_theta == 0:
            if y2 > y1:
                x = -w  #vertical line up
                y = 0
            else:
                x = w   #vertical line down
                y = 0
        else:
            theta = abs(np.arctan(y_theta/x_theta))  #sloped line up
            x = w*np.cos(theta + np.pi/2)
            y = w*np.sin(theta + np.pi/2)
    elif y_theta < 0:
        theta = abs(np.arctan(y_theta/x_theta))      #sloped line down
        x = w*np.cos(np.pi/2 - theta)
        y = w*np.sin(np.pi/2 - theta)
    elif y_theta == 0:
        x = 0
        y = w
    return [x, y]

def slope(x_tuple, y_tuple):
    m = (y_tuple[1]-y_tuple[0])/(x_tuple[1]-x_tuple[0])
    return m 

#Funtion that will return all necessary new values to plot new lines 
def new_values(x_list, y_list,w):  
    if len(x_list) != len(y_list):
        print('x and y list must be same size!')
        return
    else:
        x_add = []      #addition to x points always left point
        y_add = []      #addition to y points " "
        b_wide = []     # new y-int
        m_list = []     #slope list
        x_int = []      #intersection ptss of two lines
        
    for i in range(len(x)-1): #slope loop
        if x[i] == x[i+1]: #for vertical line set m to nan
            m_list.append(np.nan)
        else: 
            m_list.append(slope(x_list[i:i+2],y_list[i:i+2]))
        #append addition pts
        x_add.append(parallel_pt_displacement(x_list[i], x_list[i+1], y_list[i], y_list[i+1], w[i])[0]) 
        y_add.append(parallel_pt_displacement(x_list[i], x_list[i+1], y_list[i], y_list[i+1], w[i])[1]) 
    
    #now find the new y_intercepts of each new line 
    for i in range(len(x)-1):
        if m_list[i] is np.nan:
            b_wide.append(np.nan) #will never cross y axis with vertical line
        else:
            b_wide.append((y_list[i] + y_add[i]) -  m_list[i]*(x_list[i] + x_add[i]))
    
    #Now the x_intersection points of the new lines    
    for i in range(len(b_wide)-1):
        if b_wide[i+1] is np.nan:  #NOTE: initial line cannot be vertical
            x_int.append(x_list[i+1] + x_add[i+1])
            
        elif b_wide[i] is np.nan:
            x_int.append(x_int[i-1]) #for vertical segments x_int is the same

        else:
            x_int_val = (b_wide[i] - b_wide[i+1])/ (m_list[i+1] - m_list[i])
            x_int.append(x_int_val)
    
    wide_values = dict(
                    m_list = m_list,
                    b_wide = b_wide,
                    x_int = x_int,
                   )
    return wide_values

#return list of x/y points for 'wide' line
def wide_points(x_list, y_list, wide_values):
    x_wide = []
    y_wide = []
    m_list = wide_values.get('m_list')
    x_int = wide_values.get('x_int')
    b_wide = wide_values.get('b_wide')
    
    for i in range(len(x_list)):
        if i == 0:
            x_wide.append(x_list[i]) #starting line cannot be vertical
            y_wide.append(m_list[0]*x_list[i] + b_wide[0])
        elif (i > 0) and (i < (len(x_list)-1)):
            x_wide.append(x_int[i-1]) #sloped line 
            y_wide.append(m_list[i]*x_int[i-1]+b_wide[i])
        else:
            x_wide.append(x_list[len(x_list)-1])
            y_wide.append(m_list[i-1]*x_list[i]+b_wide[i-1])
    for i in range(len(y_wide)):
       if math.isnan(y_wide[i]) is True:
            if math.isnan(y_wide[i-1]) is False:
                y_wide[i] = m_list[i-1]*x_wide[i] + b_wide[i-1]
            elif math.isnan(y_wide[i+1]) is False:
                y_wide[i] = m_list[i]*x_wide[i] + b_wide[i]
    return x_wide, y_wide

#sets of x and y pts
def graph(x_list, y_list):
    for i in range(len(x)-1):
        points = np.linspace(x_list[i], x_list[i+1],10000)
        x_pt = [x_list[i], x_list[i+1]]
        y_pt = [y_list[i], y_list[i+1]]
        if x_list[i] == x_list[i+1]:
            plt.vlines(x_pt[0], y_pt[0], y_pt[1], colors = 'r')
        else:
            m, b = np.polyfit(x_pt, y_pt,1)
            plt.plot(points, points*m +b, colors = 'r')



#list of points/ widths. Note, width is n-1 to n points
#Change points/ width                
x = [0,1,3,3,4,5,5,6]
y = [0,-1,2,4,7,8,9,10]
w = [0.2,0.1,0.3,0.1,0.4,0.1,0.2]

vals = new_values(x,y,w)
x_wide, y_wide = wide_points(x, y, vals) 

#graphs original/ wide set
graph(x,y)           
graph(x_wide,y_wide)     
