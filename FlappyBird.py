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

def menu():
    font = pygame.font.Font('font.TTF', 30)
    screen.blit(background_day, (0, 0))
    screen.blit(floor.floor, (0, 500))
    screen.blit(start_image, (100, 20))

    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(60, 340, 130, 40))
    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(210, 340, 130, 40))
    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(60, 395, 130, 40))
    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(210, 395, 130, 40))
    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(60, 450, 130, 40))
    pygame.draw.rect(screen, (205, 32, 32), pygame.Rect(210, 450, 130, 40))

    white = (255, 255, 255)
    green = (51, 255, 51)
    m = True
    selected = 'Start'

    while m:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if selected == "Start":
                    if event.key == pygame.K_DOWN:
                        selected = "Options"
                    if event.key == pygame.K_RIGHT:
                        selected = "Rules"
                elif selected == "Rules":
                    if event.key == pygame.K_LEFT:
                        selected = "Start"
                    if event.key == pygame.K_DOWN:
                        selected = "Records"
                elif selected == "Options":
                    if event.key == pygame.K_UP:
                        selected = "Start"
                    if event.key == pygame.K_DOWN:
                        selected = "Author"
                    if event.key == pygame.K_RIGHT:
                        selected = "Records"
                elif selected == "Records":
                    if event.key == pygame.K_UP:
                        selected = "Rules"
                    if event.key == pygame.K_DOWN:
                        selected = "Exit"
                    if event.key == pygame.K_LEFT:
                        selected = "Options"
                elif selected == "Author":
                    if event.key == pygame.K_UP:
                        selected = "Options"
                    if event.key == pygame.K_RIGHT:
                        selected = "Exit"
                elif selected == "Exit":
                    if event.key == pygame.K_UP:
                        selected = "Records"
                    if event.key == pygame.K_LEFT:
                        selected = "Author"
                if event.key == pygame.K_RETURN:
                    if selected == "Start":
                        flap()
                    if selected == "Exit":
                        pygame.quit()
                        sys.exit()
                    if selected == "Rules":
                        pass
                    if selected == "Options":
                        pass
                    if selected == "Records":
                        pass
                    if selected == "Author":
                        pass
        if selected == "Start":
            start_text = font.render(f"Start", True, green)
        else:
            start_text = font.render(f"Start", True, white)
        if selected == "Exit":
            exit_text = font.render(f"Exit", True, green)
        else:
            exit_text = font.render(f"Exit", True, white)
        if selected == "Rules":
            rules_text = font.render(f"Rules", True, green)
        else:
            rules_text = font.render(f"Rules", True, white)
        if selected == "Author":
            author_text = font.render(f"Author", True, green)
        else:
            author_text = font.render(f"Author", True, white)
        if selected == "Records":
            scores_text = font.render(f"Records", True, green)
        else:
            scores_text = font.render(f"Records", True, white)
        if selected == "Options":
            options_text = font.render(f"Options", True, green)
        else:
            options_text = font.render(f"Options", True, white)

        screen.blit(start_text, (80, 345))
        screen.blit(rules_text, (235, 345))
        screen.blit(options_text, (70, 400))
        screen.blit(scores_text, (215, 400))
        screen.blit(author_text, (75, 455))
        screen.blit(exit_text, (245, 455))

        pygame.display.update()
        fps.tick(100)

def flap():
    bird_mov = 0
    game = True
    score = 0

    while True:
        screen.blit(background_day, (0, 0))
        screen.blit(bird.red_mid, bird.rect)

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


menu()
