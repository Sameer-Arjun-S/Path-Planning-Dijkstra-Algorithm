#Importing all the libraries
import cv2
import numpy as np
import time 
import heapq
#!pip install pygame
import pygame

#Defining canvas and gamescape
#Initiated here to just visualize the gamespace
pygame.init()
space = pygame.display.set_mode([600,250])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    space.fill((255,255,255))
    pygame.draw.rect(space, (180,0,0), pygame.Rect(0,0,600,250),5)
    pygame.draw.rect(space, (0,250,0), pygame.Rect(100,0,50,100))
    pygame.draw.rect(space, (0,250,0), pygame.Rect(100,150,50,100))
    pygame.draw.rect(space, (180,0,0), pygame.Rect(95,0,60,105),5)
    pygame.draw.rect(space, (180,0,0), pygame.Rect(95,145,60,105),5)
    pygame.draw.polygon(space, (180,0,0),((235,87.5),(300,50),(364.95,87.5),(364.95,162.5),(300,200),(235,162.5)))
    pygame.draw.polygon(space, (0,250,0),((230.04,84.61),(300,44.22),(369.95,84.61),(369.95,165.38),(300,205.77),(230.04,165.38)),5)
    pygame.draw.polygon(space, (0,250,0),((460,25),(510,125),(460,225)))
    pygame.draw.polygon(space, (180,0,0),((455,3.8196),(515.5901,125),(455,246.1803)),5)
    pygame.display.flip()

pygame.quit()

#Defining action sets for the robot
def Move_Up(crnt_node,map):

    updated_node = crnt_node.copy()
    if(updated_node[1]-1 > 0) and (not Obstacle_Detection(map, updated_node[1]-1, updated_node[0])):
        Status = True
        updated_node[1] = updated_node[1] - 1 
    else:
        Status = False   
    return (Status, updated_node)

def Move_Down(crnt_node,map):    
    updated_node = crnt_node.copy()
    if(updated_node[1]+1 < map.shape[0]) and (not Obstacle_Detection(map, updated_node[1]+1, updated_node[0])):
        Status = True 
        updated_node[1] = updated_node[1] + 1
    else:
        Status = False   
    return (Status, updated_node)

def Move_Right(crnt_node,map):    
    updated_node = crnt_node.copy()
    if(updated_node[0]+1 <map.shape[1]) and (not Obstacle_Detection(map, updated_node[1], updated_node[0]+1)):
        Status = True
        updated_node[0] = updated_node[0] + 1 
    else:
        Status = False   
    return (Status, updated_node)

def Move_Left(crnt_node,map):    
    updated_node = crnt_node.copy()
    if(updated_node[0]-1 > 0) and (not Obstacle_Detection(map, updated_node[1], updated_node[0]-1)):  
        Status = True 
        updated_node[0] = updated_node[0] - 1
    else:
        Status = False   
    return (Status, updated_node)

def Move_Up_Right(crnt_node,map):
    updated_node = crnt_node.copy()    
    if(updated_node[1]-1 > 0) and (updated_node[0]+1 <map.shape[1]) and (not Obstacle_Detection(map, updated_node[1]-1, updated_node[0])):
        Status = True
        updated_node[0] = updated_node[0] + 1 
        updated_node[1] = updated_node[1] - 1
    else:
        Status = False   
    return (Status, updated_node)

def Move_Down_Right(crnt_node,map):   
    updated_node = crnt_node.copy()
    if(updated_node[1]+1 < map.shape[0]) and (updated_node[0]+1 <map.shape[1]) and (not Obstacle_Detection(map, updated_node[1]+1, updated_node[0]+1)):
        Status = True
        updated_node[0] = updated_node[0] + 1 
        updated_node[1] = updated_node[1] + 1
    else:
        Status = False   
    return (Status, updated_node)

def Move_Down_Left(crnt_node,map):    
    updated_node = crnt_node.copy()
    if(updated_node[1]+1 < map.shape[0]) and (updated_node[0]-1 >0) and (not Obstacle_Detection(map, updated_node[1]+1, updated_node[0]-1)):
        Status = True 
        updated_node[0] = updated_node[0] - 1
        updated_node[1] = updated_node[1] + 1
    else:
        Status = False   
    return (Status, updated_node)

def Move_Up_Left(crnt_node,map):    
    updated_node = crnt_node.copy()
    if(updated_node[1]-1 > 0) and (updated_node[0]-1 > 0) and (not Obstacle_Detection(map, updated_node[1]-1, updated_node[0]-1)):
        Status = True 
        updated_node[0] = updated_node[0] - 1
        updated_node[1] = updated_node[1] - 1
    else:
        Status = False   
    return (Status, updated_node)

#Defining the obstacle region in terms of half place equaitons
#The clearance of 5 mm is also considered for obtaining these coordinate points
obstacle = (0,0,250)
def Boundary_Generator(height, width):

    map = np.ones((height, width, 3))
    for i in range(map.shape[1]):
        for j in range(map.shape[0]):
            #First Rectangle Obstacle
            Rect_1 = (i>=95 and i<=155) and (j>=0 and j<=105)
            
            #second Rectangle Obstacle
            Rect_2 = (i>=95 and i<=155) and (j>=145 and j<=250)
            
            #Hexagon Obstacle
            Edge_1 = (0.577*i-j+32.57>=0)
            Edge_2 = (i-230.04>=0)
            Edge_3 = (j+0.57*i-217.14>=0)
            Edge_4 = (0.57*i-j-128.96<=0)
            Edge_5 = (i-369.95 <=0)
            Edge_6 = (j+0.57*i-378.62 <=0)
            
            #Triangle Obstacle
            Side_1 = (i-455>=0)
            Side_2 = (2.01*i- j-915.21<=0)
            Side_3 = (2.01*i+j-1163.58<=0)
            
            if(Rect_1 or Rect_2 or (Edge_1 and Edge_2 and Edge_3 and Edge_4 and Edge_5 and Edge_6) or (Side_1 and Side_2 and Side_3)):
                map[j][i] = obstacle
    return map

#Checking for coordinates in obstacle region
def Obstacle_Detection(map, x, y):
    if (map[x][y][2] < obstacle[2]):
        return False
    else:
        return True

#Checking if the coodinates have reached target
def Target_Check(crnt_node, Target_Node):
    if list(crnt_node) == Target_Node:
        return True
    else:
        return False
    
# Dijkstras Algorithm implementation
def Dijkstra_Algorithm(Initial_Node, Target_Node, map):    
    Close_List = {}    
    Open_List = []        
    heapq.heapify(Open_List)
    heapq.heappush(Open_List, [0, Initial_Node, Initial_Node])
    
    start_time = time.time()
    while True:        
        if (len(Open_List) > 0):       
            Evaluated_Node = heapq.heappop(Open_List)
            C2C, Current_Node, Parent_Node = Evaluated_Node[0], Evaluated_Node[1], Evaluated_Node[2]
            Close_List[(Current_Node[0],Current_Node[1])] = Parent_Node
            
            if Target_Check(Current_Node, Target_Node):
                print("Robot reached target!")
                end_time = time.time()
                print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                return True

            else:

                Status, Child_Node = Move_Up(Current_Node,map)    
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):     
                        Cost = C2C + 1
                        Child_Node = list(Child_Node)
                        Status_Closed_List = False    

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True        
                                if(node[0] > Cost):    
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break
                        
                        if(not Status_Closed_List):    
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True                
                Status, Child_Node = Move_Up_Right(Current_Node,map)    
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False   
                        Cost = C2C + 1.4
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                if(node[0] > Cost):   
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break

                        if(not Status_Closed_List):    
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True

                     
                Status, Child_Node = Move_Right(Current_Node,map)    
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False    
                        Cost = C2C+1
                        Child_Node = list(Child_Node)
                        
                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                if(node[0] > Cost):    
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break

                        if(not Status_Closed_List):  
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True

                
                
                Status, Child_Node = Move_Down_Right(Current_Node,map) 
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False    
                        Cost = C2C + 1.4
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                if(node[0] > Cost):  
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break

                        if(not Status_Closed_List):   
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True
                

                
                Status,Child_Node = Move_Down(Current_Node,map)   
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False 
                        Cost = C2C + 1
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                if(node[0] > Cost):    
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break
                        if(not Status_Closed_List):  
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True
                

                
                Status, Child_Node = Move_Down_Left(Current_Node,map)  
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False  
                        Cost = C2C + 1.4
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True        
                                if(node[0] > Cost):   
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break
                        if(not Status_Closed_List):    
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Close_List[Child_Node] = Current_Node
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True
                

                
                Status,Child_Node = Move_Left(Current_Node,map)  
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False 
                        Cost = C2C + 1
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                if(node[0] > Cost):    
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break
                        if(not Status_Closed_List):    
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True                


                
                Status,Child_Node = Move_Up_Left(Current_Node,map)   
                Child_Node = tuple(Child_Node)

                if(Status is True and Child_Node not in Close_List):
                    if not Target_Check(Child_Node, Target_Node):
                        Status_Closed_List = False    
                        Cost = C2C + 1.4
                        Child_Node = list(Child_Node)

                        for node in Open_List:
                            if(node[1] == Child_Node):
                                Status_Closed_List = True
                                Cost = C2C + 1.4
                                if(node[0] > Cost):  
                                    node[0] = Cost
                                    node[2] = Current_Node
                                break

                        if(not Status_Closed_List):    
                            heapq.heappush(Open_List,[Cost, Child_Node, Current_Node])
                    else:
                        print("Robot reached target!")
                        end_time = time.time()
                        print("Time: "+str(round((end_time-start_time),4)) + " [secs]")
                        Back_Tracking_Algorithm(Target_Node,Initial_Node,Close_List,map)
                        return True    
                        
        else:
            print("Feasible path not found") 
            return False

#Backtracking algorithm for tracing the shortest path
def Back_Tracking_Algorithm(Target_Node, Initial_Node, Close_List, map):
    Final_Parent_Node = Close_List.get(tuple(Target_Node))   
    cv2.line(map, tuple(Target_Node), tuple(Final_Parent_Node), (0,0,0), 1)

    Parent_Node_keys = Close_List.keys()
    for key in Parent_Node_keys:
        if key is not tuple(Initial_Node):   
            map[key[1]][key[0]] = [255,0,0]
            cv2.circle(map,tuple(Initial_Node),5,(0,255,0),-1)            
        cv2.circle(map,tuple(Target_Node),5,(0,255,0),-1)
        cv2.imshow("Robot Path",map)
        cv2.waitKey(1)

    while True:
        key = Close_List.get(tuple(Final_Parent_Node))    
        cv2.line(map, tuple(key), tuple(Final_Parent_Node), (0,0,0), 1)
        Final_Parent_Node = key
        if key is Initial_Node:
            break
    cv2.imshow("Robot Path", map)
    cv2.waitKey(0)
    
#Main function for the program
if __name__ == '__main__':  
    map = Boundary_Generator(250, 600)                  
    print('Initializing mapping sequence')
    X_Initial = int(input("Enter the initial X-axis coordinate of robot: "))
    Y_Initial = int(input("Enter the initial Y-axis coordinate of robot: "))
    print('Enter robot destination')
    X_Target = int(input("Enter the target robot x_axis coordinate: "))
    Y_Target = int(input("Enter the target robot y_axis coordinate: "))
    print('Solving for destination...................')
    if Obstacle_Detection(map, Y_Initial, X_Initial):
        print("Invalid Input: Start location is in obstacle coordinate space")
    if Obstacle_Detection(map, Y_Target, X_Target):
        print("Invalid Input: Target location is in obstacle coordinate space")
    else:
        Initial_Node = [X_Initial, Y_Initial]
        Target_Node = [X_Target, Y_Target]
            
        res = Dijkstra_Algorithm(Initial_Node, Target_Node, map)
        cv2.destroyAllWindows()
