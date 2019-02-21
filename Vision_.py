import cv2

import numpy as np

import time

import copy

import matplotlib.pyplot as plt

from sklearn import linear_model

from sklearn.linear_model import (LinearRegression,RANSACRegressor)

from sklearn.preprocessing import PolynomialFeatures

from sklearn.pipeline import make_pipeline





######################################°ª ÃÊ±âÈ­######################################

global direction,L_num,R_num,L_ransac,R_ransac,L_roi,R_roi,start_num, L_error, R_error

global frame_num, L_check, R_check, stop_Lines, destination_J, destination_I

global L_E,R_E,mid_ransac,lane_width

global edge_lx, edge_rx    # dotted line detection

global right_bottom,left_bottom


left_bottom = 24

right_bottom = 54



destination_J = 39

stop_Lines = 0

frame_num = 0

bird_height = 480

bird_width = 270

height = 270

width = 480

height_ROI = 270

L_num = 0

R_num = 0

L_ransac = 0

R_ransac = 0

L_check = 0

R_check = 0

L_roi = 0

R_roi = 0

L_error = 0

R_error = 0

num_y = bird_height - height_ROI

direction = 'straight'

num = 0

start_num = 0

L_E = 0

R_E = 0

mid_ransac = 135.

lane_width = 30



# set cross point

y1 = 185

y2 = 269



# º¯Çü Àü »ç°¢Á¡

L_x1 = 176#400

L_x2 =  92

R_x1 = 315#560

R_x2 = 447 

road_width = R_x2 - L_x2



# º¯Çü ÈÄ »ç°¢Á¡

Ax1 = 85+5#50

Ax2 = 230-5 #470

Ay1 = 0

Ay2 = 550



# Homograpy transform

pts1 = np.float32([[L_x1,y1],[R_x1,y1],[L_x2,y2],[R_x2,y2]])

pts2 = np.float32([[Ax1,Ay1],[Ax2,Ay1],[Ax1,Ay2],[Ax2,Ay2]])

M = cv2.getPerspectiveTransform(pts1,pts2)

i_M = cv2.getPerspectiveTransform(pts2,pts1)



real_Road_Width = 125

lransac_To = []

rransac_To = []

###################################Sub Functions####################################

def lane_Tomatrix(lransac,rransac):#Vision_Lane_Data_Parsing

    global destination, destination_J, destination_I, L_E, R_E, mid_ransac,lane_width

    global left_bottom, right_bottom

    list_Lane = np.zeros((80,80))

    lransac_To = []

    rransac_To = []

    destination_I = 50

    lanewidth_Half = lane_width/2

    check = 72

    left_r = 0

    right_r = 0



##    print L_E, R_E

    if(not (L_E or R_E)):#No error both

        list_Lane = np.zeros((80,80))

        for i in range(0, 210):

            try:

                lransac_To.append(int(((lransac[i])/270.)*80.))

                rransac_To.append(int(((rransac[i])/270.)*80.))

            except:

                pass

        

        for i in range(0,80):

            try:

                list_Lane[int((i/80.)*18. + 54.), int((lransac_To[i]/1.8) + 18)] = 10

                list_Lane[int((i/80.)*18. + 54.), int((rransac_To[i]/1.8) + 18)] = 10

            except : pass

        left_r = int((lransac_To[i]/1.8) + 18)

        right_r = int((rransac_To[i]/1.8) + 18)



        try:

            #mid_ransac = (lransac[0] + rransac[0])/2.

            lane_width = int((rransac[209] - lransac[209])*54./270.)

            

            ## print lane_width

            

            destination_J = int((lransac[0] + rransac[0])*54./540. + 12.)

        except: pass

        check_len = 80 - check

        

        try:

            left_bottom = left_r

            list_Lane[check:80,left_r] = np.ones((1,check_len))*10

            

        except:

            if left_r < 0:

                left_r = 0

                list_Lane[check:80,left_r] = np.ones((1,check_len))*10

                left_bottom = left_r

            else:

                pass

        try:

            print "right_Vision",right_r

            list_Lane[check:80,right_r] = np.ones((1,check_len))*10

            print "Fuck"

            right_bottom = right_r

        except:

            if right_r > 79:

                left_r = 79

                list_Lane[check:80,left_r] = np.ones((1,check_len))*10

                right_bottom = right_r

            else:

                pass

        







        

    elif(L_E and (not R_E)):#Error left // cant go only right region

        list_Lane = np.zeros((80,80))

        for i in range(0, 210):

            try:

##                lransac_To.append(int(((lransac[i]+lransac_Be[i])/540.)*80.))

                rransac_To.append(int(((rransac[i])/270.)*80.))

            except:

                pass

        

        for i in range(0,80):

            try:

##                list_Lane[int((i/80.)*18. + 54.), int((lransac_To[i]/62.)*30. + 40] = 10

                list_Lane[int((i/80.)*18. + 54.), int((rransac_To[i]/1.8) + 18)] = 10

            except : pass

##        left_r = lransac_To[61]

        right_r = int((rransac_To[i]/1.8) + 18)

        try:

            #mid_ransac = rransac[0] - 73.

            destination_J = int((rransac[0]/270.)*54. + 12.) - lanewidth_Half

        except: pass

        check_len = 80 - check

        try:

            list_Lane[check:80,right_r] = np.ones((1,check_len))*10

            right_bottom = right_r

        except:

            if right_r > 79:

                left_r = 79

                list_Lane[check:80,left_r] = np.ones((1,check_len))*10

                right_bottom = right_r

            else:

                pass

    elif(R_E and (not L_E)):

        list_Lane = np.zeros((80,80))

        for i in range(0, 210):

            try:

                lransac_To.append(int(((lransac[i])/270.)*80.))

##                rransac_To.append(int(((rransac[i]+rransac_Be[i])/540.)*80.))

            except:

                pass

        for i in range(0,80):

            try:

                list_Lane[int((i/80.)*18. + 54.), int((lransac_To[i]/1.8) + 18)] = 10

##                list_Lane[int((i/80.)*18. + 54.), int((rransac_To[i]/62.)*30. + 40] = 10

            except : pass

        left_r = int((lransac_To[i]/1.8) + 18)

##        right_r = rransac_To[61]

        try:

            #mid_ransac = lransac[0] + 73.

            destination_J = int((lransac[0]/270.)*54. + 12.) + lanewidth_Half

        except: pass

        check_len = 80 - check

        try:

            list_Lane[check:80,left_r] = np.ones((1,check_len))*10

            left_bottom = left_r

        except:

            if left_r < 0:

                left_r = 0

                list_Lane[check:80,left_r] = np.ones((1,check_len))*10

                left_bottom = left_r

            else:

                pass

    if destination_J < 0:

       destination_J = 0

    elif destination_J > 80:

       destination_J = 79

##    list_Lane[destination_I, destination_J] = 10


    return list_Lane, [destination_I, destination_J],[not L_E, not R_E, left_bottom, right_bottom]



# set ROI of gray scale

def set_Gray(img,region):

    mask = np.zeros_like(img)

    cv2.fillPoly(mask, region, (255,255,255))

    img_ROI=cv2.bitwise_and(img, mask)

    return img_ROI



# set ROI of red scale

def set_Red(img,region):

    mask = np.zeros_like(img)

    cv2.fillPoly(mask, region, (0,0,255))

    img_red=cv2.bitwise_and(img,mask)



    return img_red



# ransac

def linear_Ransac(x_points,y_points,y_min,y_max):

    x_points = np.array(x_points)

    y_points = np.array(y_points)

    

    y_points = y_points.reshape(len(y_points),1)

    model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())



    try :

        model_ransac.fit(y_points, x_points)

    except ValueError : pass

    else :

        line_Y = np.arange(y_min, y_max)

        line_X_ransac = model_ransac.predict(line_Y[:, np.newaxis])

    

        return line_X_ransac

# ransac

def polynomial_Ransac(x_points,y_points,y_min,y_max):

    x_points = np.array(x_points)

    y_points = np.array(y_points)

    y_points = y_points.reshape(len(y_points),1)

    model_Sransac = make_pipeline(PolynomialFeatures(2),RANSACRegressor(random_state=42))

    try :

        model_Sransac.fit(y_points, x_points)

    except ValueError : pass

    else :

        line_Y = np.arange(y_min, y_max)

        line_X_ransac = model_Sransac.predict(line_Y[:, np.newaxis])

        return line_X_ransac



# draw polynomial

def draw_Poly(img, points, color):

    for i in range(num_y-60):

        try :

            cv2.circle(img,(int(points[i]),height_ROI+i),1,color,2)

        except TypeError : pass

# black bye

def black_Bye(img,th_red):

    thresholds = (img[:,:,2] < th_red)

    img[thresholds] = [0,0,0]

    return img

# black bye

def con_Bye(img,th_green):

    thresholds = (img[:,:,1] < th_green)

    img[thresholds] = [0,0,0]

    return img



# image processing

def image_Processing(img, pts1, pts2):

    # red ROI

    temp = np.zeros((bird_height, bird_width, 3), dtype=np.uint8)

    rect = np.array([[(0,200),(0,bird_height),

                      (bird_width,bird_height),(bird_width,200)]])

    img_con_Bye = con_Bye(img, 50)

    img_red = set_Red(img,rect)

    #cv2.imshow('red',img_red)

    img_black_Bye = black_Bye(img_red, 165+50)

   

    cv2.imshow('blackBye',img_black_Bye)



    # closing or opening + canny

    kernel = np.ones((2,2), np.uint8)

    img_dilation = cv2.dilate(img_black_Bye, kernel, iterations=1)

    img_erosion = cv2.erode(img_dilation, kernel, iterations=2)

    img_canny = cv2.Canny(img_erosion,20,80)

    cv2.imshow('canny',img_canny)



    return img_canny



# choose roi

def choose_Roi(dst, direction, L_num, R_num, L_ransac, R_ransac, L_roi_before, R_roi_before):

    # left line roi

    try :

        if L_num != 0:

            if direction == 'left' or direction == 'right' :

                L_roi = np.array([[(int(L_ransac[0])-25,height_ROI),(int(L_ransac[0])+25,height_ROI),

                                       (int(L_ransac[num_y/3])+25,height_ROI+num_y/3),(80,bird_height-60),

                                       (20,bird_height-60),(int(L_ransac[num_y/3])-25,height_ROI+num_y/3)]])

            else :

                L_roi = np.array([[(int(L_ransac[0])-25,height_ROI),(int(L_ransac[0])+25,height_ROI),

                                       (int(L_ransac[num_y/3])+25,height_ROI+num_y/3),(int(L_ransac[num_y-50])+25,bird_height-60),

                                       (int(L_ransac[num_y-50])-25,bird_height-60),(int(L_ransac[num_y/3])-25,height_ROI+num_y/3)]])

        elif direction == 'straight':

            L_roi = np.array([[(0,260),(bird_width/2-40,260),(bird_width/2-40,height_ROI+num_y/2),

                               (bird_width/2-40,bird_height-65),(15,bird_height-65)]])

        elif direction == 'right':

            L_roi = L_roi_before

        elif direction == 'left':

            L_roi = L_roi_before

        else : L_roi = L_roi_before

        

    except TypeError :

        L_roi = np.array([[(0,260),(bird_width/2-40,260),(bird_width/2-40,height_ROI+num_y/2),

                               (bird_width/2-40,bird_height-65),(15,bird_height-65)]])

        

    # right line roi

    try :

        if R_num != 0:

            if direction == 'left' or direction == 'right' :

                R_roi = np.array([[(250,bird_height-60),(190,bird_height-60),

                                   (int(R_ransac[num_y/3])-25,height_ROI+num_y/3),(int(R_ransac[0])-25,height_ROI),

                                   (int(R_ransac[0])+25,height_ROI),(int(R_ransac[num_y/3])+25,height_ROI+num_y/3)]])

            else :

                R_roi = np.array([[(int(R_ransac[num_y-100])+25,bird_height-60),(int(R_ransac[num_y-50])-25,bird_height-60),

                                   (int(R_ransac[num_y/3])-25,height_ROI+num_y/3),(int(R_ransac[0])-25,height_ROI),

                                   (int(R_ransac[0])+25,height_ROI),(int(R_ransac[num_y/3])+25,height_ROI+num_y/3)]])

   

        elif direction == 'straight':

            R_roi = np.array([[(bird_width-15,bird_height-65),(bird_width/2+40,bird_height-65),

                                (bird_width/2+40,height_ROI+num_y/2),(bird_width/2+40,280),(bird_width,280)]])



        elif direction == 'right':

            R_roi = R_roi_before



        elif direction == 'left':

            R_roi = R_roi_before

        else : R_roi = R_roi_before

    except TypeError :

        R_roi = np.array([[(bird_width-15,bird_height-65),(bird_width/2+40,bird_height-65),

                                (bird_width/2+40,height_ROI+num_y/2),(bird_width/2+40,280),(bird_width,280)]])

    return L_roi, R_roi



# decide left, right edge points

def extract_Line(dst, img_canny, L_line, R_line):

    global edge_lx, edge_rx    

    # draw line roi

    cv2.polylines(dst,L_line,1,(0,255,0),5)

    cv2.polylines(dst,R_line,1,(0,255,0),5)



    # canny edge

    L_edge = set_Gray(img_canny,L_line)

    R_edge = set_Gray(img_canny,R_line)

    

    # separate edge points

    edge_lx,edge_ly = np.where(L_edge >= 255)

    edge_rx,edge_ry = np.where(R_edge >= 255)



    '''# dotted line

    if len(edge_lx) <150 :

        print "left dotted line"

        print len(edge_lx)

    if len(edge_rx) <150 :

        print "right dotted line"

        print len(edge_rx)'''       

        

    for i in range(len(edge_lx)):

        try:

            cv2.circle(dst,(int(edge_ly[i]),int(edge_lx[i])),1,(0,155,255),2)

        except TypeError :

            pass

    for i in range(len(edge_rx)):

        try:

            cv2.circle(dst,(int(edge_ry[i]),int(edge_rx[i])),1,(255,155,0),2)

        except TypeError :

            pass

    return dst, edge_lx, edge_ly, edge_rx, edge_ry



# check error

def check_Error(L_ransac, R_ransac, L_check, R_check, L_num, R_num, direction, road_Width):

    global mid_ransac

    '''# 1. Æ¢ŽÂ data

    try :

        if abs(L_check[num_y-1]-L_ransac[num_y-1]) > 30 or abs(L_check[0]-L_ransac[0]) > 30 or abs(L_check[num_y/2]-L_ransac[num_y/2]) > 30 :

            L_ransac = copy.deepcopy(L_check)

            L_num = -1

    except TypeError : 

            L_num = -1

    try :

        if abs(R_check[num_y-1]-R_ransac[num_y-1]) > 30 or abs(R_check[0]-R_ransac[0]) > 30 or abs(R_check[num_y/2]-R_ransac[num_y/2]) > 30 :

            R_ransac = copy.deepcopy(R_check)

            R_num = -1

    except TypeError :

            R_num = -1

            

    # 2. ÁÂÈžÀü ¿ìÈžÀü Æ¢ŽÂ data

    try :

        if direction == 'left':

            if L_ransac[0] <= L_ransac[num_y/2] : pass

            else :

                L_ransac = copy.deepcopy(L_check)

                L_num = -1

            if R_ransac[0] <= R_ransac[num_y/2] : pass

            else :

                R_ransac = copy.deepcopy(R_check)

                R_num = -1

        elif direction == 'right':

            if L_ransac[0] >= L_ransac[num_y/2] : pass

            else :

                L_ransac = copy.deepcopy(L_check)

                L_num = -1

            if R_ransac[0] >= R_ransac[num_y/2] : pass

            else :

                R_ransac = copy.deepcopy(R_check)

                R_num = -1

        else : pass

    except TypeError :

            L_num = -1

            R_num = -1

        

    # 3. Â÷Œ±º¯°æ

    try :

        if R_ransac[num_y-50] > bird_width-10 and L_ransac[num_y-50] > bird_width/2-30 :

            L_num = -1

            R_num = -1

            #print '¿ÞÂÊÀž·Î Â÷Œ±º¯°æ'

    except TypeError : L_num = -1



    try :

        if L_ransac[num_y-50] < 10 and R_ransac[num_y-50] < bird_width/2-30:

            L_num = -1

            R_num = -1

            #print '¿Àž¥ÂÊÀž·Î Â÷Œ±º¯°æ'

    except TypeError : R_num = -1'''



    # 4. Left Lane have to primary than Right Lane

    try :

        if L_ransac[0] > mid_ransac + 20 or L_ransac[209] > mid_ransac + 20:

            print "ERROR 4"

            L_ransac = copy.deepcopy(L_check)

            L_num = -1

            

    except TypeError :

        L_num = -1

        

    try:

        if R_ransac[0] < mid_ransac -20 or R_ransac[209] < mid_ransac -20:

            print "ERROR 4"

            R_ransac = copy.deepcopy(R_check)

            R_num = -1

    except TypeError:

        R_num = -1

        

    # 5. Â÷Œ±Æø

    try :

        if abs(mid_ransac - L_ransac[0]) > 120  :

            print "ERROR 5"

            L_ransac = copy.deepcopy(L_check)

            L_num = -1

    except TypeError :

        L_num = -1

    try :

        if abs(mid_ransac - R_ransac[0]) > 120  :

            print "ERROR 5"

            R_ransac = copy.deepcopy(R_check)

            R_num = -1

    except TypeError :

        R_num = -1

  



    return L_ransac, R_ransac, L_num, R_num



# reset error 3 frame

def error_3frames(L_num, R_num, L_error, R_error, start_num):

    global L_E, R_E

    L_E = 0

    R_E = 0

    if L_num == -1 :

        L_E = 1

        if L_error == 0 or L_error == 1 or L_error == 2:

            L_error += 1

        else :

            L_error = 0

            start_num = -1  # roi 

    else : L_error = 0

    

    if R_num == -1 :

        R_E = 1

        if R_error == 0 or R_error == 1 or R_error == 2:

            R_error += 1

        else :

            R_error = 0

            start_num = -1

    else : R_error = 0

    return L_error, R_error, start_num



# check road width

def check_Road_Width(L_ransac, R_ransac):

    road_Width = [0,0,0]

    try :

        road_Width[0] = R_ransac[0] - L_ransac[0]

        road_Width[1] = R_ransac[num_y/3] - L_ransac[num_y/3]

        road_Width[2] = R_ransac[num_y-1] - L_ransac[num_y-1]

    except TypeError : return 0

    return max(road_Width)



# check direction

def check_Direction(L_ransac, R_ransac, direction_before):

    try :

        L_dif = L_ransac[0]-L_ransac[num_y/3]

        R_dif = R_ransac[0]-R_ransac[num_y/3]

    except TypeError : direction = 'straight'

    else :

        if direction_before == 'right':

            if L_dif < 30 and R_dif < 30:

                #print 'str'

                direction = 'str'

            else :

                direction = 'right'

                #print 'right'

        elif direction_before == 'left':

            if L_dif > -30 and R_dif > -30: 

                #print 'str'

                direction = 'str'

            else :

                direction = 'left'

                #print 'left'

        else:

            if L_dif > 45 and R_dif > 15 :

                #print 'right'

                direction = 'right'

            elif R_dif < -45 and L_dif < -15:

                #print 'left'

                direction = 'left'

            else :

                direction = 'straight'

                #print 'str'

    return direction



# draw straight line

def draw_Straight_Line(dst, L_points, R_points, L_check, R_check, L_num, R_num, L_color, R_color, start_num):

    if start_num == -1 : pass

    else :

        if L_num == -1: pass

            #draw_Poly(dst, L_check, L_color)

        else:

            draw_Poly(dst, L_points, L_color)

        if R_num == -1: pass

            #draw_Poly(dst, R_check, R_color)

        else:

            draw_Poly(dst, R_points, R_color)

        return dst



# draw poly line

def draw_Poly_Line(dst, L_points, R_points, L_check, R_check, L_num, R_num, L_color, R_color, start_num):

    if start_num == -1 : pass

    else :

        if L_num == -1:

            draw_Poly(dst, L_check, L_color)

        else:

            draw_Poly(dst, L_points, L_color)

        if R_num == -1:

            draw_Poly(dst, R_check, R_color)

        else:

            draw_Poly(dst, R_points, R_color)

        return dst

    

# get fit line

def get_Fit_Line(f_lines):

    try :

        if len(f_lines) == 0 :

            return None

        elif len(f_lines) == 1 :

            lines = lines.reshape(2,2)

        else :

            lines = np.squeeze(f_lines)

            lines = lines.reshape(lines.shape[0]*2,2)

    except :

        return None

    else :

        [vx,vy,x,y] = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01)

        x1 = 960-1 #width of cam(image)

        y1 = int(((960-x)*vy/vx)+y)

        x2 = 0

        y2 = int((-x*vy/vx)+y)

        result = [x1,y1,x2,y2]

        return result



# detect stop line

def detect_Stop(dst, dst_canny, L_roi, R_roi):

    stop_Roi = np.array([[(45,440),(205,440),(205,5),(45,5)]])

    #cv2.polylines(dst, stop_Roi, 1, (0,155,0),5)

    img_Stop = set_Gray(dst_canny, stop_Roi)

    line_arr = cv2.HoughLinesP(img_Stop, 1, 1 *  np.pi/180, 30, np.array([]), 10, 30)

    line_arr = np.array(np.squeeze(line_arr))

    line_arr_t = line_arr.transpose()

    if line_arr.shape != () :

        slope_Degree = ((np.arctan2(line_arr_t[1] - line_arr_t[3], line_arr_t[0] - line_arr_t[2]) * 180) / np.pi)

        try :

            line_arr = line_arr[np.abs(slope_Degree)>165]

            line_arr = line_arr[:,None]

        except IndexError : pass

        else :

            stop_Lines = get_Fit_Line(line_arr)

            try :

                cv2.line(dst, (stop_Lines[0],stop_Lines[1]), (stop_Lines[2],stop_Lines[3]),(0,155,0),5)

            except TypeError : pass

            return dst, stop_Lines

                

#####################################Main Function###################################



# read video



def lane_Detection(img):

    global direction,L_num,R_num,L_ransac,R_ransac,L_roi,R_roi,start_num, L_error, R_error

    global frame_num, L_check, R_check,stop_Lines, destination_J, destination_I

    global mid_ransac

    

    #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dst = cv2.warpPerspective(img ,M,(height,width))



    img_canny = image_Processing(dst, pts1, pts2)

   

    L_roi, R_roi = choose_Roi(dst, direction, L_num, R_num, L_ransac, R_ransac, L_roi, R_roi)

    

    dst, edge_lx, edge_ly, edge_rx, edge_ry = extract_Line(dst, img_canny, L_roi, R_roi)

    

    L_ransac = polynomial_Ransac(edge_ly, edge_lx, height_ROI,bird_height)

    R_ransac = polynomial_Ransac(edge_ry, edge_rx, height_ROI,bird_height)

    '''try:

        print "Left! ",L_ransac[0],mid_ransac

    except: pass

    try:

        print "Right! ",R_ransac[0],mid_ransac

    except: pass'''

    L_linear = linear_Ransac(edge_ly, edge_lx, height_ROI,bird_height)

    R_linear = linear_Ransac(edge_ry, edge_rx, height_ROI,bird_height)

    road_Width = check_Road_Width(L_ransac, R_ransac)

  

    if start_num == 0 :

        L_check = copy.deepcopy(L_ransac)

        R_check = copy.deepcopy(R_ransac)

    

    direction = check_Direction(L_ransac, R_ransac, direction)

    if direction == 'straight' :

        L_linear, R_linear, L_num, R_num = check_Error(L_linear, R_linear, L_check, R_check, L_num, R_num, direction, road_Width)

        L_error, R_error, start_num = error_3frames(L_num, R_num, L_error, R_error, start_num)

        draw_Straight_Line(dst, L_linear, R_linear, L_check, R_check, L_num, R_num, (0,0,255), (255,0,0), start_num)

        

        L_check = copy.deepcopy(L_linear)

        R_check = copy.deepcopy(R_linear)

        try :

            dst, stop_Lines = detect_Stop(dst, img_canny, L_roi, R_roi)

        except TypeError : pass

    else :

        L_ransac, R_ransac, L_num, R_num = check_Error(L_ransac, R_ransac, L_check, R_check, L_num, R_num, direction, real_Road_Width)

        L_error, R_error, start_num = error_3frames(L_num, R_num, L_error, R_error, start_num)



        L_check = copy.deepcopy(L_ransac)

        R_check = copy.deepcopy(R_ransac)

    cv2.imshow('dst',dst)

    i_dst = cv2.warpPerspective(dst,i_M,(bird_height,bird_width))



    start_num += 1

    frame_num += 1

    L_num += 1

    R_num += 1

  

    matrix_Lane = lane_Tomatrix(L_check,R_check)

    return matrix_Lane, stop_Lines



def dotted_Detection():

    return [len(edge_lx), len(edge_rx)]



##cam = cv2.VideoCapture(0)

##cam.set(3,480)

##cam.set(4,270)

##width = 480

##height = 270

##

##if (not cam.isOpened()):

##    print ("cam open failed")

##

##while True:

##    s, img = cam.read()

##    lane_Matrix, s_Lines = lane_Detection(img)

##    #print s_Lines

##    dim = (500, 500)

##    resized = cv2.resize(lane_Matrix[0], dim, interpolation =  cv2.INTER_AREA)

##    print lane_Matrix[0][54]

##    cv2.imshow('ee',resized)

##   

##    cv2.imshow('cam',img)

##    if cv2.waitKey(1) & 0xFF == ord('q'):

##        break

##    

##cam.release()

##cv2.destroyAllWindows()

##cv2.waitKey(0)

