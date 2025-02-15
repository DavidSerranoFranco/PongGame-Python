import pygame as pg

# Initialize pygame
pg.init()
pg.mixer.init()

# Constants
WIDTH_WINDOW = 900
HEIGHT_WINDOW = 600
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (0, 14, 46)
BLUE = (70, 150, 180)
RED = (200, 70, 90)
BLACK = (0, 0, 0)
SPEED = 7

# Initialize window
window = pg.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pg.display.set_caption('Ping Pong Game xPro 1.0')
icon = pg.image.load('D:/PythonProjects/GamePongProject/pong.png')
pg.display.set_icon(icon)

# Initialize font
pg.font.init()
font = pg.font.Font(None, 30)
big_font = pg.font.Font(None, 80)

# Load sounds
sound_hit = pg.mixer.Sound('D:/PythonProjects/GamePongProject/Sounds/hit.mp3')
sound_wall = pg.mixer.Sound('D:/PythonProjects/GamePongProject/Sounds/wall.mp3')
sound_score = pg.mixer.Sound('D:/PythonProjects/GamePongProject/Sounds/point.mp3')

# Adjust volume
sound_hit.set_volume(0.5)
sound_wall.set_volume(0.5)
sound_score.set_volume(0.7)


def draw_text(text, font, color, y_offset=0):
    """Helper function to draw centered text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH_WINDOW // 2, HEIGHT_WINDOW // 2 + y_offset))
    window.blit(text_surface, text_rect)


def show_main_menu():
    """Display the main menu and return the selected game mode."""
    while True:
        window.fill(BLACK)
        draw_text('PONG', big_font, WHITE, -200)
        draw_text('Press 1 for 1 Player (VS AI)', font, WHITE, -50)
        draw_text('Press 2 for 2 Players', font, WHITE, 0)
        draw_text('Press Q to Quit', font, WHITE, 50)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    return 'ai'
                elif event.key == pg.K_2:
                    return '2p'
                elif event.key == pg.K_q:
                    pg.quit()
                    quit()

def show_points_menu():
    """Display the points menu and return the selected winning score."""
    while True:
        window.fill(BLACK)
        draw_text('Select Winning Score', big_font, WHITE, -200)
        draw_text('Press 5 to play to 5 points', font, WHITE, -50)
        draw_text('Press 10 to play to 10 points', font, WHITE, 0)
        draw_text('Press Q to Quit', font, WHITE, 50)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_5:
                    return 5
                elif event.key == pg.K_0:
                    return 10
                elif event.key == pg.K_q:
                    pg.quit()
                    quit()

def show_restart_menu():
    """Display the restart menu and return the user's choice."""
    while True:
        window.fill(BLACK)
        draw_text('Game Over', big_font, WHITE, -200)
        draw_text('Press R to Restart with same settings', font, WHITE, -50)
        draw_text('Press M to go back to Menu', font, WHITE, 0)
        draw_text('Press Q to Quit', font, WHITE, 50)
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return 'restart'
                elif event.key == pg.K_m:
                    return 'menu'
                elif event.key == pg.K_q:
                    pg.quit()
                    quit()

def ai_move(paddle, ball, speed):
    """Simple AI to move the paddle towards the ball."""
    if paddle.centery < ball.centery:
        paddle.y += speed
    elif paddle.centery > ball.centery:
        paddle.y -= speed

    # Ensure the paddle stays within the window bounds
    if paddle.top < 0:
        paddle.top = 0
    if paddle.bottom > HEIGHT_WINDOW:
        paddle.bottom = HEIGHT_WINDOW

def reset_ball(ball, ball_speed_x, ball_speed_y):
    """Reset the ball to the center and reverse its direction."""
    ball.x = WIDTH_WINDOW // 2
    ball.y = HEIGHT_WINDOW // 2
    return ball_speed_x * -1, ball_speed_y * -1


def game_loop(winning_score, game_mode):
    """Main game loop."""
    p1_x, p1_y = 50, 250
    p2_x, p2_y = 820, 250
    ball_x, ball_y = 450, 300
    WIDTH_PADDLE, HEIGHT_PADDLE = 30, 100
    WIDTH_BALL, HEIGHT_BALL = 10, 10
    ball_speed_x, ball_speed_y = 8, 8
    score_p1, score_p2 = 0, 0

    paddle_p1 = pg.Rect(p1_x, p1_y, WIDTH_PADDLE, HEIGHT_PADDLE)
    paddle_p2 = pg.Rect(p2_x, p2_y, WIDTH_PADDLE, HEIGHT_PADDLE)
    ball = pg.Rect(ball_x, ball_y, WIDTH_BALL, HEIGHT_BALL)

    my_clock = pg.time.Clock()

    while True:
        pg.time.delay(16)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        keys = pg.key.get_pressed()
        if keys[pg.K_w] and paddle_p1.top > 0:
            paddle_p1.y -= SPEED
        if keys[pg.K_s] and paddle_p1.bottom < HEIGHT_WINDOW:
            paddle_p1.y += SPEED

        if game_mode == '2p':
            if keys[pg.K_UP] and paddle_p2.top > 0:
                paddle_p2.y -= SPEED
            if keys[pg.K_DOWN] and paddle_p2.bottom < HEIGHT_WINDOW:
                paddle_p2.y += SPEED
        else:
            ai_move(paddle_p2, ball, SPEED)

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.colliderect(paddle_p1) or ball.colliderect(paddle_p2):
            ball_speed_x *= -1
            sound_hit.play()
        if ball.top <= 0 or ball.bottom >= HEIGHT_WINDOW:
            ball_speed_y *= -1
            sound_wall.play()
        if ball.left <= 0:
            score_p2 += 1
            sound_score.play()
            ball_speed_x, ball_speed_y = reset_ball(ball, ball_speed_x, ball_speed_y)
        elif ball.right >= WIDTH_WINDOW:
            score_p1 += 1
            sound_score.play()
            ball_speed_x, ball_speed_y = reset_ball(ball, ball_speed_x, ball_speed_y)

        if score_p1 >= winning_score or score_p2 >= winning_score:
            break

        window.fill(BACKGROUND_COLOR)
        pg.draw.rect(window, BLUE, paddle_p1)
        pg.draw.rect(window, RED, paddle_p2)
        pg.draw.rect(window, WHITE, ball)
        draw_text(f'Score P1: {score_p1}', font, WHITE, -250)
        draw_text(f'Score P2: {score_p2}', font, WHITE, 250)
        pg.display.flip()
        my_clock.tick(60)

    choice = show_restart_menu()
    return choice


def main():
    """Main function to handle the game flow."""
    while True:
        game_mode = show_main_menu()  # Mostrar el menú principal

        if game_mode == '2p':
            winning_score = show_points_menu()  # Mostrar el menú de puntos para 2 jugadores
        else:
            winning_score = 5  # Valor predeterminado para el modo AI

        while True:
            choice = game_loop(winning_score, game_mode)  # Iniciar el juego
            if choice == 'menu':
                break  # Volver al menú principal


if __name__ == '__main__':
    main()
    pg.quit()