import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('HULULULU')
clock = pygame.time.Clock()
text_font = pygame.font.Font('fonts/pixeltype.ttf', 50)

# Game variables
game_active = True
crossed_snail = False

# Load graphics
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

snail_surface = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

player_surface = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Function to display score
def display_score():
    current_time=int(pygame.time.get_ticks() / 1000)
    score_surface = text_font.render(f'Score: {current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
                 game_active=True
                 snail_rect.left = 800
                 current_time=int(pygame.time.get_ticks() / 1000)
                 
                 

    if game_active:
        # Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # Score
        display_score()

        # Snail movement
        snail_rect.x -= 5
        if snail_rect.right <= 0:
            snail_rect.left = 800
            crossed_snail = False  # Reset crossed when snail comes back
        screen.blit(snail_surface, snail_rect)

        # Player movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            player_gravity = 0
        screen.blit(player_surface, player_rect)

        # Collision detection
        if player_rect.colliderect(snail_rect):
            game_active = False

        # Successful jump detection
        if snail_rect.right < player_rect.left and not crossed_snail:
            score += 1
            crossed_snail = True

    else:
        # Game Over Screen
        screen.fill('pink')
        game_over_surface = text_font.render('GAME OVER', False, 'Black')
        game_over_rect = game_over_surface.get_rect(center=(400, 200))
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(60)
