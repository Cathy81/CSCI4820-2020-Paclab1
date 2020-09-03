#using AIMA-PYTHON to solve pacman,single capsule, BFS, and DFS

import pygame, sys, random, math
sys.path.insert(0, ".\\aima-python-master")
from search import *
from pygame.locals import *
from maze_graph import *
from Pacman import *
from pacmanGame import *

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SCORE_SURF, SCORE_RECT, SOLVE_SURF, SOLVE_RECT
    global walls, pacmanPos,capsulePos,game,pacman,score, scoreText
    score=0
    filename=".\\layouts\\smallestMaze.lay"
    game=PacGame(filename)

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((game.WINDOWWIDTH, game.WINDOWHEIGHT))
    pygame.display.set_caption('PacMan')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    scoreText='SCORE:'+str(score)
    SCORE_SURF, SCORE_RECT = makeText(scoreText, TEXTCOLOR, BGCOLOR, 10, game.WINDOWHEIGHT - 40)
    DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)
    game.genMaze()
    pacmanPos=game.pacmanPos

    walls=game.walls
    allMoves = [] # list of moves made from the solved configuration
    game.drawWall(DISPLAYSURF)
    pacman=Pacman(pacmanPos,0,PACCOLOR,PAC_SIZE,0,walls,game.MAZE_WIDTH,game.MAZE_HEIGHT)
    pacman.drawPacman(DISPLAYSURF)
    game.drawCapsule(DISPLAYSURF)
    p_graph=build_graph(game)
    pygame.time.wait(2000)
    slideTo = None  # the direction, if any, a tile should slide
    scores = 0
    pygame.display.update()

    if (len(sys.argv) <=1):
        while True:# main game loop
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (K_LEFT, K_a):
                        slideTo = 'West'
                    elif event.key in (K_RIGHT, K_d):
                        slideTo = 'East'
                    elif event.key in (K_UP, K_w):
                        slideTo = 'North'
                    elif event.key in (K_DOWN, K_s):
                        slideTo = 'South'
                    if slideTo and len(game.capsulePos)>0:
                        slideAnimation(slideTo, "Ok", 8)  #
                        scores += 1
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)
                        scoreText = 'SCORE:' + str(scores)
                        SCORE_SURF, SCORE_RECT = makeText(scoreText, TEXTCOLOR, BGCOLOR, 10, game.WINDOWHEIGHT - 40)
                        DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
    else:
        if(sys.argv[1]=='auto'):
            choices=['East','West','North','South']
            while True:  # main game loop
                for event in pygame.event.get(): # event handling loop
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                #scores=0
                while(game.capsulePos):
                    pac_actions = []
                    #Q6) add a simple reflex agent:It randomly choose an action,
                    # and append it to the list pac_actions
                    # you may need nextDirectionIsValid(direction, pacman.pos[0]) in pacmanGame.py




                    pac_actions = find_solution(p_graph)
                    game.pacmanPos.pop(0)
                    game.pacmanPos.append(game.capsulePos[0])
                    while (pac_actions):
                        slideTo = pac_actions.pop(0)
                        if slideTo:
                            slideAnimation(slideTo, "Ok", 8)  #
                        scores+=1
                        FPSCLOCK.tick(FPS)
                        scoreText = 'SCORE:' + str(scores)
                        SCORE_SURF, SCORE_RECT = makeText(scoreText, TEXTCOLOR, BGCOLOR, 10, game.WINDOWHEIGHT - 40)
                        DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)

                pygame.display.update()
                FPSCLOCK.tick(FPS)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def slideAnimation(direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.
     # prepare the base surface
    baseSurf = DISPLAYSURF.copy()
    (x,y) = pacman.pos[0]
    xTop,yTop=x * PAC_SIZE* 2, y*PAC_SIZE*2
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (xTop,yTop, PAC_SIZE * 2, PAC_SIZE * 2))
    (xEnd, yEnd) =pacman.makeMove(direction)#pop the initial pos in makeMove

    if(xEnd,yEnd) in game.capsulePos:
        game.capsulePos.pop(game.capsulePos.index((xEnd,yEnd)))
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    pacman.drawPacman(baseSurf) #open widely

    DISPLAYSURF.blit(baseSurf, (0, 0))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pacman.drawPacman(DISPLAYSURF)
    game.drawCapsule(DISPLAYSURF)

def build_graph(game):
    gr = MazeGraph(game)
    gr.genGraph()
    # gr.genLocation()
    directions = []
    return gr

def find_solution(gr):
    pacG = gr.pacGame
    pacman_problem = GraphProblem(pacG.pacmanPos[0], pacG.capsulePos[0], gr.graph)
    #node=simple_reflex_search(pacman_problem)
    node = depth_first_graph_search(pacman_problem)
    #node = breadth_first_search(pacman_problem)
    #node=uniform_cost_search(pacman_problem)
    #node = astar_search(pacman_problem)
    #node = astar_search(pacman_problem)
    solutions = node.solution()
    prev=pacG.pacmanPos[0]
    directions=[]
    while solutions:
        step=solutions.pop(0)
        direction=getDirection(prev,step)
        directions.append(direction)
        prev=step
    return directions

def getDirection(prev,step):
    if(sub(step,prev)==(1,0)):
        dire="East"
    elif (sub(step,prev)==(-1,0)):
        dire="West"
    elif (sub(step,  prev) == (0, -1)):
        dire = "North"
    elif (sub(step, prev) == (0, 1)):
        dire = "South"
    else:
        dire=None
    return dire

def simple_reflex_search(pacman_problem):
    pass

if __name__ == '__main__':
    main()
