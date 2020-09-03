#from pacman3.py import *
import sys
sys.path.insert(0, ".\\aima-python-master")
from search import *
from pacmanGame import *
class MazeGraph:

    def __init__(self, pac_game):
        self.pacGame=pac_game
       # self.maze_str=pac_game.strS #[str[0]][len(str)], for example, middlwMaze 18rows, 36 cols
        self.maze_height=len(self.pacGame.strS)
        self.maze_width=len(self.pacGame.strS[0])
        self.walls =pac_game.walls
        self.map = dict()
        self.graph=dict()
        self.sortedCapsulePos=[]

    def genGraph(self):
        dict={}

        xMax=self.maze_width
        yMax=self.maze_height

        for x in range(1,xMax-1):
            for y in range(1, yMax-1):
                if(self.walls[x][y]==True):
                    continue;
                else:
                    dict1={}
                    if(self.walls[x+1][y]==False):
                        dict1[(x+1, y)]=1  # suppose the cost is 1
                    if (self.walls[x][y+1] == False):
                        dict1[(x, y+1)]=1
                    if (self.walls[x][y-1] == False):
                        dict1[(x, y-1)] = 1  # suppose the cost is 1
                    if (self.walls[x-1][y] == False):
                        dict1[(x-1, y)] = 1
                    dict[(x,y)]=dict1
        self.map=dict
        self.graph=UndirectedGraph(self.map)
        self.graph.locations= {(0,0)}

    def getkey(self,item):
        return item[1]

    def print_map(self):
        for k, v in self.map.items():
            print(k, v)

    def print_keys(self):
        for k in self.map.keys():
            print (k)
