import math
import random
import matplotlib.pyplot as plt
import numpy as np
import time
from heapq import heappush, heappop # for priority queue




#####17.5.6
def check(the_map, nx, ny): #ex, ey :- end points of frame
    ex = len(the_map[0])
    ey = len(the_map)
    if nx > -1 and ny > -1 and nx < ex and ny < ey:
        return True
    else:
        return False


def square_sweep(the_map,x,y):
   summation = 0
   dy = [0,1]
   dx = [-2,-1,0,1,2]
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


def check_boundaries(the_map, nx, ny): 
    ex = len(the_map[0])
    ey = len(the_map)
    if nx > -1 and ny > -1 and nx < ex and ny < ey:
        return True
    else:
        return False

def check_obstacles(the_map, ansx, ansy):
    if the_map[int(ansy)][int(ansx)] > 0:
        return True
    else:
        return False

      

def nearestObstacleA(x, y,the_map):
    
    de_range = 9
    square_sum = 0
    a = 10

    for i in range(int(3*a/2) + 1):
        ansx = 0
        ansy = 0
        theta = i*math.pi/a

        for count in range(0,de_range):
            ansy = y + count*math.sin(theta+3*math.pi/4)
            ansx = x + count*math.cos(theta+3*math.pi/4)
            if check_boundaries(the_map, ansx, ansy) == False:
                break
            square_sum += the_map[int(ansy)][int(ansx)]#
            
    return square_sum


def nearestObstacle(x, y,the_map): 

    square_sum = 0
    de_range = 3

    
    for i in range(15):
        ansx = 0
        ansy = 0
        theta = i*math.pi/15

        for count in range(0,de_range):
            ansy = y + count*math.sin(theta)
            ansx = x + count*math.cos(theta)
            if check_boundaries(the_map, ansx, ansy) == False:
                break
            square_sum += the_map[int(ansy)][int(ansx)]
           
    if square_sum >0:
        return True
    else:
        return False
    
    #return 0

def nearestObstacle2(x, y, the_map,xStart,yStart):
    drange = 0
    if dist(x,y,xStart,yStart) > 7:
        drange = 7
    else:
        drange = int(dist(x,y,xStart,yStart))
    square_sum = 0
    for i in range(0,32):
        ansx = 0
        ansy = 0
        #count = 1
        theta = i*math.pi/16

        for count in range(0,drange):
            ansy = y + count*math.sin(theta)
            ansx = x + count*math.cos(theta)
            if check_boundaries(the_map, ansx, ansy) == False:
                break
            square_sum += the_map[int(ansy)][int(ansx)]

    return square_sum


def up_node_search(matrix,start,end,length):
    count = 1
    space = []
    for i in range(start,end+1):
        while(matrix[len(matrix)-count][i] ==0 and count < length + 1 and  nearestObstacle(i,len(matrix)-count,matrix)==False) :
              count += 1
        space.append([i,len(matrix)-count])
        count = 1
##    print "space:",space
    return space


        
def node_select(space):
      #39,
      (xo,yo) = (0,0)
      (xo1,yo1) = (0,0)
      (xo2,yo2) = (0,0)

        
      xo1 = space[0][0]
      yo1 = space[0][1]
      xo2 = space[len(space)-1][0]
      yo2 = space[len(space)-1][1]
      #print "x2,y2 : ",space[len(space)-1]
      #print "x12,y12 :",xo1,yo1,"and",xo2,yo2
      
      j = 0
      #while (j<int(len(space)) and space[j][0]<=39):
      while (j<int(len(space))):
          if yo1 >= space[j][1]:
              yo1 = space[j][1]
              xo1 = space[j][0]
          j += 1
      k = 0
      #while(k<int(len(space)) and space[len(space)-1-k][0]>=39):
      while(k<int(len(space))):
          if yo2 >= space[len(space)-1-k][1]:
              yo2 = space[len(space)-1-k][1]
              xo2 = space[len(space)-1-k][0]
          k += 1
      xo = int((xo1+xo2)/2)
      yo = int((yo1+yo2)/2)
      #print "xo1,yo1 : ",xo1,yo1
      #print "xo2,yo2 : ",xo2,yo2
      #print "xo,yo : ",xo,yo
      
      return (xo,yo)

def node_select_left(space):
    (xo,yo) = (0,0)
    (xo,yo) = space[len(space)-1]

    j = 0
    while(j<int(len(space))):
        if yo >= space[len(space)-1-j][1]:
            yo = space[len(space)-1-j][1]
            xo = space[len(space)-1-j][0]
        j += 1
    return (xo,yo)

def node_select_right(space):
    (xo,yo) = (0,0)
    (xo,yo) = space[0]

    j = 0
    while(j<int(len(space))):
        if yo >= space[j][1]:
            yo = space[j][1]
            xo = space[j][0]
        j += 1
    return (xo,yo)

def prime_obs(lidar,l_y_width):
    #1,2 order
    (lx,ly) = (0,0)
    left1 = 38 - 10
    left2 = 38

    (rx,ry) = (0,0)
    right1 = 40
    right2 = 40 + 10

    i = len(lidar)-1
    i1 = left2
    
    while(lidar[i][i1] == 0 and len(lidar)-1-i <= l_y_width):
        while(lidar[i][i1]==0 and i1 >= left1):
            i1 -= 1
        i -= 1
    if i1 == left1 and i == l_y_width:
        return (38-7,l_y_width)
    else:
        return (i1,i)


    j = len(lidar)-1
    j1 = right1
    while(lidar[j][j1]==0 and len(lidar)-1-j <= l_y_width):
        while(lidar[j][j1]==0 and j1 <= right2):
            j1 += 1
        j -= 1

    if j1 == right2 and j == l_y_width:
        return (40+7,l_y_width)
    else:
        return (j1,j)

def downer(matrix,x,y,xStart,yStart):

    count = 1
    if nearestObstacle2(x, y, matrix,xStart,yStart) > 0:
        while(nearestObstacle2(x,y+count,matrix,xStart,yStart)>0 and y<len(matrix)-1):
            count +=1
        return (x,y+count)
    else:
        return(x,y)
    

    


def dist(x0,y0,x2,y2):
   return math.sqrt((x2-x0)*(x2-x0) + (y2-y0)*(y2-y0))

def goal_selection(lidar,the_map,l_exist,r_exist,left_bottom,right_bottom,xStart,yStart):
   l_y_width = 35
   y_width = 35

   li_left_bottom = 0
   li_right_bottom = 0
   
   the_map = the_map.tolist()

   li_exist = False
   if not np.sum(lidar[:][l_y_width:]) == 0:
       li_exist = True
   lidar = lidar.tolist()

   
   sel_space = []
   li_space = []

   #downer(matrix,x,y)   
   if l_exist == True and r_exist == True :
      sel_space = up_node_search(the_map,left_bottom,right_bottom,y_width)
      return downer(the_map,node_select(sel_space)[0],node_select(sel_space)[1],xStart,yStart)
      #return downer(the_map,int((left_bottom+right_bottom)/2),50,xStart,yStart)


   ###### might be better solution########################################################################
   elif l_exist == True and r_exist == False:
      sel_space = up_node_search(matrix,left_bottom,left_bottom+10,y_width)
      return downer(the_map,node_select_left(sel_space)[0],node_select_left(sel_space)[1],xStart,yStart)
      #return downer(the_map,left_bottom,left_bottom + 14,xStart,yStart)

   elif l_exist == False and r_exist == True:
      sel_space = up_node_search(matrix,right_bottom-10,right_bottom,y_width)
      return downer(the_map,node_select_right(sel_space)[0],node_select_right(sel_space)[1],xStart,yStart)
      #return downer(the_map,right_bottom,right_bottom-14,xStart,yStart)
   #######################################################################################################
   else:
      if li_exist == True:
         (li_left_bottom,li_right_bottom) = prime_obs(lidar,l_y_width)
         li_space = up_node_search(lidar,li_left_bottom,li_right_bottom,l_y_width)
         return downer(lidar,node_select(li_space)[0],node_select(li_space)[1],xStart,yStart)

         """
         if dist(xo,yo,39,39) <= 10 or dist(xo,yo,39,39) >= 30 :
             top = 1
             while(lidar[39-top][39] == 1 or
                   nearestObstacle(39, 39-top,lidar)==True):
                top += 1
             return (39,39-top)
         else:
             return(xo,yo)
         """
      else:
          """
         if lidar[39][39] == 0 and nearestObstacle(39,39,lidar)==False:
            return (39,39)
         else :
            top = 1
            while(lidar[39-top][39] == 1 or
                  nearestObstacle(39, 39-top,lidar)==True):
               top += 1
            return (39,39-top)
        """
          return downer(lidar,39,39,xStart,yStart)

class node:

    xPos = 0
    yPos = 0
    distance = 0
    priority = 0 
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority

    def __lt__(self, other): 
        return self.priority < other.priority
    def updatePriority(self, matrix, xDest, yDest):
        #nearestObstacleA(x, y,the_map,x_goal,y_goal)
        self.priority = (nearestObstacleA(self.xPos, self.yPos, matrix)) + (self.distance) + (self.estimate(xDest, yDest) ) # A*, *20
        #self.priority = (self.distance) + (self.estimate(xDest, yDest) ) # A*, *20
    def nextdistance(self, i): 
        if i % 2 == 0:
            #self.distance += (10)*1.38/7
            self.distance += (10)/20
        else:
            #self.distance += (14)/7
            self.distance += 20*(14)/20

    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)/20
        #d = math.sqrt(xd * xd + yd * yd)/20
        return(d)


def pathFind(lidar,l_exist,r_exist,left_bottom,right_bottom,the_map, xStart, yStart):
    start1 = time.time()

    (xFinish,yFinish) = goal_selection(lidar,the_map,l_exist,r_exist,left_bottom,right_bottom,xStart,yStart)
##    print left_bottom,right_bottom
    the_map = the_map.tolist()
    the_map[39][39] = 0

    finalpath = []
    directions = 8
    if directions == 4:
       dx = [1, 0, -1, 0]
       dy = [0, 1, 0, -1]
    
    elif directions == 8:
       dx = [1, 1, 0, -1, -1, -1, 0, 1]
       dy = [0, 1, 1, 1, 0, -1, -1, -1]

    m = len(the_map)
    n = len(the_map[0])
    closed_nodes_map = []
    open_nodes_map = []
    dir_map = []
    row = [0] * n
    for i in range(m):
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] 
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xStart, yStart, 0, 0)
    n0.updatePriority(the_map, xFinish, yFinish)#nod0's priority is updated 0->what ever calculated
    heappush(pq[pqi], n0) #n0, the start node is pushed in to pq [[n0],[]]
    open_nodes_map[yStart][xStart] = n0.priority # mark it on the open nodes map, the priority calculation
    #single node exists, the start node
    # A* search
    while len(pq[pqi]) > 0:#while node is left
        end1 = time.time()
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node,[[this],[]], top node's braket's [0] = node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi])
        open_nodes_map[y][x] = 0 
        closed_nodes_map[y][x] = 1


        if (x == xFinish and y == yFinish) or (end1-start1)>0.2:

            while not (x == xStart and y == yStart):#start node is excluded, go path backwards and return string
                finalpath.insert(0,[x,y])
                j = dir_map[y][x]
                x += dx[j]
                y += dy[j]
            finalpath.insert(0,[xStart,yStart])
            return finalpath

        # generate moves (child nodes) in all possible directions
        for i in range(directions):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] > 0 or closed_nodes_map[ydy][xdx] == 1
                    or (dist(xFinish,yFinish,x,y)<dist(xFinish,yFinish,xdx,ydy))
                    or nearestObstacle2(xdx, ydy, the_map,xStart,yStart) > 0
                    or (i ==0 or i==4)
                    or (i ==1 or i==2 or i==3)
                    or not(xdx<53 and xdx>25)):
                # generate a child node
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextdistance(i)
                m0.updatePriority(the_map,xFinish, yFinish)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:#not tried yet nodes
                    open_nodes_map[ydy][xdx] = m0.priority#update with priority(every 8 directions on map)
                    heappush(pq[pqi], m0)#from empty -> now filled [[[filled],[]]
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + directions / 2) % directions
                elif open_nodes_map[ydy][xdx] > m0.priority:#node that was tried approached from diff direction
                    # update the priority info approached from diff direction
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction info
                    dir_map[ydy][xdx] = (i + directions / 2) % directions
                    #############################################################################
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])#[[this],[]] ->to [[],[here]]
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the wanted node
                    # empty the larger size pq to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
                    #############################################################################
    print "no path found","@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    return False # no route found
                
