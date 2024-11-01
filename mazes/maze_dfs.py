import random

def generate_maze(width, height):
    # Initialize the maze with walls
    maze = [['X' for _ in range(width)] for _ in range(height)]

    # Create a stack to keep track of the visited cells
    stack = []

    # Choose a random starting point and add it to the stack
    start = (random.randrange(width), random.randrange(height))
    stack.append(start)

    # Mark the starting point as open in the maze
    maze[start[1]][start[0]] = ' '

    # Define the directions (up, right, down, left)
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]

    while stack:
        current_cell = stack[-1]
        x, y = current_cell

        # Shuffle the directions to randomize the path
        random.shuffle(directions)

        # Check each direction
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the next cell is within the maze boundaries
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 'X':
                # Mark the path as open
                maze[ny][nx] = ' '
                maze[y + dy // 2][x + dx // 2] = ' '
                
                # Add the next cell to the stack
                stack.append((nx, ny))
                break
        else:
            # If no valid direction is found, backtrack
            stack.pop()

    return maze

# Example usage for a 49x49 maze
maze = generate_maze(50, 50)

if __name__ == '__main__':
# Print the maze
    for row in maze:
        print(' '.join(row))
    # print(maze)