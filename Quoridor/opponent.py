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

#Matriz para el mapa
mat = [[] for x in range(n)] 

#start, end = (-1, -1), (-1, -1)
mat = [['.' for y in range(m)] for x in range(n)]
    
#start = ((0), (8))
#end = ((16), (8))

# Matriz de visitados y movimientos realizados
p = [[-1 for y in range(m)] for x in range(n)] #p

#p[start[0]][start[1]] = -2
#q = deque([start])

#recursos para Greedy Best First Search


class opponent():
      def __init__(self, position, start, end, type, color):
         self.position = position
         self.color = color
         self.start = start
         self.end = end
         ################# para algoritmo 1
         #self.v = p
         self.v = [[-1 for y in range(m)] for x in range(n)] #p
         self.v[self.start[0]][self.start[1]] = -2
         #self.deq = q
         self.deq = deque([self.start])
         self.moves = []
         self.moveCount = type
         ################# para algoritmo 2
         self.frontier = PriorityQueue()
         self.frontier.put((0, self.start))
         self.came_from = []
         self.camino = []
         self.came_from.append(self.start)
         self.counter = 0 #ayuda para la implementacion del PrioQueue modifica la prioridad


      def draw(self,surface):
         r = pygame.Rect((self.position[0], self.position[1]), (gridsize,gridsize))
         pygame.draw.rect(surface, self.color, r)
         pygame.draw.rect(surface, (93,216, 228), r, 1)

      def mapping(self, walls): #para buscar donde hay paredes y ponerlas en la matriz mat
         for i in range(n):
             for j in range(m):
                for w in range(len(walls)):
                    if i*(gridsize) == walls[w].position[1] and j*(gridsize) == walls[w].position[0]:
                        mat[i][j] = '='
                        if walls[w].direction == "vert":
                            mat[i+1][j] = '='
                            mat[i+2][j] = '='
                        else:
                            mat[i][j+1] = '='
                            mat[i][j+2] = '='
         #for i in range(n):
             #print(mat[i])
      def getMap(self):
          return mat
      def getEnd(self):
          return self.end
########################### algoritmo 1
      def move(self):
          if self.moveCount < len(self.moves):
              step = self.moves[self.moveCount]
              if step == 'D':
                 self.position = [self.position[0], self.position[1]+2*gridsize]
              elif step == 'R':
                 self.position = [self.position[0]+2*gridsize, self.position[1]]
              elif step == 'L':
                 self.position = [self.position[0]-2*gridsize, self.position[1]]
              elif step == 'U':
                 self.position = [self.position[0], self.position[1]-2*gridsize]
          if self.moveCount < len(self.moves): self.moveCount +=1

      def path(self):
         def reconstruct_path():
            print("YES")
            r, c  = self.end
            path = deque()
            while self.v[r][c] >= 0:
                i = self.v[r][c] 
                path.appendleft(dd[i])
                r -= dx[i]*2
                c -= dy[i]*2
            print(len(path))
            self.moves = path
            #return ''.join(path)

         def valid(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (mat[r][c] != '=') and (self.v[r][c] == -1)
         
         while len(self.deq):
            r, c = self.deq.popleft()
            if (r, c) == self.end:
                return reconstruct_path()
                #exit()
            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                nr2, nc2 = r + dx[i]*2, c + dy[i]*2
                if valid(nr, nc):
                    self.v[nr][nc] = i
                    self.v[nr2][nc2] = i
                    self.deq.append((nr2, nc2))

####################### algoritmo 3
      def path3(self, maze, end, row, col):
          def valid(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (mat[r][c] != '=') and (self.v[r][c] == -1)

          nrows = len(maze)
          ncols = len(maze[0])
          if self.end[0] == row and self.end[1] == col:#endrow == row and endcol == col:
              self.moves.append([row, col])
              for i in range(m):
                  for j in range(n):
                      self.v[i][j] = 1
              #p = [[1 for y in range(m)] for x in range(n)]
              print(self.moves)
              #self.moves = way
              found = True
              return 
          else:
              if valid(row + 1, col):
                  self.v[row+1][col] = 1
                  self.moves.append([row, col])
                  self.path3(maze, self.end, row + 2, col)
              if valid(row, col - 1):
                  self.v[row][col-1] = 1
                  self.moves.append([row, col])
                  self.path3(maze, self.end, row, col - 2)
              if valid(row - 1, col):
                  self.v[row-1][col] = 1
                  self.moves.append([row, col])
                  self.path3(maze, self.end, row - 2, col)
              if valid(row, col + 1):
                  self.v[row][col+1] = 1
                  self.moves.append([row, col])
                  self.path3(maze, self.end, row, col + 2)
          return False
############################ algoritmo 2
      def move2(self):
        if self.moveCount <= len(self.moves)-1:
          self.position = (self.moves[self.moveCount][1]*gridsize, self.moves[self.moveCount][0]*gridsize)
        if self.moveCount <= len(self.moves)-1: self.moveCount +=1

      def path2(self):
        def valid2(r, c):
          return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
             and (mat[r][c] != '=')

        def heuristic(end, nr, nc):
            # Manhattan distance on a square grid
            return abs(self.end[0]-nr) + abs(self.end[1]-nc)

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
                  #came_from.append(current[1])
            self.counter += 1

