#!/usr/bin/env python
# coding=utf-8

import numpy as np
import math

frame_num = 64
box_num = 81
video_name = "bolt"
init_torrent = 5
iteration_torrent=2
accept_rate = 0.9


def get_tolerent(x0,y0,x1,y1):
    dis = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    if dis < max_distance:
        return True
    else:
        return False

max_distance = init_torrent
waiting_list = np.arange(1, box_num+1)
for frame in range(1, frame_num - 1):
    max_distance = init_torrent
    while True:
        select_index = np.random.randint(1,len(waiting_list),3)
        select_index = np.array(select_index)
        select_list = waiting_list[select_index]
        #select_list = np.random.randint(1, box_num, 3)
        rest_list = [i for i in waiting_list if i not in select_list]
        x,y,x_,y_=np.zeros(10),np.zeros(10),np.zeros(10),np.zeros(10)
        index=0
        for j in select_list:
            #curr_num = [],x=[],y=[]
            f = open(video_name + "_" + str(j), "r")
            raw = f.readlines()[frame - 1:frame + 1]
            curr_p = raw[0].split()
            next_p = raw[1].split()
            xr,yr,w,h = float(curr_p[1]),float(curr_p[2]),float(curr_p[3]),float(curr_p[4])
            xr_,yr_,w_,h_ = float(next_p[1]),float(next_p[2]),float(next_p[3]),float(next_p[4])
            x[index] = xr+w/2
            y[index] = yr+h/2
            x_[index] = xr_+w_/2
            y_[index] = yr_+h_/2
            index+=1
            f.close()
        
        met_x = [
            [x[0],y[0],1],
            [x[1],y[1],1],
            [x[2],y[2],1]
        ]
        met_y=[
            [x_[0],y_[0]],
            [x_[1],y_[1]],
            [x_[2],y_[2]]
        ]
        #print 'frame :',frame,":\n"
        #print met_x,'\n',met_y
        try:
            m=np.linalg.solve(met_x,met_y)
        except: 
            continue
        else:
           # print m
            valid_test = 0
            total_test = len(rest_list)
            for j in rest_list:
                f=open(video_name + "_" +str(j), "r")
                raw = f.readlines()[frame -1:frame+1]
                curr_p = raw[0].split()
                real_p = raw[1].split()
                xc,yc,wc,hc = float(curr_p[1]),float(curr_p[2]),float(curr_p[3]),float(curr_p[4])
                xr,yr,w,h = float(real_p[1]),float(real_p[2]),float(real_p[3]),float(real_p[4])
                xr = xr + w/2
                yr = yr + h/2
                xc = xc + wc/2
                yc = yc + hc/2
                met_x = [
                    [xc,yc,1]
                ]
                predic_y = np.dot(met_x,m)
                #print predic_y
                #print xr,yr
                if get_tolerent(predic_y[0][0],predic_y[0][1],xr,yr) is True:
                    valid_test+=1
                #print get_tolerent(predic_y[0][0],predic_y[0][1],xr,yr)
                f.close()
            valid_rate =float(valid_test) /float(total_test)
            #print  valid_test, total_test, valid_rate
            if valid_rate > accept_rate:
                print 'frame:', frame,'\t',valid_rate
                f = open(video_name + "_result","a")
                f.write(str(frame)+"\t"+str(m)+"\n")
                f.close()
                break
            else:
                waiting_list = np.array(rest_list)
                if len(waiting_list) < 30:
                   max_distance+=iteration_torrent 
                   print 'change the torrent:', max_distance
                   waiting_list = np.arange(1, box_num+1)
           # print '---------------------------------\n'
    # raw_input()
