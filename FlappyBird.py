import pygame
import os
import sys
import random
import pickle

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (51, 255, 51)
RED = (205, 32, 32)


def load_image(name):
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image

def load_sound(name):
    fullname = os.path.join("sounds", name)
    sound = pygame.mixer.Sound(fullname)
    return sound

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
        screen.blit(result, (70,180))


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
die_sound = load_sound('die.wav')
hit_sound = load_sound('hit.wav')
point_sound = load_sound('point.wav')
flap_sound = load_sound('flap.wav')
flappy_im = pygame.transform.scale(load_image('flappy.png'), (200,100))
gold_medal = pygame.transform.scale(load_image('gold.png'), (50,50))
silver_medal = pygame.transform.scale(load_image('silver.png'), (50,50))
bronze_medal = pygame.transform.scale(load_image('bronze.png'), (50,50))

pipe = Pipe()
bird = Bird()
floor = Floor()

def rules():
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 20)
    font3 = pygame.font.SysFont('Consolas', 20)
    rul = True
    while rul:
        screen.blit(background_day, (0,0))
        screen.blit(flappy_im, (100,40))
        headline = font1.render("Game Rules", True,  WHITE)
        screen.blit(headline, (60,120))
        line1 = font2.render("lalala pitu pitu", True, WHITE)
        line5 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line1, (20,210))
        screen.blit(line5, (70,490))
        pygame.display.update()
        fps.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rul = False
                    menu()

def author_info():
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 25)
    font3 = pygame.font.SysFont('Consolas', 20)
    info = True
    while info:
        screen.blit(background_day, (0,0))
        screen.blit(flappy_im, (95, 40))
        headline = font1.render("Author", True, WHITE)
        screen.blit(headline, (110, 120))
        line1 = font2.render("Hi! I am Julia and this is a Flappy Bird", True, WHITE)
        line2 = font2.render("game - the most annoying game in the", True, WHITE)
        line3 = font2.render("world! But to be honest one of my", True, WHITE)
        line4 = font2.render("favourite and that's why I've decided to ", True, WHITE)
        line5 = font2.render("make it :). I hope you will enjoy it too!", True, WHITE)
        line6 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line1, (20, 190))
        screen.blit(line2, (20, 220))
        screen.blit(line3,(20,250))
        screen.blit(line4, (20,280))
        screen.blit(line5, (20,310))
        screen.blit(line6, (70, 490))
        pygame.display.update()
        fps.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    info = False
                    menu()

def choose_bird():
    font2 = pygame.font.SysFont('arial', 20)
    choosen = 1
    while True:
        pygame.display.update()
        fps.tick(100)
        screen.blit(load_image('redbird_mid.png'), (50,200))
        screen.blit(load_image('yellowbird_mid.png'), (50,250))
        screen.blit(load_image('bluebird_mid.png'), (50,300))
        text1 = font2.render("Press 1", True, WHITE)
        text2 = font2.render("Press 2", True, WHITE)
        text3 = font2.render("Press 3", True, WHITE)
        screen.blit(text1, (100,200))
        screen.blit(text2, (100, 250))
        screen.blit(text3, (100, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choosen = 1
                if event.key == pygame.K_2:
                    choosen = 2
                if event.key == pygame.K_3:
                    choosen = 3
                return choosen


def show_options():
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 20)
    font3 = pygame.font.SysFont('Consolas', 20)
    options = True
    while options:
        screen.blit(background_day, (0, 0))
        screen.blit(flappy_im, (100, 40))
        headline = font1.render("Options", True, WHITE)
        screen.blit(headline, (100, 120))
        line5 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line5, (70, 490))
        pygame.display.update()
        fps.tick(100)
        choose_bird()

def show_records():
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 50)
    font3 = pygame.font.SysFont('Consolas', 20)
    screen.blit(background_day, (0, 0))
    with open('high_score4.dat', 'rb') as file:
        score1 = pickle.load(file)
    with open('high_score3.dat', 'rb') as file:
        score2 = pickle.load(file)
    with open('high_score2.dat', 'rb') as file:
        score3 = pickle.load(file)
    show = True
    while show:
        screen.blit(gold_medal, (120,180))
        screen.blit(silver_medal, (117,250))
        screen.blit(bronze_medal, (118,320))
        screen.blit(flappy_im, (100, 40))
        headline = font1.render("High Scores", True, WHITE)
        screen.blit(headline, (50, 100))
        line1 = font1.render(str(score1), True, WHITE)
        screen.blit(line1, (200,180))
        line2 = font1.render(str(score2), True, WHITE)
        screen.blit(line2, (200, 250))
        line3 = font1.render(str(score3), True, WHITE)
        screen.blit(line3, (200, 320))
        line5 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line5, (70, 490))
        pygame.display.update()
        fps.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show = False
                    menu()

def update_high_scores(score):
    with open('high_score4.dat', 'rb') as f4:
        last_high = pickle.load(f4)
        if score >= last_high:
            with open('high_score4.dat', 'wb') as f4:
                pickle.dump(score, f4)
        else:
            with open('high_score3.dat', 'rb') as f3:
                last_high = pickle.load(f3)
                if score >= last_high:
                    with open('high_score3.dat', 'wb') as f3:
                        pickle.dump(score, f3)
                else:
                    with open('high_score2.dat', 'rb') as f2:
                        last_high = pickle.load(f2)
                        if score > last_high:
                            with open('high_score2.dat', 'wb') as f2:
                                pickle.dump(score, f2)

def menu():
    font = pygame.font.Font('font.TTF', 30)
    font2 = pygame.font.SysFont('Consolas', 20)
    text = font2.render("Press SPACE to choose", True, RED)

    screen.blit(background_day, (0, 0))
    screen.blit(floor.floor, (0, 500))
    screen.blit(start_image, (100, 20))
    screen.blit(bird.red_mid, bird.rect)

    pygame.draw.rect(screen, RED, pygame.Rect(60, 340, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 340, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(60, 395, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 395, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(60, 450, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 450, 130, 40))

    m = True
    selected = 'Start'

    while m:
        screen.blit(text, (80, 560))

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
                if event.key == pygame.K_SPACE:
                    if selected == "Start":
                        flap()
                    if selected == "Exit":
                        pygame.quit()
                        sys.exit()
                    if selected == "Rules":
                        rules()
                    if selected == "Options":
                        show_options()
                    if selected == "Records":
                        show_records()
                    if selected == "Author":
                        author_info()
        if selected == "Start":
            start_text = font.render(f"Start", True, GREEN)
        else:
            start_text = font.render(f"Start", True,  WHITE)
        if selected == "Exit":
            exit_text = font.render(f"Exit", True, GREEN)
        else:
            exit_text = font.render(f"Exit", True,  WHITE)
        if selected == "Rules":
            rules_text = font.render(f"Rules", True, GREEN)
        else:
            rules_text = font.render(f"Rules", True,  WHITE)
        if selected == "Author":
            author_text = font.render(f"Author", True, GREEN)
        else:
            author_text = font.render(f"Author", True,  WHITE)
        if selected == "Records":
            scores_text = font.render(f"Records", True, GREEN)
        else:
            scores_text = font.render(f"Records", True,  WHITE)
        if selected == "Options":
            options_text = font.render(f"Options", True, GREEN)
        else:
            options_text = font.render(f"Options", True, WHITE)

        screen.blit(start_text, (80, 345))
        screen.blit(rules_text, (235, 345))
        screen.blit(options_text, (70, 400))
        screen.blit(scores_text, (215, 400))
        screen.blit(author_text, (75, 455))
        screen.blit(exit_text, (245, 455))
        pygame.display.update()
        fps.tick(100)

def flap():
    SHOWPIPE = pygame.USEREVENT
    pygame.time.set_timer(SHOWPIPE, 1300)
    bird_mov = 0
    game = True
    score = 0
    sound = True

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
                    flap_sound.play()
                    game = True
                    sound = True
                    bird_mov = 0
                    bird_mov += -2.3
            if event.type == SHOWPIPE:
                pipe.list_bottom.append(pipe.create_bottom())
                pipe.list_top.append(pipe.create_top())
            if event.type == pygame.KEYDOWN:
                if not game:
                    if event.key == pygame.K_RETURN:
                        score = 0
                        bird.rect.center = (50, 270)
                        pipe.list_top.clear()
                        pipe.list_bottom.clear()
                        menu()

        bird_mov += 0.1
        bird.rect.centery += bird_mov
        if game:
            if bird.rect.centery <= 12:
                bird.rect.centery = 12  #sufit
            pipe.move()
            floor.position += -2
            floor.move()
            if floor.position <= -400:
                floor.position = 0
            for i in pipe.list_bottom:
                if i.centerx == bird.rect.centerx - 40:
                    score += 1
                    point_sound.play()
            show_score(score, 0,'game_in')
        if not game:
            screen.blit(floor.floor, (0, 500))
            screen.blit(game_over_im, (100, 100))
            screen.blit(click_to_play, (110, 250))
            font3 = pygame.font.SysFont('Consolas', 20)
            screen.blit(font3.render("Press ENTER to go to menu.", True, RED), (60,535))
            screen.blit(font3.render("Press SPACE to play", True, RED), (90,565))
            pipe.list_top.clear()
            pipe.list_bottom.clear()
            show_score(score, 0,'game_over')
            update_high_scores(score)
            show_score(score, pickle.load(open('high_score4.dat', 'rb')), 'high_score')

        if pipe.collision():
            game = False
            die_sound.play()
        elif bird.rect.centery >= 490:
            bird.rect.centery = 490
            game = False
            if sound:
                hit_sound.play()
                sound = False

        pygame.display.update()
        fps.tick(100)


menu()
