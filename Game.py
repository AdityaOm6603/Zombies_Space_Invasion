import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Title and Icons
pygame.display.set_caption("Zombie-Space-Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# Background image
background = pygame.image.load("background.png")

# Music
mixer.music.load("space-120280.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Global variables
player_x = 0
player_y = 0
player_x_change = 0
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
bullet_x = 0
bullet_y = 0
bullet_x_change = 0
bullet_y_change = 0
visible_bullet = False
score = 0
lives = 3
no_of_enemy = 6
paused = False
is_running = False

# Fonts
my_font = pygame.font.Font('freesansbold.ttf', 32)
end_font = pygame.font.Font('freesansbold.ttf', 64)
lives_font = pygame.font.Font('freesansbold.ttf', 32)

# Images
img_player = pygame.image.load("spaceship.png")
img_player = pygame.transform.scale(img_player, (64, 64))
img_bullet = pygame.image.load("bullet.png")
img_bullet = pygame.transform.scale(img_bullet, (32, 32))


# Player setting
def reset_player():
    global player_x, player_y, player_x_change
    player_x = 368
    player_y = 510
    player_x_change = 0


# Enemies setting
def reset_enemies():
    global img_enemy, enemy_x, enemy_y, enemy_x_change, enemy_y_change, no_of_enemy
    img_enemy = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    for e in range(no_of_enemy):
        enemy_img = pygame.image.load("zombie.png")
        enemy_img = pygame.transform.scale(enemy_img, (64, 64))
        img_enemy.append(enemy_img)
        enemy_x.append(random.randint(0, 736))
        enemy_y.append(random.randint(50, 200))
        enemy_x_change.append(1.0)
        enemy_y_change.append(50)


# Bullet setting
def reset_bullet():
    global bullet_x, bullet_y, bullet_x_change, bullet_y_change, visible_bullet
    bullet_x = 0
    bullet_y = 500
    bullet_x_change = 0
    bullet_y_change = 9
    visible_bullet = False


# Score
def reset_score():
    global score
    score = 0


# Lives
def reset_lives():
    global lives
    lives = 3


def final_text():
    my_final_font = end_font.render("!GAME OVER!", True, (255, 255, 255))
    screen.blit(my_final_font, (200, 200))


def show_score(x, y):
    text = my_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


def show_lives(x, y):
    text = lives_font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(text, (x, y))


def player(x, y):
    screen.blit(img_player, (x, y))


def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


def bullet(x, y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x, y + 10))


def there_is_a_collision(x_1, y_1, x_2, y_2):
    dist = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if dist < 27:
        return True
    else:
        return False


def pause_game():
    global paused
    paused = True
    pause_font = pygame.font.Font('freesansbold.ttf', 50)
    pause_text = pause_font.render('Paused', True, (255, 255, 255))
    screen.blit(pause_text, (300, 250))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False


def instructions_screen():
    screen.blit(background, (0, 0))
    instructions_font = pygame.font.Font('freesansbold.ttf', 30)
    instructions_text = [
        "Use Arrow Keys to Move",
        "Press SPACE to Shoot",
        "Avoid Enemies and Keep Your Ship Safe",
        "Press P to Pause/Resume Game"
    ]
    y_position = 150
    for line in instructions_text:
        text = instructions_font.render(line, True, (255, 255, 255))
        screen.blit(text, (150, y_position))
        y_position += 40

    # Define the Start button
    button_rect = pygame.Rect(250, 400, 300, 70)  # Adjusted size for better fit

    # Color blinking effect setup
    button_colors = [(255, 255, 255), (255, 255, 0), (0, 0, 255)]  # White, Yellow, Blue
    current_color_index = 0
    button_blink_timer = pygame.time.get_ticks()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    waiting = False

        # Blinking effect logic
        current_time = pygame.time.get_ticks()
        if current_time - button_blink_timer > 1000:  # Change color every 1000ms
            current_color_index = (current_color_index + 1) % len(button_colors)
            button_blink_timer = current_time

        # Draw the Start button with blinking effect
        button_font = pygame.font.Font('freesansbold.ttf', 40)
        start_button_text = button_font.render('Start Game', True, button_colors[current_color_index])
        text_rect = start_button_text.get_rect(center=button_rect.center)

        # Clear the previous button text by filling the button area with the background color
        screen.blit(background, button_rect.topleft, button_rect)

        screen.blit(start_button_text, text_rect)

        pygame.display.update()


def game_over_screen():
    screen.blit(background, (0, 0))
    final_text()

    # Draw the Restart button
    button_font = pygame.font.Font('freesansbold.ttf', 40)
    restart_button_text = button_font.render('Restart', True, (255, 255, 255))
    button_rect = pygame.Rect(300, 400, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), button_rect, border_radius=25)

    # Center the text within the button_rect
    text_rect = restart_button_text.get_rect(center=button_rect.center)
    screen.blit(restart_button_text, text_rect)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    waiting = False
                    return True  # Indicates that the game should restart


def game_loop():
    global player_x, player_y, player_x_change, bullet_x, bullet_y, visible_bullet, score, lives, paused, is_running

    is_running = True
    while is_running:
        current_time = pygame.time.get_ticks()

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.WINDOWMINIMIZED:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -2
                if event.key == pygame.K_RIGHT:
                    player_x_change = 2
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound("shot.mp3")
                    bullet_sound.play()
                    if not visible_bullet:
                        bullet_x = player_x
                        bullet(bullet_x, bullet_y)
                if event.key == pygame.K_p:
                    pause_game()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        player_x += player_x_change

        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        for e in range(no_of_enemy):
            if enemy_y[e] > 450:
                lives -= 1
                enemy_y[e] = random.randint(50, 200)
                if lives == 0:
                    return  # End the current game loop
            enemy_x[e] += enemy_x_change[e]

            if enemy_x[e] <= 0:
                enemy_x_change[e] = 1.0
                enemy_y[e] += enemy_y_change[e]
            elif enemy_x[e] >= 736:
                enemy_x_change[e] = -1.0
                enemy_y[e] += enemy_y_change[e]

            collision = there_is_a_collision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
            if collision:
                collision_sound = mixer.Sound("punch.mp3")
                collision_sound.play()
                bullet_y = 500
                visible_bullet = False
                score += 1
                enemy_x[e] = random.randint(0, 736)
                enemy_y[e] = random.randint(50, 200)

            enemy(enemy_x[e], enemy_y[e], e)

        if bullet_y <= -32:
            bullet_y = 500
            visible_bullet = False
        if visible_bullet:
            bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(10, 10)
        show_lives(10, 40)

        pygame.display.update()


def main():
    reset_player()
    reset_enemies()
    reset_bullet()
    reset_score()
    reset_lives()

    instructions_screen()
    game_loop()

    if game_over_screen():
        main()  # Restart the game


if __name__ == "__main__":
    main()
