import pygame
from queue import PriorityQueue
from tkinter import messagebox, Tk

def main_program(algorithm : int = 0):

    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Pathfinding Algorithm Visualizer")

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
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
        return abs(x1 - x2) + abs(y1 - y2)

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
        path = []
        start.visited = True
        end.visited = False
        end.queued = False
        end.prior = None
        queue.append(start)
        stop = True
        while stop:
            if len(queue) > 0:
                current_node = queue.pop(0)
                current_node.visited = True
                current_node.make_closed()
                start.make_start()
                if current_node == end:
                    end.make_end()
                    while current_node.prior != start:
                        path.append(current_node.prior)
                        current_node = current_node.prior
                    stop = False
                else:
                    for neighbor in current_node.neighbors:
                        if not neighbor.queued and not neighbor.is_barrier():
                            neighbor.queued = True
                            neighbor.make_open()
                            neighbor.prior = current_node
                            queue.append(neighbor)
                draw()              
                for i in path:
                    i.make_path()
            else:
                stop = False
                return False

    def dfs_algorithm(draw, start, end):
        visited = []
        path = set()
        visited.append(start)
        while visited:
            node = visited.pop(-1)
            path.add(node)
            node.make_closed()
            start.make_start()
            end.make_end()
            for neighbor in node.neighbors:
                if neighbor == end:
                    end.make_end()
                    for node in path:
                        if not node.is_start() and not node.is_end():
                                node.make_path()
                    visited.clear()
                    return True                      
                elif neighbor not in visited and not neighbor.is_barrier() and not neighbor.is_closed():
                    visited.append(neighbor)
                    neighbor.make_open()    
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

    def main(win, width, algorithm = 0):
        ROWS = 50
        grid = make_grid(ROWS, width)
        start = None
        end = None
        run = True

        while run:
            draw(win, grid, ROWS, width)
            for event in pygame.event.get():
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

                        if algorithm == 0:
                            check = dfs_algorithm(lambda: draw(win, grid, ROWS, width), start, end)
                        elif algorithm == 1:
                            check = dijkstra_algorithm(lambda: draw(win, grid, ROWS, width), start, end)
                        elif algorithm == 2:  
                            check = astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)             
                        else:
                            Tk().wm_withdraw()
                            messagebox.showinfo("Invalid Input","Enter correct algorithm number!")

                        if check == False:
                            Tk().wm_withdraw()
                            messagebox.showinfo("No Solution", "There is no solution!")

                    if event.key == pygame.K_r:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)        

        pygame.quit()                                    

    main(WIN, WIDTH, algorithm)    