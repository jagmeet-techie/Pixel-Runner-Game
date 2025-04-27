import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('HULULULU')
clock = pygame.time.Clock()
text_font = pygame.font.Font('fonts/pixeltype.ttf', 50)

#  Audios
pygame.mixer.init()
collision_sound = pygame.mixer.Sound('audio/collision.mp3')  
jump_sound = pygame.mixer.Sound('audio/jump.mp3')  
background_music = pygame.mixer.music.load('audio/bg_music.mp3') 

# Start of bgm
pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        
        # Remove obstacles that have gone off-screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def player_animation():
    global player_surface, player_index, player_jump
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):  # Prevents index error when player_index exceeds walk animation list length
            player_index = 0
        player_surface = player_walk[int(player_index)]

# Game variables
game_active = False
start_time = 0
score = 0
obstacle_rect_list = []
collision_timer = 0  # Timer to track how long the bgm should stay paused

# graphics
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_surface = pygame.image.load('graphics/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/fly1.png').convert_alpha()

# Player
player_walk1 = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_jump = pygame.image.load('graphics/jump.png').convert_alpha()
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Start screen player stand image
player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand, (100, 125))
player_stand_rect = player_stand_scaled.get_rect(center=(400, 200))

game_name = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(midbottom=(400, 80))

game_message = text_font.render('Press Space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 360))

# Timer for obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Function to display score
def display_score():
    current_time = int((pygame.time.get_ticks() / 1000) - start_time)
    score_surface = text_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# MAIN GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()  # Play jump sound

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()  # Play jump sound

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 210)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() / 1000
                obstacle_rect_list.clear()
                player_rect.midbottom = (80, 300)
                player_gravity = 0

    if game_active:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Score
        score = display_score()

        # Obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Player movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)

        # Collision detection
        for obstacle_rect in obstacle_rect_list:
            if player_rect.colliderect(obstacle_rect):
                collision_sound.play()  # Play collision sound
                pygame.mixer.music.pause()  # Pause the background music
                collision_timer = pygame.time.get_ticks()  # Start the timer
                game_active = False

        # Check if collision pause has lasted 4 seconds
        if collision_timer and pygame.time.get_ticks() - collision_timer >= 4000:  # 4 seconds (4000 ms)
            pygame.mixer.music.unpause()  # Resume background music
            collision_timer = 0  # Reset the timer

    else:
        # Game Over / Start Screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            final_score_message = text_font.render(f'Your Score: {score}', False, (111, 196, 169))
            final_score_rect = final_score_message.get_rect(center=(400, 360))
            screen.blit(final_score_message, final_score_rect)

    pygame.display.update()
    clock.tick(60)
