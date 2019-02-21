import math
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from heapq import heappush, heappop # for priority queue

def check(the_map, nx, ny): #ex, ey :- end points of frame
    ex = len(the_map[0])
    ey = len(the_map)
    if nx > -1 and ny > -1 and nx < ex and ny < ey:
        return True
    else:
        return False

def square_sweep(the_map,x,y):
   #the_map as 2d list
   summation = 0
   dy = [0,1]
   dx = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
   for i in range(0,len(dy)):
      for j in range(0,len(dx)):
          if check(the_map,x+dx[j],y+dy[i]) == True:
              summation += the_map[y+dy[i]][x+dx[j]]
          else:
              summation += 0
         
   if summation >0:
      return False
   else:
      return True
   
   

def goal_selection(lidar,the_map,l_exist,r_exist,left_bottom,right_bottom):
   #l_lane : left lane position
   #r_lane : right lane position
   #the_map : matirx with lane detection and obstacle
   #matrix = matrix.tolist()
   the_map = the_map.tolist()
   l_y_width = 30
   
   li_exist = False
   if not np.sum(lidar[:][l_y_width:]) == 0:
       li_exist = True
   
   lidar = lidar.tolist()

   
   sel_space = [] #candidates for possible objective points
   li_space = [] #candidates for objective points

   xo = 0
   yo = 0
   xo1 = 0
   yo1 = len(the_map)-1
   xo2 = 0
   yo2 = len(the_map)-1

   li_left_bottom = int(len(lidar[0])/4)
   li_right_bottom = int(len(lidar[0])*3/4)

   
   y_width = 30
   half = 0
   """
   l_pose = 0
   r_pose = 0
   l_exist = False
   r_exist = False
   """
   count = 1
   count1 = 1




    

   """
   for t in range(0,int(len(matrix[0])/2)):
      if matrix[len(matrix)-1][t] == 1:
         l_pose = t
         l_exist = True
      elif matrix[len(matrix)-1][len(matrix[0])-1-t] == 1:
         r_pose = len(matrix[0])-1-t
         r_exist = True
   left_bottom = l_pose#left most bottom position of left lane, (l,79)point
   right_bottom = r_pose#right most bottom position of right lane,(r,79)point
   #print "l and right:",left_bottom,right_bottom
   """
   
   if l_exist == True and r_exist == True :
      #r,l Lane both exists and non crossing over lanes(no errors)
      #print l_pose,r_pose   
      for i in range(left_bottom,right_bottom+1):

         while(the_map[len(the_map)-count][i] == 0 and count < y_width+1
               and square_sweep(the_map,i,len(the_map)-count)==True):
            #print "x,y for matrix : ",i,len(matrix)-count
            #print "matrix value:",matrix[len(matrix)-count][i]
            count += 1

         sel_space.insert(0,[i,len(the_map[0])-count])
         count = 1
      #print "sel_sapce, len:",sel_space,len(sel_space)

      for j in range(0,len(sel_space)):
         #xo1 = sel_space[0][0]
         #yo1 = sel_space[0][1]
         if yo1 >= sel_space[j][1]:
            yo1 = sel_space[j][1]
            xo1 = sel_space[j][0]
      #print "xo1,yo1,sel_space[j]:",xo1,yo1,sel_space[j]
      #print "xo1,yo1:",xo1,yo1
      for j in range(0,len(sel_space)):
         #print j
         #xo2 = sel_space[0][0]
         #yo2 = sel_space[0][1]
         if yo2 >= sel_space[len(sel_space)-1-j][1]:
            yo2 = sel_space[len(sel_space)-1-j][1]
            xo2 = sel_space[len(sel_space)-1-j][0]
      #print "xo2,yo2:",xo2,yo2
      #xo = int(3*(xo1 + xo2)/5 + 2*(left_bottom+right_bottom)/5)
      xo = int((xo1 + xo2)/2)
      #xo = int((xo1 + xo2)/2 + 0.25*(left_bottom + right_bottom)/4)
      yo = int((yo1 + yo2)/2)
      return(xo,yo)

   ###### might be better solution
   elif l_exist == True and r_exist == False:
      #y_width
      half = int(len(the_map[0])/2) - left_bottom
      if not the_map[half + left_bottom][len(the_map)-1-y_width] ==1:
         return (half + left_bottom + 2,len(the_map)-1-y_width)
      else:
         line = 0
         while(the_map[half + left_bottom][len(the_map)-1-y_width+line] == 1):
            line += 1
         return (half + left_bottom + 2,len(the_map)-1-y_width+line+1)
   
   elif l_exist == False and r_exist == True:
      #y_width
      half = right_bottom - int(len(the_map[0])/2)
      if not the_map[half + right_bottom][len(the_map)-1-y_width] ==1:
         return (half + right_bottom - 2,len(the_map)-1-y_width)
      else:
         line = 0
         while(the_map[half + right_bottom][len(the_map)-1-y_width+line] == 1):
            line += 1
         return (half + right_bottom - 2,len(the_map)-1-y_width+line+1)
   #######################################################################################################
   else:
      if li_exist == True:
         for yy in range(0,l_y_width):
            for k in range(0,int(len(lidar[0])/2)):
               if lidar[len(lidar)-1-yy][int(len(lidar[0])/2) - 2 - k] > 0:
                  li_left_bottom = len(lidar[0])/2 - 2 - k
                  break
            break
         for yy in range(0,l_y_width):
            for k in range(int(len(lidar[0])/2),len(lidar[0])):
               if lidar[len(lidar)-1-yy][k] > 0:
                  li_right_bottom = k
                  break
            break
         for i in range(li_left_bottom,li_right_bottom + 1):
            while(lidar[len(lidar)-count1][i] == 0 and count1 < l_y_width+1
                  and square_sweep(lidar,i,len(lidar)-count1)==True):
            #print "x,y for matrix : ",i,len(matrix)-count
            #print "matrix value:",matrix[len(matrix)-count][i]
               count1 += 1

            li_space.insert(0,[i,len(lidar[0])-count1])
            count1 = 1
      #print "sel_sapce, len:",sel_space,len(sel_space)

         for j in range(0,len(li_space)):
         #xo1 = sel_space[0][0]
         #yo1 = sel_space[0][1]
            if yo1 >= li_space[j][1]:
               yo1 = li_space[j][1]
               xo1 = li_space[j][0]
      #print "xo1,yo1,sel_space[j]:",xo1,yo1,sel_space[j]
      #print "xo1,yo1:",xo1,yo1
         for j in range(0,len(li_space)):
         #print j
         #xo2 = sel_space[0][0]
         #yo2 = sel_space[0][1]
            if yo2 >= li_space[len(li_space)-1-j][1]:
               yo2 = li_space[len(li_space)-1-j][1]
               xo2 = li_space[len(li_space)-1-j][0]
      #print "xo2,yo2:",xo2,yo2
      #xo = int(3*(xo1 + xo2)/5 + 2*(left_bottom+right_bottom)/5)
         xo = int((xo1 + xo2)/2)
      #xo = int((xo1 + xo2)/2 + 0.25*(left_bottom + right_bottom)/4)
         yo = int((yo1 + yo2)/2)
         return(xo,yo)      
      else:
         return (39,39) #I & J value
    
    #return (int(len(the_map[0])/2),int(len(the_map))-1)
