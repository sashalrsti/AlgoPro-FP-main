import pygame #Used for game development
import sys #For system-related functions like exiting the game
import json #For handling high score storage in a JSON file
import os #For file path and existence checks
from game import Game #A custom class managing game logic
from colors import Colors #A custom module defining color constants

pygame.init()

#Loads a custom font 
title_font = pygame.font.Font("Early GameBoy.ttf", 13)
#Renders text surfaces
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
hold_surface = title_font.render("Hold", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
game_over1_surface = title_font.render("PRESS ANY KEY", True, Colors.white)

#Difficulty selection text surfaces rendered for the difficulty selection screen
easy_surface = title_font.render("Easy: Press 1", True, Colors.white)
normal_surface = title_font.render("Normal: Press 2", True, Colors.white)
hard_surface = title_font.render("Hard: Press 3", True, Colors.white)
select_difficulty_surface = title_font.render("Select Difficulty:", True, Colors.white)

#Defines rectangular areas for displaying score, next block, and hold block previews
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 190, 170, 180)
hold_rect = pygame.Rect(320, 430, 170, 180)

#Creates the main game window (500x620) and sets the window title to "Walmart Tetris"
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Walmart Tetris")

#Creates a clock object to control the game's frame rate
clock = pygame.time.Clock()

#Defines game states: DIFFICULTY_SELECT, PLAYING, and NAME_INPUT
#Initializes the game state to difficulty selection.
DIFFICULTY_SELECT = 0
PLAYING = 1
NAME_INPUT = 2
game_state = DIFFICULTY_SELECT


#Loads high scores from a JSON file if it exists; otherwise, returns an empty list
def load_high_scores():
    if os.path.exists('highscores.json'):
        with open('highscores.json', 'r') as f:
            return json.load(f)
    return []
#Saves high scores to a JSON file
def save_high_scores(scores):
    with open('highscores.json', 'w') as f:
        json.dump(scores, f)
#Checks if a score qualifies as a high score, ensuring only the top 3 scores are kept
def is_high_score(score, high_scores):
    if len(high_scores) < 3:
        return True
    return score > min(score_entry['score'] for score_entry in high_scores)

#Loads the current high scores at the start of the game
high_scores = load_high_scores()

#Handles name input for high scores
#current_name: Stores the player's input
#name_input_prompt: Instruction for name input
current_name = ""
name_input_prompt = title_font.render("Enter your name 5 chars:", True, Colors.white)
name_input_surface = None

# Game speed multipliers
EASY_SPEED = 2
NORMAL_SPEED = 1
HARD_SPEED = 0.5

#Defines score multipliers for different difficulties
EASY_SCORE_MULTIPLIER = 1
NORMAL_SCORE_MULTIPLIER = 1
HARD_SCORE_MULTIPLIER = 1
current_score_multiplier = NORMAL_SCORE_MULTIPLIER

current_speed = NORMAL_SPEED

game = Game()

#Load background image
background_image = pygame.image.load("./assets/sprites/bg.png")
#Calculate grid dimensions
grid_width = game.grid.num_cols * game.grid.cell_size
grid_height = game.grid.num_rows * game.grid.cell_size
#Scale background to fit only the grid area
background_image = pygame.transform.scale(background_image, (grid_width, grid_height))

#Create overlay surface for grid area only
overlay = pygame.Surface((grid_width, grid_height))
overlay.fill((0, 0, 0))  #Black overlay
overlay.set_alpha(128)    #50% transparent

#Custom game event (GAME_UPDATE) triggers periodic updates based on game speed
GAME_UPDATE = pygame.USEREVENT
base_speed = 250
pygame.time.set_timer(GAME_UPDATE, int(base_speed * current_speed))

#Tracks continuous movement states for left, right, and down keys
moving_left = False
moving_right = False
moving_down = False

#Defines timers for smooth, continuous movement
down_movement_timer = 0
down_movement_interval = 100

left_movement_timer = 0
left_movement_interval = 100

right_movement_timer = 0
right_movement_interval = 100

#Main loop that processes events and updates the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #Handles difficulty selection
        if game_state == DIFFICULTY_SELECT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    current_speed = EASY_SPEED
                    current_score_multiplier = EASY_SCORE_MULTIPLIER
                    pygame.time.set_timer(GAME_UPDATE, int(base_speed * current_speed))
                    game.reset()
                    game.game_over = False
                    game_state = PLAYING
                elif event.key == pygame.K_2:
                    current_speed = NORMAL_SPEED
                    current_score_multiplier = NORMAL_SCORE_MULTIPLIER
                    pygame.time.set_timer(GAME_UPDATE, int(base_speed * current_speed))
                    game.reset()
                    game.game_over = False
                    game_state = PLAYING
                elif event.key == pygame.K_3:
                    current_speed = HARD_SPEED
                    current_score_multiplier = HARD_SCORE_MULTIPLIER
                    pygame.time.set_timer(GAME_UPDATE, int(base_speed * current_speed))
                    game.reset()
                    game.game_over = False
                    game_state = PLAYING

        #Handles name input for high scores
        elif game_state == NAME_INPUT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(current_name) > 0:
                    #Add score to high scores
                    high_scores.append({'name': current_name, 'score': int(game.score * current_score_multiplier)})
                    #Sort and keep top 3
                    high_scores.sort(key=lambda x: x['score'], reverse=True)
                    high_scores = high_scores[:3]
                    #Save to file
                    save_high_scores(high_scores)
                    # Reset game and go back to difficulty select
                    current_name = ""
                    game.reset()
                    game_state = DIFFICULTY_SELECT
                elif event.key == pygame.K_BACKSPACE:
                    current_name = current_name[:-1]
                elif len(current_name) < 5 and event.unicode.isalnum():
                    current_name += event.unicode.upper()

        #Processes player inputs like moving, rotating, or holding blocks  
        #Updates the game state based on inputs and the GAME_UPDATE event          
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if is_high_score(int(game.score * current_score_multiplier), high_scores):
                        game_state = NAME_INPUT
                    else:
                        game.reset()
                        game.game_over = False
                        game_state = DIFFICULTY_SELECT
                    continue
                if event.key == pygame.K_LEFT:
                    moving_left = True
                    left_movement_timer = left_movement_interval
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                    right_movement_timer = right_movement_interval
                if event.key == pygame.K_DOWN:
                    moving_down = True
                    down_movement_timer = down_movement_interval
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
                if event.key == pygame.K_LSHIFT and not game.game_over:  # Changed to Left Shift key
                    game.hold_current_block()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_DOWN:
                    moving_down = False
            if event.type == GAME_UPDATE and not game.game_over:
                game.move_down()

    difficulty_bg_image = pygame.image.load('./assets/sprites/bg.png')
    difficulty_bg_image = pygame.transform.scale(difficulty_bg_image, (screen.get_width(), screen.get_height()))  # Scale to fit the screen

    if game_state == DIFFICULTY_SELECT:
        # Draw difficulty selection screen
        screen.blit(difficulty_bg_image, (0,0))
        screen.blit(select_difficulty_surface, (150, 200))
        screen.blit(easy_surface, (150, 250))
        screen.blit(normal_surface, (150, 300))
        screen.blit(hard_surface, (150, 350))
        
        # Draw high scores
        high_score_title = title_font.render("High Scores:", True, Colors.white)
        screen.blit(high_score_title, (150, 400))
        for i, score in enumerate(high_scores):
            score_text = title_font.render(f"{score['name']}: {score['score']}", True, Colors.white)
            screen.blit(score_text, (150, 450 + i * 30))
            
    elif game_state == NAME_INPUT:
        screen.fill(Colors.dark_blue)
        screen.blit(name_input_prompt, (50, 250))
        name_input_surface = title_font.render(current_name + "_", True, Colors.white)
        screen.blit(name_input_surface, (200, 300))
        
    elif game_state == PLAYING:
        # Handle continuous movement
        if not game.game_over:
            if moving_left:
                left_movement_timer -= clock.get_time()
                if left_movement_timer <= 0:
                    game.move_left()
                    left_movement_timer = left_movement_interval

            if moving_right:
                right_movement_timer -= clock.get_time()
                if right_movement_timer <= 0:
                    game.move_right()
                    right_movement_timer = right_movement_interval

            if moving_down:
                down_movement_timer -= clock.get_time()
                if down_movement_timer <= 0:
                    game.move_down()
                    down_movement_timer = down_movement_interval

        score_value_surface = title_font.render(str(int(game.score * current_score_multiplier)), True, Colors.white)
        
        screen.fill(Colors.dark_blue)
        screen.blit(background_image, (11, 11))
        screen.blit(overlay, (11, 11))
        
        game.draw(screen)
        
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        pygame.draw.rect(screen, Colors.light_blue, hold_rect, 0, 10)  # Draw hold area
        screen.blit(score_surface, (375, 15, 50, 50))
        screen.blit(score_value_surface, score_value_surface.get_rect(center=(score_rect.centerx, score_rect.centery)))
        screen.blit(next_surface, (375, 150, 50, 50))
        screen.blit(hold_surface, (375, 390, 50, 50))  # Draw hold text

        if game.game_over == True:
            screen.blit(game_over_surface, (100, 280, 50, 50))
            screen.blit(game_over1_surface, (80, 300, 50, 50))
        
        # Draw the next block preview
        if game.next_block is not None:
            block_size = 30
            original_offset = (game.next_block.row_offset, game.next_block.column_offset)
            game.next_block.row_offset = 0
            game.next_block.column_offset = 0
            
            positions = game.next_block.get_cell_positions()
            min_col = min(p.column for p in positions)
            max_col = max(p.column for p in positions)
            min_row = min(p.row for p in positions)
            max_row = max(p.row for p in positions)
            block_width = (max_col - min_col + 1) * block_size
            block_height = (max_row - min_row + 1) * block_size
            
            next_block_offset_x = next_rect.centerx - (block_width // 2)
            next_block_offset_y = next_rect.centery - (block_height // 2)
            
            for position in positions:
                x_pos = next_block_offset_x + (position.column - min_col) * block_size
                y_pos = next_block_offset_y + (position.row - min_row) * block_size
                cell_rect = pygame.Rect(x_pos, y_pos, block_size - 1, block_size - 1)
                scaled_texture = pygame.transform.scale(game.next_block.texture, (block_size - 1, block_size - 1))
                screen.blit(scaled_texture, cell_rect)
            
            game.next_block.row_offset, game.next_block.column_offset = original_offset

        # Draw the hold block preview
        if game.hold_block is not None:
            block_size = 30
            original_offset = (game.hold_block.row_offset, game.hold_block.column_offset)
            game.hold_block.row_offset = 0
            game.hold_block.column_offset = 0
            
            positions = game.hold_block.get_cell_positions()
            min_col = min(p.column for p in positions)
            max_col = max(p.column for p in positions)
            min_row = min(p.row for p in positions)
            max_row = max(p.row for p in positions)
            block_width = (max_col - min_col + 1) * block_size
            block_height = (max_row - min_row + 1) * block_size
            
            hold_block_offset_x = hold_rect.centerx - (block_width // 2)
            hold_block_offset_y = hold_rect.centery - (block_height // 2)
            
            for position in positions:
                x_pos = hold_block_offset_x + (position.column - min_col) * block_size
                y_pos = hold_block_offset_y + (position.row - min_row) * block_size
                cell_rect = pygame.Rect(x_pos, y_pos, block_size - 1, block_size - 1)
                scaled_texture = pygame.transform.scale(game.hold_block.texture, (block_size - 1, block_size - 1))
                screen.blit(scaled_texture, cell_rect)
            
            game.hold_block.row_offset, game.hold_block.column_offset = original_offset

    pygame.display.update()
    clock.tick(100)