#!/usr/bin/env python
#
# Author: Griffin Leonard
# Title: tic tac toe plus

# LOAD MODULES
try:
    import sys
    import pygame
except Exception as exc:
    print("ERROR: couldn't load modules.",exc)
    sys.exit()


# GENERAL SETUP
pygame.init()
clock = pygame.time.Clock()

# Initialise window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
SIDE_MARGIN = 200
TILE_SIZE = 64
PIECE_SIZES = 6
TEAMS = ['blue','red']

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('tic-tac-toe+') 

# Get images
img_pieces = {}
for team in TEAMS:
    img_pieces[team] = []
    for x in range(PIECE_SIZES):
        img = pygame.image.load(f'img/pieces/{team}{x}.png').convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_pieces[team].append(img)

grid_img = pygame.image.load('img/grid.png').convert_alpha()
grid_img = pygame.transform.scale(grid_img, (grid_img.get_width()*2, grid_img.get_height()*2))
select_img = pygame.image.load('img/select.png').convert_alpha()
select_img = pygame.transform.scale(select_img, (TILE_SIZE*2, TILE_SIZE*2))

GRID_Y = SCREEN_HEIGHT/2 - grid_img.get_height()/2
GRID_X = SCREEN_WIDTH/2 - grid_img.get_width()/2

# For text
FONT = pygame.font.SysFont('Futura', 24)
COLORS = {'blue': (91, 110, 225), 'red': (172, 50, 50)}
WHITE = (255, 255, 255)
BLACK = (34, 32, 52)
def blit_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# HELPER FUNCTIONS AND CLASSES
def restart_button():
    restart_rect = pygame.Rect(GRID_X+grid_img.get_width()/3-20, GRID_Y/2-10, 180, 40)
    pygame.draw.rect(screen, BLACK, restart_rect)
    blit_text('New Game', FONT, WHITE, GRID_X+grid_img.get_width()/3+10, GRID_Y/2-5)
    
    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1:    
        if restart_rect.collidepoint(pos[0],pos[1]):
            return True
    return False

class Piece():
    def __init__(self, size, team):
        self.size = size
        self.team = team
        self.img = img_pieces[team][size]
        self.used = False

class TikTakToe():
    def __init__(self):
        self.game_board = [[0,0,0],
                           [0,0,0],
                           [0,0,0]]

        self.pieces = {}
        for team in TEAMS:
            self.pieces[team] = []
            for i,img in enumerate(img_pieces[team]):
                p = Piece(i,team)
                self.pieces[team].append(p)

        self.selected = self.pieces[TEAMS[0]][0]
        self.turn = TEAMS[0]
        self.winner = False # False if in progess, True if tie game, or str (color of winning team)

    def update(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:    
            if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
                # play move on game board
                if pos[0] >= GRID_X and pos[0] < SCREEN_WIDTH-GRID_X and pos[1] >= GRID_Y and pos[1] <= SCREEN_HEIGHT-GRID_Y:
                    x = int((pos[0]-GRID_X) // (grid_img.get_width()/3))
                    y = int((pos[1]-GRID_Y) // (grid_img.get_height()/3))

                    # place piece on game board
                    if self.selected != None and self.can_place(x, y):
                        self.game_board[y][x] = self.selected
                        self.selected.used = True
                        self.selected = None

                        # update whose turn it is
                        if self.turn == TEAMS[0]: self.turn = TEAMS[1]
                        else: self.turn = TEAMS[0]

                # change selected piece
                else:
                    p = round(pos[1] / (SCREEN_HEIGHT//(PIECE_SIZES+1)))-1
                    if p in range(PIECE_SIZES):
                        if pos[0] < SIDE_MARGIN: team = TEAMS[0]
                        else: team = TEAMS[1]
                
                        if self.turn == team and not self.pieces[team][p].used:
                            self.selected = self.pieces[team][p]

    def game_over(self):
        ''' determines if pieces can be played. returns winner and updates self.winner
        returns:
            False if game in progress
            str, color of wining team
            True if the game is a tie
        '''
        # check for winner
        winner = self.three_in_a_row()
        if winner: 
            self.winner = winner
            return winner

        if not self.pieces_left(): 
            self.winner = True
            return True # if player has no more pieces (tie)
        if not self.board_filled(): 
            self.winner = False
            return False # if the board has empty spaces (in progress)
        largest_piece = -1
        for p in self.pieces[self.turn]:
            if not p.used and p.size > largest_piece:
                largest_piece = p.size
        for row in self.game_board:
            for p in row:
                if p.team != self.turn and p.size < largest_piece: 
                    self.winner = False
                    return False # if player can place piece on top of oppoent's smaller piece
        self.winner = True
        return True # if player has pieces left but no legal moves

    def three_in_a_row(self):
        ''' determines if either player has 3 in a row
        returns:
            False if neither player has won
            str, color of wining team
        '''
        for i in range(3):
            #check rows
            if self.game_board[i][0] != 0:
                t = self.game_board[i][0].team
                win = True
                for p in self.game_board[i]:
                    if p == 0 or p.team != t: 
                        win = False
                if win: return t

            #check cols
            if self.game_board[0][i] != 0:
                t = self.game_board[0][i].team
                win = True
                for j in range(3):
                    if self.game_board[j][i] == 0 or self.game_board[j][i].team != t: 
                        win = False
                if win: return t

        #check diagonals 
        if self.game_board[0][0] != 0:
            t = self.game_board[0][0].team
            if self.game_board[1][1] != 0 and self.game_board[2][2] != 0:
                if self.game_board[1][1].team == t and self.game_board[2][2].team == t: return t
        if self.game_board[2][0] != 0:
            t = self.game_board[2][0].team
            if self.game_board[1][1] != 0 and self.game_board[0][2] != 0:
                if self.game_board[1][1].team == t and self.game_board[0][2].team == t: return t

        return False

    def board_filled(self):
        ''' determines whether the board has empty spaces 
        returns:
            True if the board has a piece in every square
            False if the board has empty squares
        '''
        for row in self.game_board:
            for p in row: 
                if p == 0: return False
        return True

    def pieces_left(self):
        ''' determines if a player is out of pieces. doesn't account for whether pieces can be legally played
        returns:
            True if the player whose turn it is has pieces unused
            False if the player whose turn it is has used all thier pieces 
        '''
        for p in self.pieces[self.turn]:
            if not p.used: return True
        return False

    def can_place(self, x, y):
        ''' determines if the selected piece can be legally played in a clicked position
        returns:
            True if the move is legal
            False if the move is illegal
        '''
        if self.selected == None: return False
        if self.game_board[y][x] == 0: return True
        if self.game_board[y][x].team != self.selected.team and self.game_board[y][x].size < self.selected.size: return True
        return False

    def draw(self):
        screen.fill(WHITE)
        self.draw_grid()
        self.draw_pieces()
        self.display_turn()

    def draw_grid(self):
        screen.blit(grid_img, ((SCREEN_WIDTH-grid_img.get_width())//2, (SCREEN_HEIGHT-grid_img.get_height())//2))
        for y,row in enumerate(self.game_board):
            for x,piece in enumerate(row):
                if piece != 0:
                    screen.blit(piece.img, (GRID_X + x*grid_img.get_width()/3 + grid_img.get_width()/12, GRID_Y + y*grid_img.get_height()/3 + grid_img.get_height()/12))

    def draw_pieces(self):
        for team in TEAMS:
            for piece in self.pieces[team]:
                if not piece.used:
                    if team == TEAMS[0]:
                        loc = (SIDE_MARGIN//2 - TILE_SIZE//2, SCREEN_HEIGHT//(PIECE_SIZES+1)*(piece.size+1) - TILE_SIZE//2)
                        if self.selected == piece:
                            screen.blit(select_img, (loc[0]-TILE_SIZE//2,loc[1]-TILE_SIZE//2))
                        screen.blit(piece.img, loc)
                    else:
                        loc = (SCREEN_WIDTH - SIDE_MARGIN//2 - TILE_SIZE//2, SCREEN_HEIGHT//(PIECE_SIZES+1)*(piece.size+1) - TILE_SIZE//2)
                        if self.selected == piece:
                            screen.blit(select_img, (loc[0]-TILE_SIZE//2,loc[1]-TILE_SIZE//2))
                        screen.blit(piece.img, loc)    

    def display_winner(self):
        if type(self.winner) == str: 
            blit_text(f'{self.winner} team wins!', FONT, COLORS[self.winner], SIDE_MARGIN+grid_img.get_width()/3, SCREEN_HEIGHT-GRID_Y/2)
        elif self.winner: 
            blit_text('tie game!', FONT, BLACK, SIDE_MARGIN+grid_img.get_width()/3+10, SCREEN_HEIGHT-GRID_Y/2)
  
    def display_turn(self):
        if not self.winner:
            blit_text(f'Turn: {self.turn}', FONT, COLORS[self.turn], SIDE_MARGIN+grid_img.get_width()/3+10, SCREEN_HEIGHT-GRID_Y/2)

# MAIN GAME LOOP
game = TikTakToe()
while 1:
    clock.tick(60) # Update clock

    game.draw() # Draw objects on screen
    if game.winner: game.display_winner()
    if not game.game_over():
        game.update()
    
    if restart_button(): # Draw and handle presses of the Start Over button
        game = TikTakToe()

    # Quit game 
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()

    pygame.display.update() # Update screen 