import cv2
import time
import math
import numpy as np
import matplotlib.pyplot as plt

global destination, lanewidth_Half, lane_Error, destination_I,list_Lane
global t1, start_time, gear, find, point, speed_Obs
global start_time, U_straight_time, J_straight_time, J_straight_time_2
global just_once, just_once_2, t1, t2,t3,a, steer_2,steer_x_length,  point,b,past
gear = 0
steer = 0
past = []
steer_angle = []
just_once = 0
just_once_2 =0
U_alpha = 3.4
U_beta = 1.7
J_alpha = 0
J_beta = 0
start_time = 0
U_straight_time = 1
J_straight_time = 1
J_straight_time_2 = 1
speed_Obs = 0
speed_Default = 30
look_ahead = 4
steer_x_length = []
steer_y_length = []
think_x = 0
think_y = 0
find = 0
point = 0
t1 = 0
t2 = 0
t3 = 0
a = 1
b = 0
steer_2 = 0
################Function#######################
def steering(Mission, Obstacle, dotted_Line,points_Path, steer_measured_Comb):#, speed_Default, speed_Obs):

    global steer, gear, speed_Obs, speed_Default,start_time, U_straight_time, J_straight_time, J_straight_time_2
    global just_once, just_once_2, t1, t2,t3,a, steer_2, steer_x_length, point, b, past
    check = Mission * Obstacle
            
################### U-TURN ##################################
    if check == 5:
        wSPEED = 35
        curve_time = 18.22/ (wSPEED * 100 /(360*5.8)) +U_alpha ######## wSTEER = -1970
        curve_time_2 = (9.11/( wSPEED * 100 /(360*5.8)))+U_beta ######## wSTEER = 1970
        if dotted_Line < 180:     # left dotted line
            t2 = t1     
            t1 = time.time()
            t3 = t1 - t2
            if just_once == 0:
                start_time = t1
                just_once = 1
        if time.time() - start_time -t3 > U_straight_time: ###########straight
            steer = -1970
        if time.time() - start_time - U_straight_time - t3> curve_time:#############first curve
            steer = 1970  
        if time.time() - curve_time - start_time -U_straight_time -t3 > curve_time_2:###########second curve
            steer = 0
            check = 10
        return steer, speed_Obs#, gear


################## S-CURVE ################################        
    elif check == 0:
##        print "Path",points_Path
        ## S curve = 4, Narrow = 2
        if check == 4 :
            look_ahead = 1
        look_ahead = 8  ########### 'look_ahead' is distance of what you see.
        if look_ahead > len(points_Path):
            look_ahead = len(points_Path)/2 
        for i in range(0,len(points_Path) -look_ahead ):
            x_length = (points_Path[i+look_ahead][0] - points_Path[i][0])*(0.1/1.41)
            y_length = (points_Path[i+look_ahead][1] - points_Path[i][1])*(0.1/1.41)
            abs(y_length)
            if x_length == 0. :
##                print "1111111111111111111111111"
                tan_value = 0
            else:
                tan_value = 1.04/(abs(pow(x_length,2) + pow(y_length,2) - 1.04)/(2*x_length))
##            print pow(x_length, 2), pow(y_length,2), x_length
            theta = math.degrees(math.atan(tan_value))
            steer_angle_now = steer_measured_Comb/71
            steer_angle.append( theta)
            #steer_angle[i] = steer_angle_now + theta
        steer = (steer_angle[0])*71
##        print 'sA', steer_angle
##        print "iner steer" ,steer
        return steer, speed_Obs#, gear


################  JU - CHA ##################################

    elif check == 7:
        wSPEED = 35
        jucha_time = (9.11/ (wSPEED * 100 /(360*5.8))) +J_alpha ######## in
        jucha_time_2 = (9.11/( wSPEED * 100 /(360*5.8))) +J_beta ######## back(out)
        if VLD.dotted_Detection()[0] < 180:     # left dotted line
            t1 = time.time()
            if just_once_2 == 0:
                start_time = t1
                just_once_2 = 1
        if time.time() - start_time > J_straight_time: ###########straight
            steer = 1970
        if time.time() - start_time - J_straight_time > jucha_time:#############in
            steer = 0 
        if time.time()  - start_time - J_straight_time - jucha_time > (J_straight_time+10):###########in straight
            steer = 0
            gear = 2
        if time.time()  - start_time - J_straight_time - jucha_time - J_straight_time - 10 > J_straight_time:###########back straight
            steer = 1970
            gear = 2
        if time.time()  - start_time - J_straight_time - jucha_time - J_straight_time - 10 - J_straight_time > jucha_time_2:###########back 
            steer = 0
            gear = 0
            check = 10

        return steer, speed_Obs#, gear


################ default #######################################    


    else:
        if a ==1 :
            if past == points_Path:
                speed_Default = 23
            else:
                speed_Default = 30
            past = points_Path
            """ti1 = time.time()
            ti3 = ti2 - ti1
            ti2 = time.time()"""
            steer = []
            steer_x_length = []
            steer_y_length = []
            point = 0
            think_x = 0
            think_y = 0
            find = []
            next_steer = 0
            look_ahead = 1  ########### 'look_ahead' is tistance of what you see.
            
            if len(points_Path) <= 10:
                speed_Default = 23
            if len(points_Path) <= 3:
                return steer, speed_Default
            for i in range(0,len(points_Path) -look_ahead):
                x_length = (points_Path[i+look_ahead][0] - points_Path[i][0])*(0.1/1.41)
                y_length = (points_Path[i+look_ahead][1] - points_Path[i][1])*(0.1/1.41)
                abs(y_length)
                steer_x_length.append(x_length)
                steer_y_length.append(y_length)
            for j in range(0,len(points_Path)-3):
                find.append(steer_x_length[j+look_ahead] * steer_x_length[j])
                if steer_x_length[j+1] == 0:
                    if steer_x_length[j] == 0:
                        find[j] = 1
                if find[j] <= 0 :
##                    if j <= 10:
                    point = j + 1
##                    if j > 10:
##                        point = j +1
                    if point >= (len(points_Path) -6):
                        point = len(points_Path) -10
            if point > 0:
                for k in range(0, point):
                    think_x = think_x + steer_x_length[k]                 
                    think_y = think_y + steer_y_length[k]
                if think_x == 0:
                    tan_value = 0
                    b = 1
                else:
                    tan_value = 1.04/(abs(pow(think_x,2) + pow(think_y,2) - 1.04)/(2*think_x))    
            else:
                print steer_x_length
                if steer_x_length[0] == 0:
                    tan_value = 0
                    b = 1
                else:
                    for k in range(0, len(points_Path) - 2):
                        think_x = think_x + steer_x_length[k]                 
                        think_y = think_y + steer_y_length[k]
                    tan_value = 1.04/(abs(pow(think_x,2) + pow(think_y,2) - 1.04)/(2*think_x))
            theta = math.degrees(math.atan(tan_value))
            if j <=10:
                theta = theta*(2.61)
                speed_Default = 23
            else:
                theta = theta
                speed_Default = 30
            steer_angle_now = steer_measured_Comb/71
            steer = ( theta)*71
##        if a == 0:
##            steer = steer_2
##            a = 1
##        if steer_x_length[point+1] == 0:
##            if b == 0:
##                steer_2 = -steer
##                a = 0
##        b = 0
        print "iner steer", steer
                
        return steer, speed_Default#, gear
            

##########################################################


'''while True:
    try:
        steer(points_Path, steer_measured_Comb )
    except Exception as e:
        print "d",e'''
