import pygame
import sys
import random
from opponent import opponent

class player():
    def __init__(self):
        self.position = [(screen_width/2)-(gridsize/2), (screen_height-gridsize)]
        self.direction = (0, 0)
        self.color = (17, 24, 47)

    def getPosition(self):
        return self.position

    def turn(self, point):
        self.direction = point

    def invert(self):
        if self.direction == up: self.direction = down
        elif self.direction == down: self.direction = up
        elif self.direction == right: self.direction = left
        elif self.direction == left: self.direction = right

    def move(self):
        x,y = self.direction
        if ((self.position[0]+(x*gridsize))) < screen_width and ((self.position[0]+(x*gridsize))) > -1 and (self.position[1]+(y*gridsize)) < screen_height and (self.position[1]+(y*gridsize)) > -1:
            self.position = (((self.position[0]+(x*gridsize))), (self.position[1]+(y*gridsize)))
        #self.direction = [0,0]

    def draw(self,surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize,gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                    self.move()
                    return False
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                    self.move()
                    return False
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                    self.move()
                    return False
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                    self.move()
                    return False
        return True

class wall():
    def __init__(self, x=0, y=0, direc=''):
        if x == 0:
            self.position = (0,0)
            self.color = (223, 163, 49)
            self.direction = random.choice(["vert", "horiz"])
            self.randomize_position()
            self.length = 3
        else:
            self.position = (x*gridsize, y*gridsize)
            self.color = (223, 163, 49)
            self.direction = direc
            #self.randomize_position()
            self.length = 3
    def getPosW(self):
        return self.position
    def randomize_position(self):
        pValida = False
        while not pValida:
           if self.direction == "vert":
              x = (random.randint(0, grid_width-3))  
              y = (random.randint(0, grid_height-3))
              if ( x % 2 != 0 and y % 2 != 1):
                 self.position = (x*gridsize, y*gridsize)
                 pValida = True
           else: 
              x = (random.randint(0, grid_width-3))  
              y = (random.randint(0, grid_height-3))
              if ( x % 2 != 1 and y % 2 != 0):
                 self.position = (x*gridsize, y*gridsize)
                 pValida = True


    def draw(self, surface):
        if self.direction == "vert":
            r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize*self.length))
        else : r = pygame.Rect((self.position[0], self.position[1]), (gridsize*self.length, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if y%2 != 0 or x%2 != 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 578
screen_height = 578

gridsize = 2*17
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-2)
down = (0,2)
left = (-2,0)
right = (2,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    walls = []
    #posW = []
    posWV = []
    posWH = []
    player1 = player() 
    ops = [opponent([(screen_width/2)-(gridsize/2), (0)], (0, 8), (16, 8), 1, (245, 245, 220, 255), 0), \
           opponent([(0), (screen_height/2)-(gridsize/2)], (8, 0), (8, 16), 1, (127, 255, 212, 255), 1), \
           opponent([16*gridsize, (screen_height/2)-(gridsize/2)], (8, 16), (8, 0), 1, (255, 100, 100), 1)]
    ops[0].mapping(walls)
    ops[0].path(ops[0].getPos())
    ops[0].cambiarMoves()
    ops[1].mapping(walls)
    ops[1].path2((ops[1].getStart()))
    ops[2].mapping(walls)
    ops[2].path3(ops[2].getMap(), 8, 16)
    turn1= True
    myfont = pygame.font.SysFont("monospace",16)
    id = [[1,2],[0,2],[0,1]]
    while (True):
        clock.tick(10)
        if turn1: 
            turn1 = player1.handle_keys()
            for i in range(len(ops)):
                if ops[i].position[0] == player1.position[0] and ops[i].position[1] == player1.position[1]: 
                    player1.turn(random.choice([player1.direction, [player1.direction[1], player1.direction[0]], [-player1.direction[1], -player1.direction[0]]]))
                    player1.move()
        else:
            pared = False
            cnt = 0
            for op in ops:
                for j in range(2):
                    if op.paredesL():
                        if op.getMovesL() > ops[id[cnt][j]].getMovesL() and (not op.gReach()):
                            path = ops[id[cnt][j]].getPath()
                            if ops[id[cnt][j]].getType() == 1:
                                current, max = ops[id[cnt][j]].getMoveData()
                                for i in range(current, max-1):
                                    x = path[i + 1][1]
                                    y = path[i + 1][0]
                                    x -= 1
                                    if ([x,y+2] in posWV) and ([x,y] in posWV):
                                        continue
                                    elif x > 0 and y > 0 and y < 15 or x < 18 and ([x,y] not in posWV):
                                        walls.append(wall(x, y, 'vert'))
                                        pared = True
                                        posWV.append([x,y])
                                        op.subPared()
                                        op.setuPared(True)
                                        break
                            elif ops[id[cnt][j]].getType() == 0:
                                current, max = ops[id[cnt][j]].getMoveData()
                                for i in range(current, max-1):
                                    x = path[i + 1][1]
                                    y = path[i + 1][0]
                                    y -= 1
                                    if ([x+2,y] in posWH) and ([x,y] in posWH):
                                        continue
                                    elif x > 0 and y > 0 and y < 18 and x < 15 and ([x,y] not in posWH):
                                        walls.append(wall(x, y, 'horiz'))
                                        pared = True
                                        posWH.append([x,y])
                                        op.subPared()
                                        op.setuPared(True)
                                        break

                    break
                cnt += 1
            if pared: # recalculando paths si es que se coloco una pared nueva
                
                ops[0].mapping(walls)
                ops[0].path(ops[0].getPos())
                ops[0].cambiarMoves()

                ops[1].mapping(walls)
                ops[1].path2((ops[1].getCurrMove(0)))

                ops[2].mapping(walls)
                nx, ny = ops[2].getCurrMove(1)[0], ops[2].getCurrMove(1)[1]
                ops[2].reboot(nx, ny)
                ops[2].path3(ops[2].getMap(), nx, ny)

            ops[0].move2()
            if ops[0].position[0] == player1.position[0] and ops[0].position[1] == player1.position[1]:
                ops[0].move2()
            ops[1].move2()
            if ops[1].position[0] == player1.position[0] and ops[1].position[1] == player1.position[1]:
                ops[1].move2()
            ops[2].move2()
            if ops[2].position[0] == player1.position[0] and ops[2].position[1] == player1.position[1]:
                ops[2].move2()
            turn1 = True
        drawGrid(surface)
        for i in range(len(walls)):
            if walls[i].direction == "vert":
                if (player1.getPosition()[0]-(player1.direction[0]/2)*gridsize >= walls[i].position[0] and player1.getPosition()[0]-(player1.direction[0]/2)*gridsize <= walls[i].position[0] 
                and player1.getPosition()[1] >= walls[i].position[1] and player1.getPosition()[1] <= (walls[i].position[1])+((walls[i].length-1)*gridsize)):
                    player1.invert()
                    player1.move()
                    turn1= True
            else: 
                if (player1.getPosition()[0] >= walls[i].position[0] and player1.getPosition()[0] <= (walls[i].position[0])+((walls[i].length-1)*gridsize) 
                and player1.getPosition()[1]-(player1.direction[1]/2)*gridsize >= walls[i].position[1] and player1.getPosition()[1]-(player1.direction[1]/2)*gridsize <= walls[i].position[1]):
                    player1.invert()
                    player1.move()
                    turn1= True
        player1.draw(surface)
        for op in ops:
            op.draw(surface)
            op.checkGoal()
            op.setuPared(False)

        for i in range(len(walls)):
            walls[i].draw(surface)
        player1.turn((0, 0))
        screen.blit(surface, (0,0))
        pygame.display.update()

main()
