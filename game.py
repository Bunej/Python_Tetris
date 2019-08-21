import pygame as pg
import random

pg.font.init()

# VARS
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..XX..',
      '.XX...',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '...X.',
      '.....']]

Z = [['.....',
      '.....',
      '.XX..',
      '..XX.',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '.X...',
      '.....']]

I = [['..X..',
      '..X..',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      'XXXX.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.XX..',
      '.XX..',
      '.....']]

J = [['.....',
      '.X...',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..XX.',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '...X.',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '.XX..',
      '.....']]

L = [['.....',
      '...X.',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '..XX.',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '.X...',
      '.....'],
     ['.....',
      '.XX..',
      '..X..',
      '..X..',
      '.....']]

T = [['.....',
      '..X..',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (150, 255, 255), (255, 255, 90), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shapes


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0)for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                k = locked_positions[(j, i)]
                grid[i][j] = k
    return grid


def convert_shape_format(shape):
    positions = []
    format_shape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def valid_space(shape, grid):
    correct_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    correct_pos = [j for x in correct_pos for j in x]  # Converting a list of list to a single list
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in correct_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text(surface, text, size, color):
    font = pg.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    # Drawing the grid
    start_x = top_left_x
    start_y = top_left_y
    for i in range(len(grid)):
        pg.draw.line(surface, (128, 128, 128), (start_x, start_y+i*block_size), (start_x+play_width,
                                                                                 start_y + i*block_size))
        for j in range(len(grid[i])):
            pg.draw.line(surface, (128, 128, 128), (start_x + j*block_size, start_y),
                         (start_x + j*block_size, start_y + play_height))


def clear_rows(grid, locked_pos):
    increment = 0
    # Deleting current row which doesn't have black blocks
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            independent = i
            for j in range(len(row)):
                try:
                    del locked_pos[(j, i)]
                except:
                    continue
    if increment > 0:
        '''
        Kinda complex way to sort a list,
        but i'm not sure how to do it easier way
        TODO: FIND A SIMPLER SOLUTION TO THIS IF POSSIBLE
        '''
        for key in sorted(list(locked_pos), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < independent:
                new_key = (x, y + increment)
                locked_pos[new_key] = locked_pos.pop(key)
    return increment


def draw_next_shape(shape, surface):
    font = pg.font.SysFont('Arial', 30)
    label = font.render('Next Block', 1, (255, 255, 255))
    shape_x = top_left_x + play_width + 50  # Position x of next block in a window
    shape_y = top_left_y + play_height/2 - 100  # Position y of next block in a window
    shape_format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                pg.draw.rect(surface, shape.color, (shape_x + j*block_size, shape_y + i*block_size,
                                                    block_size, block_size), 0)
    surface.blit(label, (shape_x + 10, shape_y - 30))


def draw_window(surface, grid, score=0, high_score=0):
    surface.fill((0, 0, 0))  # Color of a window
    pg.font.init()
    font = pg.font.SysFont('Arial', 30)
    label = font.render('Tetris', 1, (255, 255, 255))
    # Drawing label on screen
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    # current score
    label = font.render('High Score: ' + str(high_score), 1, (255, 255, 255))
    score_x = top_left_x - 250  # Position x of score
    score_y = top_left_y + 200  # Position y of score
    surface.blit(label, (score_x + 30, score_y + 150))
    # last score
    font = pg.font.SysFont('Arial', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    score_x = top_left_x + play_width + 50  # Position x of score
    score_y = top_left_y + play_height / 2 - 100  # Position y of score
    surface.blit(label, (score_x + 30, score_y + 150))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pg.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y +
                                               i*block_size, block_size, block_size), 0)
    pg.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)


def update_score(end_score):
    score = best_score()
    with open('score.txt', 'w') as f:
        if int(score) > end_score:
            f.write(str(score))
        else:
            f.write(str(end_score))


def best_score():
    with open('score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def main(win):
    locked_positions = {}
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pg.time.Clock()
    fall_time = 0
    fall_speed = 0.3
    fall_level = 0
    score = 0
    high_score = best_score()
    key_hold = pg.key.get_pressed()
    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        fall_level += clock.get_rawtime()
        clock.tick()
        # Setting up a faster speed by the time goes on
        if fall_level/1000 > 6:
            fall_level = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pg.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pg.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pg.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color  # {(1, 2):(0, 255, 0)}
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        draw_window(win, grid, score, int(high_score))
        draw_next_shape(next_piece, win)
        pg.display.update()
        if check_lost(locked_positions):
            draw_text(win, 'YOU LOST!', 100, (255, 255, 255))
            pg.display.update()
            pg.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text(win, 'Press Key to Play', 100, (255, 255, 255))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                main(win)
    pg.display.quit()


win = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Tetris')
# start game
main_menu(win)

