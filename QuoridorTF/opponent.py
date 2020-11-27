from collections import deque
import pygame
from queue import PriorityQueue
screen_width = 578
screen_height = 578

gridsize = 2*17
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
dd = list("DURL") #para enumerar movimientos
n, m = 17, 17

# Matriz de visitados y movimientos realizados
p = [[-1 for y in range(m)] for x in range(n)] #p


class opponent():
      def __init__(self, position, start, end, moveC, color, type):
         self.position = position
         self.color = color
         self.start = start
         self.end = end
         self.moves = []
         self.moveCount = moveC
         self.type = type
         self.movesLeft = 0
         self.paredes = 5
         self.usePared = False
         self.goalReach = False
         #Matriz para el mapa
         self.mat = [[] for x in range(n)] 
         #start, end = (-1, -1), (-1, -1)
         self.mat = [['.' for y in range(m)] for x in range(n)]
         ################# para algoritmo 1
         #self.v = p
         self.v = [[-1 for y in range(m)] for x in range(n)] #p
         self.v[self.start[0]][self.start[1]] = -2
         #self.deq = q
         self.deq = deque([self.start])
         ################# para algoritmo 2
         self.frontier = PriorityQueue()
         #self.frontier.put((0, self.start))
         self.came_from = []
         self.camino = []
         self.came_from.append(self.start)
         self.counter = 0 #ayuda para la implementacion del PrioQueue modifica la prioridad


      def draw(self,surface):
         r = pygame.Rect((self.position[0], self.position[1]), (gridsize,gridsize))
         pygame.draw.rect(surface, self.color, r)
         pygame.draw.rect(surface, (93,216, 228), r, 1)

      def mapping(self, walls): #para buscar donde hay paredes y ponerlas en la matriz mat
         #Matriz para el mapa
         self.mat = [[] for x in range(n)] 
         #start, end = (-1, -1), (-1, -1)
         self.mat = [['.' for y in range(m)] for x in range(n)]
         for i in range(n):
             for j in range(m-1):
                for w in range(len(walls)):
                    if i*(gridsize) == walls[w].position[1] and j*(gridsize) == walls[w].position[0]:
                        self.mat[i][j] = '='
                        if walls[w].direction == "vert":
                            self.mat[i+1][j] = '='
                            self.mat[i+2][j] = '='
                        else:
                            self.mat[i][j+1] = '='
                            self.mat[i][j+2] = '='


      def getMovesL(self):
          return self.movesLeft
      def getMap(self):
          return self.mat
      def getEnd(self):
          return self.end
      def getMoveData(self):
          return self.moveCount, len(self.moves)
      def getMoveCount(self):
          return self.moveCount
      def getType(self):
          return self.type
      def getPath(self):
          return self.moves
      def getStart(self):
          return self.start
      def paredesL(self):
          return self.paredes > 0
      def subPared(self):
          self.paredes -=1
      def getPos(self):
          return self.position
      def usedPared(self):
          return self.usePared
      def setuPared(self, condicion):
          self.usePared = condicion
      def checkGoal(self):
          if self.position[0]/gridsize == self.end[1] and self.position[1]/gridsize == self.end[0]:
              self.goalReach = True
      def gReach(self):
          return self.goalReach
      def getCurrMove(self, i):
          return self.moves[self.moveCount-i]
########################### algoritmo 1
      def move(self):
          if self.moveCount < len(self.moves):
              step = self.moves[self.moveCount]
              if step == 'D':
                 self.position = [self.position[0]*gridsize, self.position[1]+2*gridsize]
              elif step == 'R':
                 self.position = [self.position[0]+2*gridsize, self.position[1]*gridsize]
              elif step == 'L':
                 self.position = [self.position[0]-2*gridsize, self.position[1]*gridsize]
              elif step == 'U':
                 self.position = [self.position[0]*gridsize, self.position[1]-2*gridsize]
              self.movesLeft = len(self.moves) - self.moveCount
          if self.moveCount < len(self.moves): self.moveCount +=1

      def cambiarMoves(self):
          moves2 = []
          self.moveCount = 1
          moves2.append([int(self.position[0]/gridsize), int(self.position[1]/gridsize)])
          for i in range(len(self.moves)):
              step = self.moves[i]
              if step == 'D':
                 moves2.append([moves2[-1][0], moves2[-1][1]+2])
              elif step == 'R':
                 moves2.append([moves2[-1][0]+2, moves2[-1][1]])
              elif step == 'L':
                 moves2.append([moves2[-1][0]-2, moves2[-1][1]])
              elif step == 'U':
                 moves2.append([moves2[-1][0], moves2[-1][1]-2])
          for i in range(len(moves2)):
              moves2[i] = [moves2[i][1],moves2[i][0]]
          self.moves = moves2

      def path(self, init):
         self.v = [[-1 for y in range(m)] for x in range(n)]
         self.v[self.start[0]][self.start[1]] = -2
         initR = [int(init[1]/gridsize), int(init[0]/gridsize)]
         init2 = [int(init[0]/gridsize), int(init[1]/gridsize)]
         self.deq = deque([initR])
         self.position = init
         self.moves = []
         self.moveCount = 1

         def reconstruct_path():
            r, c  = self.end
            path = deque()
            while self.v[r][c] >= 0:
                i = self.v[r][c] 
                path.appendleft(dd[i])
                r -= dx[i]*2
                c -= dy[i]*2
            self.moves = path

         def valid(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (self.mat[r][c] != '=') and (self.v[r][c] == -1)
         
         while len(self.deq):
            r, c = self.deq.popleft()
            if (r, c) == self.end:
                return reconstruct_path()
            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                nr2, nc2 = r + dx[i]*2, c + dy[i]*2
                if valid(nr, nc):
                    self.v[nr][nc] = i
                    self.v[nr2][nc2] = i
                    self.deq.append((nr2, nc2))

############################ algoritmo 2
      def move2(self):
        if (not self.usePared) and (not self.goalReach):
            if self.moveCount <= len(self.moves)-1:
              self.position = [self.moves[self.moveCount][1]*gridsize, self.moves[self.moveCount][0]*gridsize]
              self.movesLeft = len(self.moves) - self.moveCount
            if self.moveCount <= len(self.moves)-1: 
              self.moveCount +=1
            #else: 
                #self.moves = [[], moves[-1]]
                #self.moveCount = 0


      def path2(self, init):
        def valid2(r, c):
          return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
             and (self.mat[r][c] != '=')

        def heuristic(end, nr, nc):
            # distancia
            return abs(self.end[0]-nr) + abs(self.end[1]-nc)

        self.moves = []
        self.frontier = PriorityQueue()
        self.frontier.put((0, init))
        self.came_from = [init]
        self.moveCount = 1
        self.counter = 0
        while not self.frontier.empty():
            current = self.frontier.get()
            self.moves.append(current[1])
            if current[1] == self.end: 
               break

            for next in range(4):
               nr, nc = current[1][0] + dx[next], current[1][1] + dy[next]
               nr2, nc2 = current[1][0] + dx[next]*2, current[1][1] + dy[next]*2
               if valid2(nr, nc) and ((nr2, nc2) not in self.came_from):
                  priority = heuristic(self.end, nr2, nc2)
                  self.frontier.put((priority - self.counter, (nr2, nc2)))
                  self.came_from.append((nr2, nc2))
            self.counter += 2

####################### algoritmo 3
      def reboot(self, x, y):
          self.v = [[-1 for y in range(m)] for x in range(n)] #p
          self.v[x][y] = -2
          self.moveCount = 1
          self.moves = []

      def path3(self, maze, row, col):
          def valid(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (self.mat[r][c] != '=') and (self.v[r][c] == -1)

          nrows = len(maze)
          ncols = len(maze[0])

          if self.end[0] == row and self.end[1] == col:
              self.moves.append([row, col])
              for i in range(m):
                  for j in range(n):
                      self.v[i][j] = 1
              #print(self.moves)
              return 
          else:
              if valid(row - 1, col):
                  self.v[row-1][col] = 1
                  self.moves.append([row, col])
                  self.path3(maze, row - 2, col)
              if valid(row, col - 1):
                  self.v[row][col-1] = 1
                  self.moves.append([row, col])
                  self.path3(maze, row, col - 2)
              if valid(row + 1, col):
                  self.v[row+1][col] = 1
                  self.moves.append([row, col])
                  self.path3(maze, row + 2, col)
              if valid(row, col + 1):
                  self.v[row][col+1] = 1
                  self.moves.append([row, col])
                  self.path3(maze, row, col + 2)
          return False


