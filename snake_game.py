import pygame
import random

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)

# Dimensiones del juego
width, height = 600, 400

# Inicializar Pygame
pygame.init()
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Retro-Modern')

# Cargar imágenes y música
seta_img = pygame.image.load("assets/seta.png").convert_alpha()
mushroom_img = pygame.transform.scale(seta_img, (20, 20))
background_img = pygame.transform.scale(pygame.image.load("assets/fondo.png").convert(), (width, height))

pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.play(-1)

# Efecto de sonido cuando la serpiente come
eat_sound = pygame.mixer.Sound("assets/eat_sound.mp3")

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 10
font_style = pygame.font.SysFont("bahnschrift", 25)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, (34, 139, 34), [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect()

    # Establecemos un ancho máximo del 80% de la pantalla
    max_width = width * 0.8

    # Si el mensaje es más ancho que el ancho máximo, lo reducimos
    if text_rect.width > max_width:
        scale_factor = max_width / text_rect.width
        new_width = int(text_rect.width * scale_factor)
        new_height = int(text_rect.height * scale_factor)
        mesg = pygame.transform.scale(mesg, (new_width, new_height))
        text_rect = mesg.get_rect()

    # Centramos el mensaje
    text_rect.center = (width / 2, height / 2)
    game_window.blit(mesg, text_rect)



def spawn_food(snake_list):
    while True:
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        if [foodx, foody] not in snake_list:
            return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1

    # Initialize food position
    foodx, foody = spawn_food(snake_list)

    while not game_over:
        while game_close:
            game_window.blit(background_img, [0, 0])
            message("Perdiste! Presiona C para jugar de nuevo o Q para salir", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_over = False
                        game_close = False
                        gameLoop()  # Restart game properly

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        game_window.blit(background_img, [0, 0])

        game_window.blit(mushroom_img, [foodx, foody])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)

        pygame.display.update()

        # Manejo de colisiones con la comida
        snake_rect = pygame.Rect(x1, y1, snake_block, snake_block)
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)
        if snake_rect.colliderect(food_rect):
            foodx, foody = spawn_food(snake_list)  # Generate new food
            length_of_snake += 1
            pygame.mixer.Sound.play(eat_sound)  # Play eating sound

        clock.tick(snake_speed)

    pygame.quit()

gameLoop()
