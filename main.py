# Snake Pygame Beta
import pygame as pg
from random import randrange

pg.font.init()

window = 600
tile_size = 30
range = (tile_size // 2, window - tile_size // 2 , tile_size)
pg.display.set_caption("Snake Pygame")
fullscreen = False
get_random_pos = lambda: [randrange(*range), randrange(*range)]
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
snake.center = get_random_pos()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_pos()
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
dirs = {
    pg.K_w or pg.K_UP :1,
    pg.K_s or pg.K_DOWN: 1, 
    pg.K_a or pg.K_LEFT: 1, 
    pg.K_d or pg.K_RIGHT: 1
}

# Background image
bg = pg.image.load('snakebackground.png').convert()

# Assets Load
original_snakeright = pg.image.load('snakeright.jpg')
snakeright = pg.transform.scale(original_snakeright, (tile_size - 2, tile_size - 2))

original_snakeleft = pg.image.load('snakeleft.jpg')
snakeleft = pg.transform.scale(original_snakeleft, (tile_size - 2, tile_size - 2))

original_snakedown = pg.image.load('snakedown.jpg')
snakedown = pg.transform.scale(original_snakedown, (tile_size - 2, tile_size - 2))

original_snakeup = pg.image.load('snakeup.jpg')
snakeup = pg.transform.scale(original_snakeup, (tile_size - 2, tile_size - 2))

original_snakebody = pg.image.load('snake_body.png')
snakebody = pg.transform.scale(original_snakebody, (tile_size - 2, tile_size - 2))

original_apple = pg.image.load('redButton.png')
apple = pg.transform.scale(original_apple, (tile_size - 2, tile_size - 2))

# Music
ost = "chill by sakura HZ [Music promoted by Audio Library].mp3"
pg.mixer.init()
pg.mixer.music.load(ost)
pg.mixer.music.play(-1)


# Score and Font
font = pg.font.Font(None, 26)
score = 0

game_over = False

# Guide Before the Game Start
guide_text = font.render("Press WASD or Arrow Keys to Start the Game!", True, (93, 255, 0))
guide_rect = guide_text.get_rect(center=(window // 2, window // 2))
guide_visible = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            guide_visible = False
            if (event.key == pg.K_w or event.key == pg.K_UP) and dirs[pg.K_w]:
                snake_dir = (0, -tile_size)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d:1}
            elif event.key == pg.K_s or event.key == pg.K_DOWN and dirs[pg.K_s]:
                snake_dir = (0, tile_size)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d:1}
            elif event.key == pg.K_a or event.key == pg.K_LEFT and dirs[pg.K_a]:
                snake_dir = (-tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d:0}
            elif event.key == pg.K_d or event.key == pg.K_RIGHT and dirs[pg.K_d]:
                snake_dir = (tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d:1}

            if game_over and event.key == pg.K_SPACE:
                game_over = False
                snake.center, food.center = get_random_pos(), get_random_pos()
                length = 1
                snake_dir = (0, 0)
                segments = [snake.copy()]
                score = 0
                guide_visible = True

    screen.blit(bg, (0, 0))
    if guide_visible:
        screen.blit(guide_text, guide_rect)

    if not game_over:
        # Borders and Selfeating Check
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or self_eating:
            game_over = True
        # Food Check
        if snake.center == food.center:
            while True:
                food.center = get_random_pos()
                if food.center not in [seg.center for seg in segments]:
                    break
            length += 1
            score += 1
        # Food Draw
        screen.blit(apple, food)
        # Snake Draw
        # Body
        for segment in segments[:-1]:
            screen.blit(snakebody, segment)
        
        # Head
        head = segments[-1]

        if snake_dir == (tile_size, 0):
            screen.blit(snakeright, head)
        elif snake_dir == (-tile_size, 0):
            screen.blit(snakeleft, head)
        elif snake_dir == (0, tile_size):
            screen.blit(snakedown, head)
        elif snake_dir == (0, -tile_size):
            screen.blit(snakeup, head)
        
        else:
            screen.blit(snakeright, head)
    
        # Score Display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        # Snake Movement
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

    if game_over:
        game_over_text1 = font.render("Game Over", True, (255, 0, 0))
        game_over_rect1 = game_over_text1.get_rect(center=(window // 2, window // 2 - 20))
        screen.blit(game_over_text1, game_over_rect1)

        game_over_text2 = font.render("Press SPACE to Restart", True, (255, 255, 0))
        game_over_rect2 = game_over_text2.get_rect(center=(window // 2, window // 2 + 10))
        screen.blit(game_over_text2, game_over_rect2)

        game_over_text3 = font.render("Your Score: " + str(score), True, (255, 255, 255))
        game_over_rect3 = game_over_text3.get_rect(center=(window // 2, window // 2 + 40))
        screen.blit(game_over_text3, game_over_rect3)

        guide_visible = False

    pg.display.flip()
    clock.tick(120)