import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Load assets
def load_image(path):
    return pygame.image.load(os.path.join("Assets", path))

# Dino images
DINO_RUN1 = load_image("Dino/DinoRun1.png")
DINO_RUN2 = load_image("Dino/DinoRun2.png")
DINO_DUCK1 = load_image("Dino/DinoDuck1.png")
DINO_DUCK2 = load_image("Dino/DinoDuck2.png")
DINO_DEAD = load_image("Dino/DinoDead.png")
DINO_START = load_image("Dino/DinoStart.png")  # Dino image for the main menu

# Cactus images
CACTUS_SMALL = [
    load_image("Cactus/SmallCactus1.png"),
    load_image("Cactus/SmallCactus2.png"),
    load_image("Cactus/SmallCactus3.png")
]
CACTUS_LARGE = [
    load_image("Cactus/LargeCactus1.png"),
    load_image("Cactus/LargeCactus2.png"),
    load_image("Cactus/LargeCactus3.png")
]

# Bird images
BIRD_FLY1 = load_image("Bird/Bird1.png")
BIRD_FLY2 = load_image("Bird/Bird2.png")

# Potion image
POTION_IMG = load_image("Potion/Potion1.png")

# Other images
GAME_OVER_IMG = load_image("Other/GameOver.png")
RESET_IMG = load_image("Other/Reset.png")
PAUSE_BUTTON_IMG = load_image("Other/PauseButton.png")
PLAY_BUTTON_IMG = load_image("Other/PlayButton.png")
CLOUD_IMG = load_image("Other/Cloud.png")
TRACK_IMG = load_image("Other/Track.png")
MENU_BUTTON_IMG = load_image("Other/MenuButton.png")  # Menu button image

# Dino properties
dino_width, dino_height = 40, 60
dino_x, dino_y = 50, HEIGHT - dino_height - 50
dino_vel_y = 0
gravity = 1
jump_strength = -15
is_jumping = False
is_ducking = False
dino_run_images = [DINO_RUN1, DINO_RUN2]
dino_duck_images = [DINO_DUCK1, DINO_DUCK2]
dino_index = 0

# Cactus properties
cactus_width, cactus_height = 30, 50
cactus_x, cactus_y = WIDTH, HEIGHT - cactus_height - 50
cactus_vel_x = -5
cactus_images = CACTUS_SMALL + CACTUS_LARGE
current_cactus = random.choice(cactus_images)

# Bird properties
bird_width, bird_height = 40, 30
bird_x, bird_y = WIDTH, HEIGHT - bird_height - 100
bird_vel_x = -5
bird_images = [BIRD_FLY1, BIRD_FLY2]
bird_index = 0
bird_active = False

# Potion properties
potion_width, potion_height = 20, 30
potion_x, potion_y = WIDTH, HEIGHT - potion_height - 100
potion_vel_x = -5
potion_active = False

# Cloud properties
cloud_width, cloud_height = 70, 40
cloud_x, cloud_y = WIDTH, random.randint(50, 150)
cloud_vel_x = -2

# Track properties
track_x, track_y = 0, HEIGHT - 50
track_vel_x = -5

# Health system
max_health = 100
health = max_health
health_bar_width, health_bar_height = 200, 20
health_bar_x, health_bar_y = 10, 100  # Updated position

# Score
distance_score = 0  # Distance traveled (incremented every frame)
cactus_score = 0    # Cacti jumped over (incremented when cactus goes off-screen)
hi_score = 0
font = pygame.font.SysFont("comicsans", 30)

# Load high score from file
def load_hi_score():
    if os.path.exists("hi_score.txt"):
        with open("hi_score.txt", "r") as file:
            return int(file.read())
    return 0

# Save high score to file
def save_hi_score(score):
    with open("hi_score.txt", "w") as file:
        file.write(str(score))

# Initialize high score
hi_score = load_hi_score()

# Pause button
pause_button_width, pause_button_height = 80, 80  # Size of the button image
pause_button_x, pause_button_y = WIDTH - pause_button_width - 50, 10
pause_button_hitbox_width, pause_button_hitbox_height = 100, 100  # Larger hitbox for easier clicking
is_paused = False

# Game over
game_over = False
restart_button_width, restart_button_height = 100, 50
restart_button_x, restart_button_y = WIDTH // 2 - restart_button_width // 2, HEIGHT // 2
menu_button_width, menu_button_height = 126, 50
menu_button_x, menu_button_y = WIDTH // 2 - menu_button_width // 2, HEIGHT // 2 + 70

# Hit effect
hit_effect_duration = 30  # Frames to display the hit effect
hit_effect_counter = 0
hit_effect_text = ""

# Main menu
main_menu = True
game_mode = None  # 1 for Normal, 2 for Advanced
mode1_button_width, mode1_button_height = 200, 50
mode1_button_x, mode1_button_y = WIDTH // 2 - mode1_button_width // 2, HEIGHT // 2 + 20
mode2_button_width, mode2_button_height = 200, 50
mode2_button_x, mode2_button_y = WIDTH // 2 - mode2_button_width // 2, HEIGHT // 2 + 80

# Sound effects and background music
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("Assets/Sounds/Jump.mp3")
bite_sound = pygame.mixer.Sound("Assets/Sounds/Bite.mp3")
collect_sound = pygame.mixer.Sound("Assets/Sounds/Collect.mp3")
pygame.mixer.music.load("Assets/Sounds/BackgroundMusic.mp3")
pygame.mixer.music.set_volume(0.3)  # Initial music volume
jump_sound.set_volume(0.5)  # Initial SFX volume
bite_sound.set_volume(0.5)
collect_sound.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop background music

def draw_dino(x, y, image):
    screen.blit(image, (x, y))

def draw_cactus(x, y, image):
    screen.blit(image, (x, y))

def draw_bird(x, y, image):
    screen.blit(image, (x, y))

def draw_potion(x, y):
    screen.blit(POTION_IMG, (x, y))

def draw_cloud(x, y):
    screen.blit(CLOUD_IMG, (x, y))

def draw_track(x, y):
    screen.blit(TRACK_IMG, (x, y))

def draw_pause_button():
    if is_paused:
        screen.blit(PLAY_BUTTON_IMG, (pause_button_x, pause_button_y))
    else:
        screen.blit(PAUSE_BUTTON_IMG, (pause_button_x, pause_button_y))

def draw_restart_button():
    screen.blit(RESET_IMG, (restart_button_x, restart_button_y))

def draw_menu_button():
    screen.blit(MENU_BUTTON_IMG, (menu_button_x, menu_button_y))  # Use MenuButton image

def draw_health_bar():
    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, health_bar_width * (health / max_health), health_bar_height))
    # Display HP number
    hp_text = font.render(f"HP: {health}", True, BLACK)
    screen.blit(hp_text, (health_bar_x + health_bar_width + 10, health_bar_y))

def display_score(distance_score, cactus_score, hi_score):
    distance_text = font.render(f"Distance: {distance_score}", True, BLACK)
    cactus_text = font.render(f"Cacti: {cactus_score}", True, BLACK)
    hi_score_text = font.render(f"Hi Score: {hi_score}", True, BLACK)
    screen.blit(distance_text, (10, 10))
    screen.blit(cactus_text, (10, 40))
    screen.blit(hi_score_text, (10, 70))

def check_collision(rect1_x, rect1_y, rect1_width, rect1_height, rect2_x, rect2_y, rect2_width, rect2_height):
    rect1 = pygame.Rect(rect1_x, rect1_y, rect1_width, rect1_height)
    rect2 = pygame.Rect(rect2_x, rect2_y, rect2_width, rect2_height)
    return rect1.colliderect(rect2)

def reset_game():
    global dino_y, dino_vel_y, is_jumping, cactus_x, distance_score, cactus_score, game_over, health, hit_effect_counter, hit_effect_text, potion_x, potion_active, bird_x, bird_active, is_ducking, cloud_x, cloud_y, hi_score
    dino_y = HEIGHT - dino_height - 50
    dino_vel_y = 0
    is_jumping = False
    is_ducking = False
    cactus_x = WIDTH
    potion_x = WIDTH
    potion_active = False
    bird_x = WIDTH
    bird_active = False
    cloud_x = WIDTH
    cloud_y = random.randint(50, 150)
    distance_score = 0
    cactus_score = 0
    health = max_health
    game_over = False
    hit_effect_counter = 0
    hit_effect_text = ""
    # Update high score if current score is higher
    if distance_score + cactus_score > hi_score:
        hi_score = distance_score + cactus_score
        save_hi_score(hi_score)
    # Restart background music
    pygame.mixer.music.play(-1)

def draw_main_menu():
    screen.fill(WHITE)
    # Draw Dino image
    dino_menu_x, dino_menu_y = WIDTH // 2 - DINO_START.get_width() // 2, HEIGHT // 2 - 100
    screen.blit(DINO_START, (dino_menu_x, dino_menu_y))
    # Draw game mode buttons
    pygame.draw.rect(screen, GRAY, (mode1_button_x, mode1_button_y, mode1_button_width, mode1_button_height))
    mode1_text = font.render("Normal Mode", True, BLACK)
    screen.blit(mode1_text, (mode1_button_x + 20, mode1_button_y + 10))
    pygame.draw.rect(screen, GRAY, (mode2_button_x, mode2_button_y, mode2_button_width, mode2_button_height))
    mode2_text = font.render("Advanced Mode", True, BLACK)
    screen.blit(mode2_text, (mode2_button_x + 20, mode2_button_y + 10))

def draw_pause_menu():
    # Darken the screen
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    # Draw pause menu options using images
    screen.blit(RESET_IMG, (restart_button_x, restart_button_y - 70))  # Restart button
    screen.blit(MENU_BUTTON_IMG, (menu_button_x, menu_button_y - 70))  # Main menu button
    
    # Volume controls
    music_volume_text = font.render("Music Volume", True, WHITE)
    sfx_volume_text = font.render("SFX Volume", True, WHITE)
    screen.blit(music_volume_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    screen.blit(sfx_volume_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))

    # Music volume slider
    music_slider_x = WIDTH // 2 - 100
    music_slider_y = HEIGHT // 2 + 70
    pygame.draw.rect(screen, WHITE, (music_slider_x, music_slider_y, 200, 10))
    pygame.draw.rect(screen, GREEN, (music_slider_x, music_slider_y, int(200 * pygame.mixer.music.get_volume()), 10))

    # SFX volume slider
    sfx_slider_x = WIDTH // 2 - 100
    sfx_slider_y = HEIGHT // 2 + 120
    pygame.draw.rect(screen, WHITE, (sfx_slider_x, sfx_slider_y, 200, 10))
    pygame.draw.rect(screen, BLUE, (sfx_slider_x, sfx_slider_y, int(200 * jump_sound.get_volume()), 10))
    
# Game loop
running = True
while running:
    if main_menu:
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if Normal Mode button is clicked
                if mode1_button_x <= mouse_x <= mode1_button_x + mode1_button_width and mode1_button_y <= mouse_y <= mode1_button_y + mode1_button_height:
                    main_menu = False
                    game_mode = 1  # Normal Mode
                    pygame.mixer.music.play(-1)  # Restart background music
                # Check if Advanced Mode button is clicked
                if mode2_button_x <= mouse_x <= mode2_button_x + mode2_button_width and mode2_button_y <= mouse_y <= mode2_button_y + mode2_button_height:
                    main_menu = False
                    game_mode = 2  # Advanced Mode
                    pygame.mixer.music.play(-1)  # Restart background music
    else:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not is_jumping and not game_over:
                    is_jumping = True
                    is_ducking = False
                    dino_vel_y = jump_strength
                    jump_sound.play()  # Play jump sound
                if event.key == pygame.K_DOWN and not is_jumping and not game_over:
                    is_ducking = True
                if event.key == pygame.K_p:  # Pause game when 'P' is pressed
                    is_paused = not is_paused
                    if is_paused:
                        pygame.mixer.music.pause()  # Pause background music
                    else:
                        pygame.mixer.music.unpause()  # Resume background music
                if event.key == pygame.K_r:  # Reset game when 'R' is pressed
                    reset_game()
                if event.key == pygame.K_m:  # Return to main menu when 'M' is pressed
                    main_menu = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_ducking = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if pause button is clicked (using larger hitbox)
                if pause_button_x <= mouse_x <= pause_button_x + pause_button_hitbox_width and pause_button_y <= mouse_y <= pause_button_y + pause_button_hitbox_height:
                    is_paused = not is_paused
                    if is_paused:
                        pygame.mixer.music.pause()  # Pause background music
                    else:
                        pygame.mixer.music.unpause()  # Resume background music
                # Adjust music volume
                music_slider_x = WIDTH // 2 - 100
                music_slider_y = HEIGHT // 2 + 70
                if is_paused and music_slider_x <= mouse_x <= music_slider_x + 200 and music_slider_y <= mouse_y <= music_slider_y + 10:
                    volume = (mouse_x - music_slider_x) / 200
                    pygame.mixer.music.set_volume(volume)

                # Adjust SFX volume
                sfx_slider_x = WIDTH // 2 - 100
                sfx_slider_y = HEIGHT // 2 + 120
                if is_paused and sfx_slider_x <= mouse_x <= sfx_slider_x + 200 and sfx_slider_y <= mouse_y <= sfx_slider_y + 10:
                    volume = (mouse_x - sfx_slider_x) / 200
                    jump_sound.set_volume(volume)
                    bite_sound.set_volume(volume)
                    collect_sound.set_volume(volume)
                # Check if restart button is clicked (in pause menu)
                if is_paused and restart_button_x <= mouse_x <= restart_button_x + restart_button_width and restart_button_y - 70 <= mouse_y <= restart_button_y - 70 + restart_button_height:
                    reset_game()
                    is_paused = False
                # Check if main menu button is clicked (in pause menu)
                if is_paused and menu_button_x <= mouse_x <= menu_button_x + menu_button_width and menu_button_y - 70 <= mouse_y <= menu_button_y - 70 + menu_button_height:
                    main_menu = True
                    is_paused = False
                # Check if restart button is clicked (in game over screen)
                if game_over and restart_button_x <= mouse_x <= restart_button_x + restart_button_width and restart_button_y <= mouse_y <= restart_button_y + restart_button_height:
                    reset_game()
                # Check if main menu button is clicked (in game over screen)
                if game_over and menu_button_x <= mouse_x <= menu_button_x + menu_button_width and menu_button_y <= mouse_y <= menu_button_y + menu_button_height:
                    main_menu = True
                    game_over = False

        if not is_paused and not game_over:
            # Dino movement
            if is_jumping:
                dino_y += dino_vel_y
                dino_vel_y += gravity
                if dino_y >= HEIGHT - dino_height - 50:
                    is_jumping = False
                    dino_y = HEIGHT - dino_height - 50

            # Cactus movement
            cactus_x += cactus_vel_x
            if cactus_x + cactus_width < 0:
                cactus_x = WIDTH
                current_cactus = random.choice(cactus_images)
                cactus_score += 1  # Increment cactus score

            # Bird movement (only in Advanced Mode)
            if game_mode == 2:
                if bird_active:
                    bird_x += bird_vel_x
                    if bird_x + bird_width < 0:
                        bird_active = False
                        bird_x = WIDTH

                # Randomly spawn bird (ensure it doesn't overlap with cactus)
                if not bird_active and random.randint(1, 100) == 1:  # 1% chance per frame
                    bird_active = True
                    bird_x = WIDTH
                    bird_y = random.randint(HEIGHT // 2, HEIGHT - bird_height - 50)
                    # Ensure bird doesn't spawn too close to cactus
                    if abs(bird_x - cactus_x) < 200:
                        bird_x = cactus_x + 200

            # Potion movement (only in Advanced Mode)
            if game_mode == 2:
                if potion_active:
                    potion_x += potion_vel_x
                    if potion_x + potion_width < 0:
                        potion_active = False
                        potion_x = WIDTH

                # Randomly spawn potion
                if not potion_active and random.randint(1, 100) == 1:  # 1% chance per frame
                    potion_active = True
                    potion_x = WIDTH
                    potion_y = random.randint(HEIGHT // 2, HEIGHT - potion_height - 50)

            # Cloud movement
            cloud_x += cloud_vel_x
            if cloud_x + cloud_width < 0:
                cloud_x = WIDTH
                cloud_y = random.randint(50, 150)

            # Track movement
            track_x += track_vel_x
            if track_x <= -WIDTH:
                track_x = 0

            # Update distance score (incremented every frame)
            distance_score += 1

            # Check collision with cactus
            if check_collision(dino_x, dino_y, dino_width, dino_height, cactus_x, cactus_y, cactus_width, cactus_height):
                if game_mode == 1:  # Normal Mode: Game over on collision
                    game_over = True
                elif game_mode == 2:  # Advanced Mode: Deduct health
                    health -= 20
                    cactus_x = WIDTH
                    hit_effect_counter = hit_effect_duration
                    hit_effect_text = "-20 HP"
                    bite_sound.play()  # Play bite sound
                    if health <= 0:
                        health = 0
                        game_over = True
                # Update high score if current score is higher
                if distance_score + cactus_score > hi_score:
                    hi_score = distance_score + cactus_score
                    save_hi_score(hi_score)

            # Check collision with bird (only in Advanced Mode)
            if game_mode == 2 and bird_active and check_collision(dino_x, dino_y, dino_width, dino_height, bird_x, bird_y, bird_width, bird_height):
                health -= 30
                bird_active = False
                hit_effect_counter = hit_effect_duration
                hit_effect_text = "-30 HP"
                bite_sound.play()  # Play bite sound
                if health <= 0:
                    health = 0
                    game_over = True
                # Update high score if current score is higher
                if distance_score + cactus_score > hi_score:
                    hi_score = distance_score + cactus_score
                    save_hi_score(hi_score)

            # Check collision with potion (only in Advanced Mode)
            if game_mode == 2 and potion_active and check_collision(dino_x, dino_y, dino_width, dino_height, potion_x, potion_y, potion_width, potion_height):
                health += 10
                if health > max_health:
                    health = max_health
                potion_active = False
                hit_effect_counter = hit_effect_duration
                hit_effect_text = "+10 HP"
                collect_sound.play()  # Play collect sound

        # Draw everything
        draw_track(track_x, track_y)
        draw_track(track_x + WIDTH, track_y)  # Draw second track for seamless scrolling
        draw_cloud(cloud_x, cloud_y)
        if is_ducking:
            draw_dino(dino_x, dino_y + 20, dino_duck_images[dino_index // 5 % len(dino_duck_images)])  # Ducking animation
        else:
            if game_over:
                draw_dino(dino_x, dino_y, DINO_DEAD)  # Show dead Dino when game over
            else:
                draw_dino(dino_x, dino_y, dino_run_images[dino_index // 5 % len(dino_run_images)])  # Running animation
        draw_cactus(cactus_x, cactus_y, current_cactus)
        if game_mode == 2 and bird_active:
            draw_bird(bird_x, bird_y, bird_images[bird_index // 5 % len(bird_images)])
        if game_mode == 2 and potion_active:
            draw_potion(potion_x, potion_y)
        display_score(distance_score, cactus_score, hi_score)
        if game_mode == 2:
            draw_health_bar()
        draw_pause_button()

        # Display hit effect
        if hit_effect_counter > 0:
            hit_text = font.render(hit_effect_text, True, RED if "-" in hit_effect_text else GREEN)
            screen.blit(hit_text, (dino_x, dino_y - 20))
            hit_effect_counter -= 1

        # Game over screen
        if game_over:
            screen.blit(GAME_OVER_IMG, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            draw_restart_button()
            draw_menu_button()
            pygame.mixer.music.stop()  # Stop background music

        # Pause menu
        if is_paused:
            draw_pause_menu()

    # Update display
    pygame.display.update()
    clock.tick(30)

    # Update animation indices
    dino_index += 1
    bird_index += 1

# Quit pygame
pygame.quit()