import random

def generate_maze(width, height):
    def find_set(cell):
        if cell != disjoint_sets[cell]:
            disjoint_sets[cell] = find_set(disjoint_sets[cell])
        return disjoint_sets[cell]

    def union_sets(cell1, cell2):
        root1, root2 = find_set(cell1), find_set(cell2)
        if root1 != root2:
            disjoint_sets[root1] = root2

    # Initialize the maze with walls
    maze = [['X' for _ in range(width)] for _ in range(height)]

    # Initialize disjoint sets for each cell
    disjoint_sets = [i for i in range(width * height)]

    # Create a list of all walls in random order
    walls = [(x, y, 'h') for y in range(height) for x in range(width - 1)] + [(x, y, 'v') for x in range(width) for y in range(height - 1)]
    random.shuffle(walls)

    for wall in walls:
        x, y, orientation = wall

        if orientation == 'h':
            cell1, cell2 = y * width + x, y * width + x + 1
        else:
            cell1, cell2 = y * width + x, (y + 1) * width + x

        if find_set(cell1) != find_set(cell2):
            union_sets(cell1, cell2)

            if orientation == 'h':
                maze[y][x] = ' '
            else:
                maze[y][x] = ' '
    return maze

# Example usage for a 50x50 maze
maze = generate_maze(50, 50)

if __name__ == '__main__':
# Print the maze
    for row in maze:
        print(' '.join(row))
    # print(maze)
