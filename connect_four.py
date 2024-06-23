"""""
Name: Oween Cesar Barranzuela Carrasco, Student Number = 22302013
Connect-Four in Python
Solution for: Programming 2, Exercise Performance Task 1

Recommendations:
You may need to install separately numpy or pgame too.
After running the file, you should write your input in the console: 
   - two_players : you will get the first turn in a two-players game.
   - random : you may get the first or second turn against your oponent. Since it is using random, it can be that one 
   of the players receive the same turn again.
   - ai: you will get the first turn against AI
After you win or lose, there will be a message in the console, write yes to continue or not to exit 

IMPORTANT REMARKS:
!! Chat gpt was used to debbuging specially to deal with the two players-random-ai modes.
!! You can find the used sources with their links in this file. 
!!  When playing against AI, the evaluation score will be displayed in the console, it may take up to 30 seconds or less than 
one minute for AI to give its decision (In Pycharm and VS took less than the python IDLE ). One of its characteristics is that it will try to block your wins so I would encourage the user
to try to make a win to see this AI's functionality. 

!! When the pygame window is displayed the user turn will be determined by a circle in the bottom-side. The idea was that the user
can move and select the column when clicking the circle from the bottom-side. However, the user can select an input by clicking also in the 
desired column (due to a bug,i couldnt solve this issue)

!! When quiting, the code kept having a "pygame.error: display Surface quit", I couldnt unfortunately fix this.


"""

import numpy as np
import pygame
import sys
import math
import random


#colors 
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

empty = 0

columns = 7
rows = 6

def create_board():
    board = np.zeros((6, 7))
    return np.flip(board, 0)

def correct_position(board, y_axis):
    return board[rows - 1][y_axis] == 0

def selecting_rows(board, rows, y_axis, value):
    if board[5][y_axis] != 0:  # Check if the top row of the column is already filled
        print("Column is already full")
        return False

    for row in range(rows):
        if board[row][y_axis] == 0:
            board[row][y_axis] = value
            return True
    return False


# IMPORTANT: The following functions (draw_board() and winner() where done following a youtube tutorial (https://www.youtube.com/watch?v=SDz3P_Ctm7U))
# for draw_board(), i used too the python (https://www.amazon.de/-/en/Eric-Matthes/dp/1593279280)crash course - projects (alien invasion project )

def draw_board(screen, board):
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, RED, (c * 100, r * 100 + 100, 100, 100))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (c * 100 + 50, r * 100 + 150), 45)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, GREEN, (c * 100 + 50, r * 100 + 150), 45)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE, (c * 100 + 50, r * 100 + 150), 45)
    pygame.display.update()

def winner(board, value):
    # Check for horizontal wins
    for c in range(columns - 3):
        for r in range(rows):
            if board[r][c] == value and board[r][c + 1] == value and board[r][c + 2] == value and board[r][c + 3] == value:
                return True
    # Check for vertical wins
    for c in range(columns):
        for r in range(rows - 3):
            if board[r][c] == value and board[r + 1][c] == value and board[r + 2][c] == value and board[r + 3][c] == value:
                return True
    # Check for diagonal wins
    for c in range(columns - 3):
        for r in range(rows - 3):
            if board[r][c] == value and board[r + 1][c + 1] == value and board[r + 2][c + 2] == value and board[r + 3][c + 3] == value:
                return True
    for c in range(columns - 3):
        for r in range(3, rows):
            if board[r][c] == value and board[r - 1][c + 1] == value and board[r - 2][c + 2] == value and board[r - 3][c + 3] == value:
                return True

def scores(board, value):
    points = 0
    for r in range(rows):
        array_rows = [int(i) for i in list(board[r, :])]
        for c in range(columns - 3):
            calculator = array_rows[c:c + 4]
            if calculator.count(value) == 4:
                points += 100
            elif calculator.count(value) == 3 and calculator.count(empty) == 1:
                points += 10

    # Vertical
    for c in range(columns):
        array_col = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            calculator = array_col[r:r + 4]
            if calculator.count(value) == 4:
                points += 100
            elif calculator.count(value) == 3 and calculator.count(empty) == 1:
                points += 10

    # Diagonals
    for r in range(rows - 3):
        for c in range(columns - 3):
            calculator = [board[r + 3 - i][c + 3] for i in range(4)]
            if calculator.count(value) == 4:
                points += 100
            elif calculator.count(value) == 3 and calculator.count(empty) == 1:
                points += 10

    for r in range(rows - 3):
        for c in range(columns - 3):
            calculator = [board[r + 3 - i][c] for i in range(4)]
            if calculator.count(value) == 4:
                points += 100
            elif calculator.count(value) == 3 and calculator.count(empty) == 1:
                points += 10

    return points

def locations(board):
    locations_list = []
    for col in range(columns):
        if correct_position(board, col):
            locations_list.append(col)
    return locations_list

def evaluate_board(board):
    score = 0
    score += scores(board, 1)
    score -= scores(board, 2)
    return score

def good_move(board, value):
    locations_list = locations(board)
    top_score = -1000
    top_col = random.choice(locations_list)
    for col in locations_list:
        temporal_board = board.copy()
        if selecting_rows(temporal_board, rows, col, value):
            points = scores(temporal_board, value)
            if points > top_score:
                top_score = points
                top_col = col
    return top_col

#for the implementation of the minimax algorithm this source was followed: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/

def minimax(board, depth, maximizing_player):
    if depth == 0 or winner(board, 1) or winner(board, 2):
        print("Evaluated board:")
        print(board)
        print("Evaluation score:", evaluate_board(board))
        return None, evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in locations(board):
            temp_board = board.copy()
            selecting_rows(temp_board, rows, move, 1)
            _, eval_score = minimax(temp_board, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return best_move, max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in locations(board):
            temp_board = board.copy()
            selecting_rows(temp_board, rows, move, 2)
            _, eval_score = minimax(temp_board, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return best_move, min_eval

def ai_move(board):
    move, _ = minimax(board, 4, True) 
    if move is not None:
        selecting_rows(board, rows, move, 1)

def human_move(board, y_axis):
    if correct_position(board, y_axis):
        selecting_rows(board, rows, y_axis, 2)






def play_game(mode):
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Connect Four - Programming II -  THD")
    board = create_board()
    pygame.display.update()
    first_move = 0
    mytext = pygame.font.SysFont("monospace", 75)
    selected_option = False
    AI_PLAYER = 1
    HUMAN_PLAYER = 2
    first_move_random = random.randint(0,1)



#every mode represent the selection of the user

    while True:  # Loop for replaying the game
        game_over = False  # Reset game_over flag for each new game
        while not game_over:
            if mode == "two_players":
                draw_board(screen, board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        if selected_option == False:
                            pygame.draw.rect(screen, BLACK, (0, 700, 700, 100))
                            posx = event.pos[0]
                            if first_move % 2 == 0:
                                pygame.draw.circle(screen, GREEN, (posx, 750), 45)
                            else:
                                pygame.draw.circle(screen, BLUE, (posx, 750), 45)
                            pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if selected_option == False:
                            if 30 <= event.pos[0] <= 750:
                                if first_move % 2 == 0:
                                    posx = event.pos[0]
                                    y_axis = int(math.floor((posx) / 100))
                                    if correct_position(board, y_axis):
                                        selecting_rows(board, rows, y_axis, 1)
                                        if winner(board, 1):
                                            print("congrats Player number 1")
                                            notification = mytext.render(
                                                "Player 1 wins", 1, GREEN)
                                            screen.blit(notification, (40, 10))
                                            #game_over = True
                                            pygame.display.update()
                                            pygame.time.wait(1000)
                                            pygame.quit()                                            
                                            message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                                            if message == "yes":
                                                return play_game("two_players")
                                            else:
                                                print("thanks for playing!")

                                            
                                else:
                                    posx = event.pos[0]  # between 0 and 600
                                    y_axis = int(math.floor((posx) / 100))
                                    if correct_position(board, y_axis):
                                        selecting_rows(board, rows, y_axis, 2)
                                        if winner(board, 2):
                                            print("player 2 wins")
                                            notification = mytext.render(
                                                "Player 2 wins", 1, BLUE)
                                            screen.blit(notification, (40, 10))
                                            #game_over = True 
                                            pygame.display.update()
                                            pygame.time.wait(2000)
                                            pygame.quit()
                                            message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                                            if message == "yes":
                                                return play_game("two_players")
                                            else:
                                                 print("thanks for playing!")
                                            

                                            
                                first_move += 1
                                draw_board(screen, board)
            elif mode == "random":
                draw_board(screen, board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        if selected_option == False:
                            pygame.draw.rect(screen, BLACK, (0, 700, 700, 100))
                            posx = event.pos[0]
                            if first_move_random % 2 == 0:
                                pygame.draw.circle(screen, GREEN, (posx, 750), 45)
                            else:
                                pygame.draw.circle(screen, BLUE, (posx, 750), 45)
                            pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if selected_option == False:
                            if 30 <= event.pos[0] <= 750:
                                if first_move_random % 2  == 0:
                                    posx = event.pos[0]
                                    y_axis = int(math.floor((posx) / 100))
                                    if correct_position(board, y_axis):
                                        selecting_rows(board, rows, y_axis, 1)
                                        if winner(board, 1):
                                            print("congrats Player number 1")
                                            notification = mytext.render(
                                                "Player 1 wins", 1, GREEN)
                                            screen.blit(notification, (40, 10))
                                            #game_over = True
                                            pygame.display.update()
                                            pygame.time.wait(1000)
                                            pygame.quit()                                            
                                            message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                                            if message == "yes":
                                                return play_game("random")
                                            else:
                                                print("thanks for playing!")

                                            
                                else:
                                    posx = event.pos[0]  # between 0 and 600
                                    y_axis = int(math.floor((posx) / 100))
                                    if correct_position(board, y_axis):
                                        selecting_rows(board, rows, y_axis, 2)
                                        if winner(board, 2):
                                            print("player 2 wins")
                                            notification = mytext.render(
                                                "Player 2 wins", 1, BLUE)
                                            screen.blit(notification, (40, 10))
                                            #game_over = True 
                                            pygame.display.update()
                                            pygame.time.wait(2000)
                                            pygame.quit()
                                            message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                                            if message == "yes":
                                                return play_game("random")
                                            else:
                                                print("thanks for playing!")
                                            

                                            
                                first_move_random += 1
                                draw_board(screen, board)

            elif mode =="ai":
                draw_board(screen, board)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        if selected_option == False:
                            pygame.draw.rect(screen, BLACK, (0, 700, 700, 100))
                            posx = event.pos[0]
                            if first_move % 2 == 0:
                                pygame.draw.circle(screen, BLUE, (posx, 750), 45)
                            else:
                                pygame.draw.circle(screen, BLUE, (posx, 750), 45)
                            pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        if selected_option == False:
                            if 30 <= event.pos[0] <= 750:
                                if first_move % 2  == 0:
                                    posx = event.pos[0]
                                    y_axis = int(math.floor((posx) / 100))
                                    if correct_position(board, y_axis):
                                        human_move(board, y_axis)
                                        if winner(board, HUMAN_PLAYER):
                                            print("congrats, you win against AI")
                                            notification = mytext.render(
                                                "You are the winner", 1, GREEN)
                                            screen.blit(notification, (40, 10))
                                            #game_over = True
                                            pygame.display.update()
                                            pygame.time.wait(1000)
                                            pygame.quit()                                            
                                            message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                                            if message == "yes":
                                                return play_game("ai")
                                            else:
                                                print("thanks for playing!")
                                        first_move +=1
                                        draw_board(screen, board)
                if selected_option == False and not game_over and first_move== AI_PLAYER:
                    ai_move(board)
                    if winner(board, AI_PLAYER):
                        print("YOU LOST TO AI!!!")
                        notification = mytext.render("    AI wins", 1, GREEN)
                        screen.blit(notification, (40, 10))
                        #game_over = True
                        pygame.display.update()
                        pygame.time.wait(1000)
                        pygame.quit()                                            
                        message = input("Hey!!! Would you like to continue playing? choose : yes or not :")
                        if message == "yes":
                            return play_game("ai")
                        else:
                            print("thanks for playing!")
                    first_move -=1
                    draw_board(screen, board)


                               
                                    
                

if __name__ == "__main__":
    mode = input("Welcome to Connect-Four! Choose mode (two_players/random/ai): ").lower()
    if mode in ["two_players", "random", "ai"]:
        play_game(mode)
    else:
        print("Invalid mode. Please choose from: two_player, random, ai.")




    
