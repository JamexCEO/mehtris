import pygame, sys, random

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Colors:
    black = (0, 0, 0)                           # Copied from grid.py
    white = (255, 255, 255)

    @classmethod
    def get_cell_colors(cls):
        return [cls.black] + [cls.white] * 7


class Block:                                    # parent class for all other block shapes
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0                     # Add offset to move the block (if row offset is 1 then the block will be one row lower)
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles

    def rotate(self):                           # to rotate the block
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):      # For when the rotation state = 3 and we need to reset it to zero again
            self.rotation_state = 0

    def undo_rotation(self):                    # For when the rotation will cause the block to go out of the window, so we need to undo it
        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.cells) - 1   # For when the rotation state = 0 and we need to decrease it again

    def draw(self, window, offset_x, offset_y):
        tiles = self.get_cell_positions()       # retrieves list of positions for the current state of the block
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(window, self.colors[self.id], tile_rect)


# create the necessary code for each block type

class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)                         # Offset so each block spawns from the middle of the grid instead of the top left corner

class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)                        # Extra offset because otherwise this block will spawn one row down instead of at the top

class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0, 4)                         # Extra offset because otherwise this block will spawn one column to the left instead of in the middle

class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)


class Grid:
    def __init__(self):
        self.num_rows = 20                      # Number of rows
        self.num_cols = 10                      # Number of columns
        self.cell_size = 30                     # Size of each "cell" in the grid
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]   # Create a list of lists to reflect the value of each cell
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):           # Using this to ensure the piece does not go outside the border of the game
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False 

    def get_cell_colors(self):

        black = (0, 0, 0)
        white = (255, 255, 255)

        return [black, white]

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):                 # Check if a row is full to clear it
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):     # Moves the above row down when the below row has been cleared
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):                  # Checks all rows in grid to see if any are completed
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def reset(self):                            # to start a new game
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, window):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column] # Iterates through each cell in the grid
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(window, self.colors[cell_value], cell_rect)


class Grid:
    def __init__(self):
        self.num_rows = 20                      # Number of rows
        self.num_cols = 10                      # Number of columns
        self.cell_size = 30                     # Size of each "cell" in the grid
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]   # Create a list of lists to reflect the value of each cell
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):           # Using this to ensure the piece does not go outside the border of the game
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False 

    def get_cell_colors(self):

        black = (0, 0, 0)
        white = (255, 255, 255)

        return [black, white]

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):                 # Check if a row is full to clear it
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):     # Moves the above row down when the below row has been cleared
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):                  # Checks all rows in grid to see if any are completed
        completed = 0
        for row in range(self.num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def reset(self):                            # to start a new game
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, window):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column] # Iterates through each cell in the grid
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(window, self.colors[cell_value], cell_rect)


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100                   # 100 points for every line cleared
        elif lines_cleared == 2:
            self.score += 300                   # 300 points for every double line cleared
        elif lines_cleared == 3:
            self.score += 500                   # 500 points for every triple line cleared
        elif lines_cleared == 4:
            self.score += 1000                  # 1000 points for every four lines cleared
        self.score += move_down_points

    def get_random_block(self):                 # Ensure that each block appears at least once before a block appears twice
        if len(self.blocks) == 0:               # Refill the list once each block has appeared at least once to continue the cycle
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)      # Spawn a random block
        self.blocks.remove(block)               # Remove the block from the list once it has appeared
        return block

    def move_left(self):
        self.current_block.move(0, -1)          # moves the block to the left
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)       # moves the block to the right if it goes out of the boundary

    def move_right(self):
        self.current_block.move(0, 1)           # moves the block to the right
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)      # moves the block to the left if it goes out of the boundary

    def move_down(self):
        self.current_block.move(1, 0)           # moves the block down
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)      # moves the block up if it goes out of the boundary
            self.lock_block()                   # block can no longer move

    def lock_block(self):                       # stops the ability to move the block once it has hit the bottom
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block    # the next block becomes the current block after our current block has hit the bottom
        self.next_block = self.get_random_block() # the new next block will be generated randomly
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:          # for when the new block cannot spawn, the game should end
            self.game_over = True

    def reset(self):                            # for when we need to start a new game
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):                           # rotation
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()  # undo rotation

    def block_inside(self):                     # checks if the block is inside the boundary or not
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, window):
        self.grid.draw(window)
        self.current_block.draw(window, 11, 11)
        if self.next_block.id == 3:
            self.next_block.draw(window, 255, 290)  # Different offset to ensure the OBlock centres properly
        elif self.next_block.id == 4:
            self.next_block.draw(window, 255, 280)  # Different offset to ensure the IBlock centres properly
        else:
            self.next_block.draw(window, 270, 270)  # All other blocks


pygame.init()
# dark_blue = (44, 44, 127)                     # Dark blue for game background, may replace with black in future

title_font = pygame.font.Font(None, 40)         # Font for the titles "Score", etc
score_surface = title_font.render("score", True, Colors.black)      # Add the title
next_surface = title_font.render("next", True, Colors.black)
game_over_surface = title_font.render("game over lol", True, Colors.black)

score_rect = pygame.Rect(320, 55, 170, 60)      # Add a rectangle to display the score inside
next_rect = pygame.Rect(320, 215, 170, 180)     # Add a rectangle to display the next block inside

window = pygame.display.set_mode((500, 620))    # Creates the window and sets the size of the window to 300x600px
pygame.display.set_caption("mehtris")           # Name the window

clock = pygame.time.Clock()

game = Game()

# game_grid = Grid()                            # Testing purposes only

# game_grid.grid[0][0] = 1                      # Testing the grid filling with hard-coded values
# game_grid.grid[3][5] = 1                      # Testing the grid filling with hard-coded values
# game_grid.grid[17][8] = 1                     # Testing the grid filling with hard-coded values

# block = IBlock()                              # Testing if each block appears properly
# block.move(4, 3)                              # Testing if the block can move properly based on row_offset and column_offset

# game_grid.print_grid()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)         # creates a timer that will trigger GAME_UPDATE every 200 ms, updating the position of the block every 200 ms


while True:
    for event in pygame.event.get():            # Gets all event Pygame recognises and puts into a list
        if event.type == pygame.QUIT:           
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over == True:  # Use R to restart the game
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:  # Use ← to move the block to the left
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False: # Use → to move the block to the right
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:  # Use ↓ to move the block down
                game.move_down()
                game.update_score(0, 1)         # Update score by 1 whenever the user presses the block down
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:           # ensures the block moves down every time GAME_UPDATE updates
            game.move_down()

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    window.fill(Colors.white)                        # Window background colour
    window.blit(score_surface, (365, 20, 50, 50))
    window.blit(next_surface, (375, 180, 50, 50))
    if game.game_over == True:
        window.blit(game_over_surface, (320, 450, 50, 50))      # Draw the game over message

    pygame.draw.rect(window, Colors.black, score_rect, 0, 10)   # Draw the score rectangle
    window.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    pygame.draw.rect(window, Colors.black, next_rect, 0, 10)    # Draw the next block rectangle
    game.draw(window)

    pygame.display.update()
    clock.tick(60)                              # Set FPS to 60