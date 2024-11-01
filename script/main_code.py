import pygame
from queue import PriorityQueue
from tkinter import messagebox, Tk
import time

def main_program(pfAlgorithm : int = 0, mazeAlgorithm : int = 0):

    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Pathfinding Algorithm Visualizer")

    RED = (255, 0, 128)
    GREEN = (39, 255, 0)
    BLUE = (0, 255, 255)
    YELLOW = (255, 240, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 29, 49)
    PURPLE = (229, 0, 230)
    ORANGE = (255, 105, 0)
    GREY = (128, 128, 128)
    TURQUISE = (65, 224, 208)

    class Node:
        def __init__(self, row, col, width, total_rows) -> None:
            self.row = row
            self.col = col
            self.x = row * width
            self.y = col * width
            self.color = WHITE
            self.neighbors = []
            self.width = width
            self.total_rows = total_rows
            self.queued = False
            self.visited = False
            self.prior = None

        def get_color(self):
            return self.color    

        def get_pos(self):
            return self.row, self.col

        def is_closed(self):
            return self.color == RED

        def is_open(self):
            return self.color == GREEN

        def is_barrier(self):
            return self.color == BLACK

        def is_start(self):
            return self.color == ORANGE

        def is_end(self):
            return self.color == TURQUISE

        def reset(self):
            self.color = WHITE
        
        def make_start(self):
            self.color = ORANGE

        def make_closed(self):
            self.color = RED

        def make_open(self):
            self.color = GREEN

        def make_barrier(self):
            self.color = BLACK 

        def make_end(self):
            self.color = TURQUISE        

        def make_path(self):
            self.color = PURPLE

        def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

        def update_neighbors(self, grid):
            self.neighbors = []
            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])    

            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
                self.neighbors.append(grid[self.row][self.col - 1])

        def __lt__(self, other):
            return False


    def h_fun(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def reconstruct_path(came_from, current, draw):
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()

    def astar_algorithm(draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {node: float("inf") for row in grid for node in row}
        g_score[start] = 0
        f_score = {node: float("inf") for row in grid for node in row}
        f_score[start] = h_fun(start.get_pos(), end.get_pos())

        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                reconstruct_path(came_from, end, draw)
                end.make_end()
                start.make_start()
                return True        

            for neighbor in current.neighbors:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h_fun(neighbor.get_pos(), end.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw()

            if current != start:
                current.make_closed()

        return False    

    def dijkstra_algorithm(draw, start, end):
        queue = []
        queue.append(start)
        start.queued = True
        start.distance = 0
        while queue:
            current_node = queue.pop(0)
            current_node.visited = True
            current_node.make_closed()
            start.make_start()
            if current_node == end:
                end.make_end()
                while current_node.prior != start:
                    current_node.make_path()
                    current_node = current_node.prior
                return True
            for neighbor in current_node.neighbors:
                if not neighbor.visited and not neighbor.is_barrier():
                    neighbor.prior = current_node
                    neighbor.distance = current_node.distance + 1
                    neighbor.queued = True
                    queue.append(neighbor)
            draw()
        return False

    def dfs_algorithm(draw, start, end):
        stack = [start]
        visited = set()
        while stack:
            node = stack.pop()
            if node == end:
                end.make_end()
                while node != start:
                    node.make_path()
                    node = node.prior
                return True
            if node not in visited:
                visited.add(node)
                for neighbor in node.neighbors:
                    if neighbor not in visited and not neighbor.is_barrier():
                        neighbor.prior = node
                        stack.append(neighbor)
                node.make_closed()
                start.make_start()
            draw()
        return False    

    def make_grid(rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node = Node(i, j, gap, rows)
                grid[i].append(node)

        return grid

    def draw_grid(win, rows, width):
        gap = width // rows            
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    def draw(win, grid, rows, width):
        win.fill(WHITE)
        for row in grid:
            for node in row:
                row, col = node.get_pos()
                node.draw(win)
                if col == 0 or row == 0 or col == rows - 1 or row == rows - 1:
                    node.make_barrier() 

        draw_grid(win, rows, width)
        pygame.display.update()

    def get_clicked_position(pos, rows, width):
        gap = width // rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

    def main(win, width, pfAlgorithm = 0, mazeAlgorithm = 0):
        ROWS = 50
        grid = make_grid(ROWS, width)
        start = None
        end = None
        run = True

        if mazeAlgorithm == 1:
            from mazes import maze_dfs
            maze = maze_dfs.maze
            i,j = -1, -1
            for row in maze:
                i+=1
                for tile in row:
                    j+=1
                    if tile == 'X':
                        node = grid[i][j]
                        node.make_barrier()
                j = -1 
        elif mazeAlgorithm == 2:
            from mazes import maze_kruskal
            maze = maze_kruskal.maze
            i,j = -1, -1
            for row in maze:
                i+=1
                for tile in row:
                    j+=1
                    if tile == 'X':
                        node = grid[i][j]
                        node.make_barrier()
                j = -1 
        elif mazeAlgorithm == 3:
            from mazes import maze_wilson
            maze = maze_wilson.maze
            i,j = -1, -1
            for row in maze:
                i+=1
                for tile in row:
                    j+=1
                    if tile == 'X':
                        node = grid[i][j]
                        node.make_barrier()
                j = -1 
        else: 
            maze = [['' for _ in range(50)] for _ in range(50)]

        while run:     
            for event in pygame.event.get():
                
                draw(win, grid, ROWS, width)

                if event.type == pygame.QUIT:
                    run = False     

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_position(pos, ROWS, width)
                    
                    try:
                        node = grid[row][col]
                        if not start and node != end and row != 0 and col != 0 and row != ROWS - 1 and col != ROWS - 1:
                            start = node
                            start.make_start()

                        elif not end and node != start and row != 0 and col != 0 and row != ROWS - 1 and col != ROWS - 1:
                            end = node
                            end.make_end()

                        elif node != end and node != start and row != 0 and col != 0 and row != ROWS - 1 and col != ROWS - 1:  
                            node.make_barrier()
                    except IndexError:
                        pass 

                    

                elif pygame.mouse.get_pressed()[2]:   
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_position(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None    
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                end.visited = False
                                end.queued = False
                                end.prior = None
                                if node.get_color() == RED or node.get_color() == PURPLE or node.get_color() == GREEN:
                                    node.reset()
                                    node.visited = False
                                    node.queued = False
                                    node.prior = None
                        start_timer = time.time()
                        if pfAlgorithm == 0:
                            check = dfs_algorithm(lambda: draw(win, grid, ROWS, width), start, end)
                        elif pfAlgorithm == 1:
                            check = dijkstra_algorithm(lambda: draw(win, grid, ROWS, width), start, end)
                        elif pfAlgorithm == 2:  
                            check = astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)             
                        else:
                            pass

                        if check == False:
                            messagebox.showinfo("No Solution", "There is no solution!")
                        else:    
                            end_timer = time.time() 
                            print("The time of execution of above program is :",(end_timer-start_timer) * 10**3, "ms")   
                            messagebox.showinfo("Solution Found", f"Execution time: { (end_timer-start_timer) * 10**3 } ms")

                    if event.key == pygame.K_r:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)  
                        i,j = -1, -1
                        for row in maze:
                            i+=1
                            for tile in row:
                                j+=1
                                if tile == 'X':
                                    node = grid[i][j]
                                    node.make_barrier()
                            j = -1          

        pygame.quit()                                    

    main(WIN, WIDTH, pfAlgorithm, mazeAlgorithm)    