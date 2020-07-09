import pygame 
from sys import exit
n = 20
infinity = 99999

pygame.init()
size = 20
m = 20

display_width = size*m
display_height = size*m
gameDisplay = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
crashed = False
black = (0,0,0)
red = (200,0,0)
white = (255,255,255)
green = (0, 200, 0 )

#variables
processed = []
finish = (15,15)
run = True
crashed = False
path_arr = []

def drawBoard():
    #draw finish
    pygame.draw.rect(gameDisplay,green,(finish[0]*size,finish[1]*size,size,size))
    
    #trial obstacle
    pygame.draw.rect(gameDisplay, black,(4*size,4*size,size*6,size))
    pygame.draw.rect(gameDisplay, black,(4*size,size*4,size,size*12))
    pygame.draw.rect(gameDisplay, black,(10*size,size*4,size,size*12))
    #main part to draw the board itself
    for i in range(size):
        pygame.draw.rect(gameDisplay, black,(i*m,0,1,size*(m)))
        pygame.draw.rect(gameDisplay, black,(0,i*m,size*(m),1))

#gets the costs for the graph
def get_costs():
    costs = {}
    for i in range(n):
        for j in range(n):
            costs[i,j] = infinity
    costs[0,1]=1
    costs[1,0] = 1
    return costs

def get_parents():
    parents = {}
    for i in range(n):
        for j in range(n):
            parents[i,j] = None
    parents[0,1] = 0,0
    parents[1,0] = 0,0
    return parents

#trial function as obstacle
def obstacle():
    arr_x = []
    arr_y = []
    for i in range(12):
        arr_x.append(4)
        arr_y.append(4+i)
        arr_x.append(10)
        arr_y.append(4+i)
    for j in range(6):
        arr_x.append(4+j)
        arr_y.append(4)
        
    return arr_x,arr_y

#checks for walls and obstacles on the map
def is_valid(x,y):
    validx,validy = obstacle()
    if x>=0 and x<n and y>=0 and y<n:
        for i in range(len(validx)):
            if (x == validx[i] and y == validy[i]) :
                return False
        else:
            return True
    else:
        return False
    
    
def get_neighbours(x,y,graph):
    for k in range(-1,2):
        for l in range(-1,2):
            if is_valid(x+k,y+l) and k !=l:
                graph[x,y][x+k,y+l] = 1
    return graph[x,y]

def get_graph():
    graph = {}
    for i in range(n):
        for j in range(n):
            graph[i,j] = {}
            graph[i,j] = get_neighbours(i,j,graph)
    return graph
            
graph = get_graph()
costs = get_costs()
parents = get_parents()


def find_lowest_cost_node(costs):
    lowest_cost = infinity
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost< lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

def check_processed(processed):
    if(len(processed)>1):
        for i in range(len(processed)):
            pygame.draw.rect(gameDisplay,red,(size*processed[i][0],
                                              size*processed[i][1],
                                              size,size))
            clock.tick(50)
            pygame.display.update()
            

def dijkstra():
    node = find_lowest_cost_node(costs)
    
    while node is not None: 
        
        cost = costs[node]
        neighbours = graph[node]
        for n in neighbours.keys():
            new_cost = cost + neighbours[n]
            if costs[n] > new_cost:
                costs[n] = new_cost 
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs)
        if(node == finish):
            run = False
            check_processed(processed)
            get_path(node,parents,path_arr)
            
            

#recursion to get path and draw it on the board
def get_path(node,parents,path_arr):
    
    if (node == (0,0)):
        path_arr.append(node)
        pygame.draw.rect(gameDisplay,white,(size*node[0],
                                           size*node[1],
                                           size,size))
        clock.tick(30)
        if run:
            pygame.display.update()
        return path_arr
    path_arr.append(node)
    if(node != (0,0)):
        pygame.draw.rect(gameDisplay,white,(size*node[0],
                                           size*node[1],
                                           size,size))
        clock.tick(30)
        if run:
            pygame.display.update()
        return get_path(parents[node],parents,path_arr)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
           
            
            
     
    pygame.display.set_caption("Dijkstras algo")
    gameDisplay.fill(white)
    drawBoard()
    while run:
        pygame.display.update()
        clock.tick(5)
        dijkstra()
    
    
pygame.display.quit()    
pygame.quit()
exit()


