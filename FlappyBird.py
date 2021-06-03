import pygame
import os
from pygame.locals import *
import sys
import random
import pickle


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


def load_image(name):
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.red_mid = load_image("redbird_mid.png")
        self.rect = self.red_mid.get_rect(center=(50, 270))


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.floor = pygame.transform.scale(load_image("base.png"), (400, 130))
        self.position = 0

    def move(self):
        screen.blit(self.floor, (self.position, 500))
        screen.blit(self.floor, (self.position + 400, 500))


class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.green_bottom = pygame.transform.scale(load_image("green_bottom.png"), (60, 350))
        self.green_top = pygame.transform.scale(load_image('green_top.png'), (60, 350))
        self.list_bottom = []
        self.list_top = []

    def create_bottom(self):
        self.random_height = random.randrange(150, 440)
        self.bottom = self.green_bottom.get_rect(midtop=(430, self.random_height))
        return self.bottom

    def create_top(self):
        self.top = self.green_bottom.get_rect(midbottom=(427, self.bottom.centery - 260))
        return self.top

    def move(self):
        for i in self.list_bottom:
            i.centerx -= 2
            screen.blit(self.green_bottom, i)
        for i in self.list_top:
            i.centerx -= 2
            screen.blit(self.green_top, i)

    def collision(self):
        for i in self.list_bottom:
            for j in self.list_top:
                if i.colliderect(bird.rect) or j.colliderect(bird.rect):
                    return True


def show_score(score, high_score, option):
    font = pygame.font.Font('font.TTF', 40)
    if option == 'game_over':
        result = font.render(f"SCORE: {int(score)}", True, (255, 255, 255))
        screen.blit(result, (120,40))
    elif option == 'game_in':
        result = font.render(f"{int(score)}", True, (255, 255, 255))
        screen.blit(result, (185,40))
    elif option == 'high_score':
        result = font.render(f"HIGH SCORE: {int(high_score)}", True, (255,255,255))
        screen.blit(result, (70,450))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
fps = pygame.time.Clock()
background_day = load_image("background_day.png")
background_day = pygame.transform.scale(background_day, (400, 600))
start_image = load_image("start.png")
start_image = pygame.transform.scale(start_image, (200,300))
start_image_rect = start_image.get_rect(center=(200,270))
game_over_im = load_image("gameover.png")
click_to_play = load_image("startclick.png")
SHOWPIPE = pygame.USEREVENT
pygame.time.set_timer(SHOWPIPE, 1300)

pipe = Pipe()
bird = Bird()
floor = Floor()


def flap():
    bird_mov = 0
    waiting = True
    game = True
    score = 0

    while True:
        screen.blit(background_day, (0, 0))
        screen.blit(bird.red_mid, bird.rect)

        while waiting:
            screen.blit(start_image, start_image_rect)
            floor.position += -1
            floor.move()
            if floor.position <= -400:
                floor.position = 0
            fps.tick(100)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                    if not game:
                        score = 0
                    game = True
                    bird_mov = 0
                    bird_mov += -2.3
            if event.type == SHOWPIPE:
                pipe.list_bottom.append(pipe.create_bottom())
                pipe.list_top.append(pipe.create_top())

        bird_mov += 0.1
        bird.rect.centery += bird_mov

        if game:
            if bird.rect.centery <= 12:
                bird.rect.centery = 12  #sufit
            pipe.move()
            floor.position += -1
            floor.move()
            if floor.position <= -400:
                floor.position = 0
            for i in pipe.list_bottom:
                if i.centerx == bird.rect.centerx - 40:
                    score += 1
            show_score(score, 0,'game_in')
        else:
            screen.blit(floor.floor, (0, 500))
            screen.blit(game_over_im, (100, 100))
            screen.blit(click_to_play, (110, 250))
            pipe.list_top.clear()
            pipe.list_bottom.clear()
            show_score(score, 0,'game_over')
            with open('high_score.dat', 'rb') as file:
                last_high = pickle.load(file)
                if score > last_high:
                    with open('high_score.dat', 'wb') as f:
                        pickle.dump(score, f)
            show_score(score, pickle.load(open('high_score.dat', 'rb')), 'high_score')

        if pipe.collision():
            game = False
        elif bird.rect.centery >= 490:
            bird.rect.centery = 490
            game = False

        pygame.display.update()
        fps.tick(100)


flap()
