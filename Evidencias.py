from collections import deque
from queue import PriorityQueue

""" 
. -> posiciones para el jugador
| y - -> posiciones para poner paredes
= -> pared
Ejemplo de input
17 17
.|.|.|.|A|.|.|.|.
-|-|-|-|-|-|-|-|-
.|.|.|.|.=.|.|.|.
-|-|-|====.|.|-|-
.|.|.|.|.=.|.|.|.
.|.|-|-|-|===|-|-
.|.|.|.|.|.|.|.|.
-|-|-======|-|-|-
.|.|.|.|.|.|.|.|.
-|-|-|-|-=-|-|-|-
.|.|.|.|.=.|.|.|.
-|-=-|-|-=-|-|-|-
.|.=.|.|.|.|.|.|.
-|-====|-|===|-|-
.=.|.|.|.|.|.|.|.
-=-|-|-===-|-|-|-
.=.|.|.|B|.|.|.|.
"""

## Dos arreglos paralelos dx, dy para enumerar movimientos
## El movimiento i es (x + dx[i], y + dy[i])
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
dd = list("DURL") #para enumerar movimientos
n, m = [int(x) for x in input().split()] 

#Matriz para el mapa
mat = [[] for x in range(n)] 

start, end = (-1, -1), (-1, -1)
for i in range(n):
	mat[i] = list(input())
	for j in range(m):
		if mat[i][j] == 'A':
			start = (i, j)
		if mat[i][j] == 'B':
			end = (i, j)

# Matriz de visitados y movimientos realizados
p = [[-1 for y in range(m)] for x in range(n)] #p

p[start[0]][start[1]] = -2
q = deque([start])
found = False
####### valida algoritmo de BFS y Backtracking
def valid(r, c):
	return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
		and (mat[r][c] != '=') and (p[r][c] == -1)

####### valida algoritmo de GBFS
def valid2(r, c):
	return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
		and (mat[r][c] != '=')

################# algoritmo BFS
printed = False
def reconstruct_path():
	global printed
	r, c  = end
	path = deque()
	while p[r][c] >= 0:
		i = p[r][c] 
		path.appendleft(dd[i])
		r -= dx[i]*2
		c -= dy[i]*2
	if not printed:
		print("Algoritmo BFS:")
		print(len(path))
		print(''.join(path))
		printed = True

		
while len(q):
	r, c = q.popleft()
	if (r, c) == end:
		reconstruct_path()
		#exit()
	for i in range(4):
		nr, nc = r + dx[i], c + dy[i]
		nr2, nc2 = r + dx[i]*2, c + dy[i]*2
		if valid(nr, nc):
			p[nr][nc] = i
			p[nr2][nc2] = i
			q.append((nr2, nc2))

####### recursos Algoritmo GBFS
frontier = PriorityQueue()
frontier.put((0, start))
came_from = []
camino = []
came_from.append(start)
counter = 0

################## algoritmo GBFS
def heuristic(end, nr, nc):
   # Manhattan distance - distancia entre el punto y la meta
   return abs(end[0]-nr) + abs(end[1]-nc)


while not frontier.empty():
    current = frontier.get()
    camino.append(current[1])
    if current[1] == end: 
       break

    for next in range(4):
       nr, nc = current[1][0] + dx[next], current[1][1] + dy[next]
       nr2, nc2 = current[1][0] + dx[next]*2, current[1][1] + dy[next]*2
       if valid2(nr, nc) and ((nr2, nc2) not in came_from):
          priority = heuristic(end, nr2, nc2)
          frontier.put((priority - counter, (nr2, nc2)))
          came_from.append((nr2, nc2))
    counter += 1
print("       ")
print("Algoritmo GBFS:")
print(len(camino)-1)
print(camino)

################## Algoritmo de Backtracking
p = [[-1 for y in range(m)] for x in range(n)]
way = []
def solveMaze(maze, end, row, col):
    nrows = len(maze)
    ncols = len(maze[0])

    if end[0] == row and end[1] == col:
        way.append([row, col])
        for i in range(m):
            for j in range(n):
                p[i][j] = 1
        print(len(way)-1)
        print(way)
        found = True
        return 
    else:
        if valid(row, col - 1):
            p[row][col-1] = 1
            way.append([row, col])
            solveMaze(maze, end, row, col - 2)
        if valid(row + 1, col):
            p[row+1][col] = 1
            way.append([row, col])
            solveMaze(maze, end, row + 2, col)
        if valid(row, col + 1):
            p[row][col+1] = 1
            way.append([row, col])
            solveMaze(maze, end, row, col + 2)
        if valid(row - 1, col):
            p[row-1][col] = 1
            way.append([row, col])
            solveMaze(maze, end, row - 2, col)
    return False
print("       ")
print("Algoritmo Backtracking:")
solveMaze(mat, end, start[0], start[1])
#print("NO")
