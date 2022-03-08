import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

principal_path = os.path.dirname(__file__)
images_path = os.path.join(principal_path, 'images')
sounds_path = os.path.join(principal_path, 'sounds')

WIDTH = 640
HEIGHT = 480
WHITE = (255,255,255)

clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Game by. odgiedev')

sprite_sheet = pygame.image.load(os.path.join(images_path, 'dinoSpritesheet.png')).convert_alpha()

collision_sound = pygame.mixer.Sound(os.path.join('sounds', 'death_sound.wav'))
collision_sound.set_volume(1)

points_sound = pygame.mixer.Sound(os.path.join('sounds', 'score_sound.wav'))
points_sound.set_volume(1)

collided = False

obstacle_choice = choice([0,1])

game_velocity = 10

points = 0

highscore = 0

def restart_game():
    global points, game_velocity, collided, jumping, obstacle_choice
    points = 0
    game_velocity = 10
    collided = False
    dinoF.rect.x = WIDTH
    dino.rect.y  = HEIGHT - 64 - (96/2)
    dino.jumping = False
    cactus.rect.x = WIDTH
    obstacle_choice = choice([0,1])

def show_message(msg, size, collor):
    font = pygame.font.SysFont('comicsansms', size, True, False)
    message = f'{msg}'
    formated_text = font.render(message, True, False)
    return formated_text

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.jump_sound = pygame.mixer.Sound(os.path.join('sounds', 'jump_sound.wav'))
        self.jump_sound.set_volume(1)

        self.dino_images = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dino_images.append(img)
        
        self.list_index = 0
        self.image = self.dino_images[self.list_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100, HEIGHT - 64)
        self.initial_pos_y = HEIGHT - 64 - (96/2)
        self.jumping = False

    def jump(self):
        self.jumping = True
        self.jump_sound.play()

    def update(self):
        if self.jumping:
            if self.rect.y <= 200:
                self.jumping = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.initial_pos_y:
                self.rect.y += 20
            else:
                self.rect.y = self.initial_pos_y

        if self.list_index > 2:
            self.list_index = 0
        
        self.list_index += 0.25
        self.image = self.dino_images[int(self.list_index)]



class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50,200,50)
        self.rect.x = WIDTH - randrange(30,300,90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
            self.rect.y = randrange(50,200,50)
        self.rect.x -= game_velocity

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 64
        self.rect.x = pos_x*64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = WIDTH
        self.rect.x -= 10

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = obstacle_choice
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT - 64)
        self.rect.x = WIDTH
    
    def update(self):
        if self.choice == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH
            self.rect.x -= game_velocity

class DinoFly(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dinoF_images = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.dinoF_images.append(img)

        self.list_index = 0
        self.image = self.dinoF_images[self.list_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.choice = obstacle_choice
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, 300)
        self.rect.x = WIDTH

    def update(self):
        if self.choice == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = WIDTH
            self.rect.x -= game_velocity

            if self.list_index > 1:
                self.list_index = 0
            
            self.list_index += 0.25
            self.image = self.dinoF_images[int(self.list_index)]

all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)

for i in range(4):
    clouds = Clouds()
    all_sprites.add(clouds)

for i in range(11):
    ground = Ground(i)
    all_sprites.add(ground)

cactus = Cactus()
all_sprites.add(cactus)

dinoF = DinoFly()
all_sprites.add(dinoF)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(cactus)
obstacle_group.add(dinoF)

while True:
    clock.tick(30)
    window.fill(WHITE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_SPACE and collided == False:
                if dino.rect.y != dino.initial_pos_y:
                    pass
                else:
                    dino.jump()    
                
            if event.key == K_r and collided:
                restart_game()

    collisions = pygame.sprite.spritecollide(dino, obstacle_group, False, pygame.sprite.collide_mask)

    all_sprites.draw(window)

    if cactus.rect.topright[0] <= 0 or dinoF.rect.topright[0] <= 0:
        obstacle_choice = choice([0,1])
        cactus.rect.x = WIDTH
        dinoF.rect.x = WIDTH
        cactus.choice = obstacle_choice
        dinoF.choice = obstacle_choice

    if collisions and collided == False:
        collision_sound.play()
        collided = True
    
    if collided:
        if points % 100 == 0:
            points += 1
        
        if points > highscore:
            highscore = points

        game_over = show_message('GAME OVER', 40, (0,0,0))
        window.blit(game_over, (WIDTH/2, HEIGHT/2))

        restart = show_message('Press R to restart.', 20, (0,0,0))
        window.blit(restart, (WIDTH/2, (HEIGHT/2) + 60))

        highscoreM = show_message(f'Your highscore is {highscore}!', 20, (0,0,0))
        window.blit(highscoreM, (WIDTH/2, (HEIGHT/2) + 90))
    else:
        points += 1
        all_sprites.update()
        points_text = show_message(points, 40, (0,0,0))

    if points % 100 == 0:
        points_sound.play()
        if game_velocity >= 23:
            game_velocity += 0
        else:
            game_velocity += 1

    window.blit(points_text, (520,30))

    pygame.display.flip()
