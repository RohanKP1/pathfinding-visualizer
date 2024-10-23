import random

def generate_maze(width, height):
    # Initialize the maze with walls
    maze = [['X' for _ in range(width)] for _ in range(height)]

    # Initialize a set of unvisited cells
    unvisited_cells = set((x, y) for x in range(width) for y in range(height))

    # Choose a random starting point
    start = random.choice(list(unvisited_cells))
    unvisited_cells.remove(start)

    # Mark the starting point as open
    maze[start[1]][start[0]] = ' '

    while unvisited_cells:
        # Choose a random unvisited cell
        current_cell = random.choice(list(unvisited_cells))

        # Perform a loop-erased random walk
        path = [current_cell]

        while current_cell in unvisited_cells:
            neighbors = []

            # Check neighbors
            if current_cell[0] > 0 and (current_cell[0] - 1, current_cell[1]) not in path:
                neighbors.append((current_cell[0] - 1, current_cell[1]))
            if current_cell[0] < width - 1 and (current_cell[0] + 1, current_cell[1]) not in path:
                neighbors.append((current_cell[0] + 1, current_cell[1]))
            if current_cell[1] > 0 and (current_cell[0], current_cell[1] - 1) not in path:
                neighbors.append((current_cell[0], current_cell[1] - 1))
            if current_cell[1] < height - 1 and (current_cell[0], current_cell[1] + 1) not in path:
                neighbors.append((current_cell[0], current_cell[1] + 1))

            if not neighbors:
                break

            # Move to a random neighbor
            current_cell = random.choice(neighbors)
            path.append(current_cell)

        # Carve the path in the maze
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            maze[(y1 + y2) // 2][(x1 + x2) // 2] = ' '
            maze[y2][x2] = ' '

        # Remove the visited cells from the unvisited list
        unvisited_cells -= set(path)
    return maze

# Example usage for a 50x50 maze
maze = generate_maze(50, 50)

if __name__ == '__main__':
# Print the maze
    for row in maze:
        print(' '.join(row))
    # print(maze)
