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
BLACK = (0,0,0)


def load_image(name):
    """
    Upload an image from file and convert it to the surface.
    :param name: name of the image file
    :return: converted image
    """
    fullname = os.path.join("images", name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image

def load_sound(name):
    """
    Upload a sound from file.
    :param name: name of the sound file
    :return: sound
    """
    fullname = os.path.join("sounds", name)
    sound = pygame.mixer.Sound(fullname)
    return sound

class Bird(pygame.sprite.Sprite):
    """
    Class representing a bird.
    """
    def __init__(self):
        """
        Initialize three birds and their rects.
        """
        pygame.sprite.Sprite.__init__(self)
        self.red_mid = load_image("redbird_mid.png")
        self.red_rect = self.red_mid.get_rect(center=(50, 270))
        self.yellow_mid = load_image('yellowbird_mid.png')
        self.yellow_rect = self.yellow_mid.get_rect(center=(50,260))
        self.blue_mid = load_image('bluebird_mid.png')
        self.blue_rect = self.blue_mid.get_rect(center=(50,260))


class Floor(pygame.sprite.Sprite):
    """
    Class representing the floor.
    """
    def __init__(self):
        """
        Initialize the floor and its position.
        """
        pygame.sprite.Sprite.__init__(self)
        self.floor = pygame.transform.scale(load_image("base.png"), (400, 130))
        self.position = 0

    def move(self):
        """
        Repeatedly move the floor to the left.
        """
        screen.blit(self.floor, (self.position, 500))
        screen.blit(self.floor, (self.position + 400, 500))


class Pipe(pygame.sprite.Sprite):
    """
    Class representing the pipes.
    """
    def __init__(self):
        """
        Initialize top and bottom pipe.
        """
        pygame.sprite.Sprite.__init__(self)
        self.green_bottom = pygame.transform.scale(load_image("green_bottom.png"), (60, 350))
        self.green_top = pygame.transform.scale(load_image('green_top.png'), (60, 350))
        self.list_bottom = []
        self.list_top = []

    def create_bottom(self):
        """
        Create a bottom pipe rectangle.
        :return: bottom pipe rectangle
        """
        self.random_height = random.randrange(150, 440)
        self.bottom = self.green_bottom.get_rect(midtop=(430, self.random_height))
        return self.bottom

    def create_top(self):
        """
        Create a top pipe rectangle.
        :return: top pipe rectangle
        """
        self.top = self.green_bottom.get_rect(midbottom=(427, self.bottom.centery - 260))
        return self.top

    def move(self, option: float):
        """
        Move top and bottom pipes repeatedly to the left.
        :param option: distance by which the pipes move
        :return: moving pipes
        """
        for i in self.list_bottom:
            i.centerx -= option
            screen.blit(self.green_bottom, i)
        for i in self.list_top:
            i.centerx -= option
            screen.blit(self.green_top, i)

    def collision(self, bird_col):
        """
        Check if bird collide with the pipes.
        :param bird_col: chosen bird rectangle
        :return: True if collided
        """
        for i in self.list_bottom:
            for j in self.list_top:
                if i.colliderect(bird_col) or j.colliderect(bird_col):
                    return True

def show_score(score, high_score, option):
    """
    Display the score on the screen.
    :param score: gained score to display
    :param high_score: high_score to display
    :param option: state of the game('game_over', 'game_in' or 'high_score' when displaying the high score)
    :return: display wanted score
    """
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
background_night = load_image("background_night.png")
background_night = pygame.transform.scale(background_night, (400,600))
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
gold_medal = pygame.transform.scale(load_image('gold.png'), (40,40))
silver_medal = pygame.transform.scale(load_image('silver.png'), (40,40))
bronze_medal = pygame.transform.scale(load_image('bronze.png'), (40,40))

pipe = Pipe()
bird = Bird()
floor = Floor()

def rules():
    """
    Show rules of the game
    """
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 20)
    font3 = pygame.font.SysFont('Consolas', 20)
    rul = True
    while rul:
        screen.blit(background_day, (0,0))
        screen.blit(flappy_im, (100,40))
        headline = font1.render("Game Rules", True,  WHITE)
        screen.blit(headline, (60,120))
        screen.blit(font2.render("This game is about flying a bird between pipes.", True, BLACK),(20,210))
        screen.blit(font2.render("The bird is automatically flying down and you", True, BLACK),(20,230))
        screen.blit(font2.render("can start its fly up by pressing a SPACE button ", True, BLACK), (20,250))
        screen.blit(font2.render("or click a mouse. When the bird collide with ", True, BLACK),(20,270))
        screen.blit(font2.render("the pipes or with the ground the game is over", True, BLACK),(20,290))
        screen.blit(font2.render("and you have to start from the beginning. ", True, BLACK),(20,310))
        screen.blit(font2.render("After avoiding the pipe you will get one point.", True, BLACK),(20,330))
        screen.blit(font2.render("So let's try it yourself and have fun!", True, BLACK), (20, 350))
        screen.blit(font3.render("Press SPACE to go back.", True, RED),(70,490))
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
    """
    Show info about author of this game"
    """
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 25)
    font3 = pygame.font.SysFont('Consolas', 20)
    info = True
    while info:
        screen.blit(background_day, (0,0))
        screen.blit(flappy_im, (95, 40))
        headline = font1.render("Author", True, WHITE)
        screen.blit(headline, (110, 120))
        line1 = font2.render("Hi! I am Julia and this is a Flappy Bird", True, BLACK)
        line2 = font2.render("game - the most annoying game in the", True, BLACK)
        line3 = font2.render("world! But to be honest one of my", True, BLACK)
        line4 = font2.render("favourite and that's why I've decided to ", True, BLACK)
        line5 = font2.render("make it :). I hope you will enjoy it too!", True, BLACK)
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

def choose_options():
    """
    Show screen with possible game options which player can choose and start the game after choosing.
    """
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 20)
    font3 = pygame.font.SysFont('Consolas', 20)
    font4 = pygame.font.SysFont('arial', 25)
    options = True
    while options:
        screen.blit(background_day, (0, 0))
        screen.blit(load_image('redbird_mid.png'), (30, 260))
        screen.blit(load_image('yellowbird_mid.png'), (30, 300))
        screen.blit(load_image('bluebird_mid.png'), (30, 340))
        screen.blit(load_image('redbird_mid.png'), (230, 260))
        screen.blit(load_image('yellowbird_mid.png'), (230, 300))
        screen.blit(load_image('bluebird_mid.png'), (230, 340))
        screen.blit(font2.render("Press 1", True, WHITE), (80, 260))
        screen.blit(font2.render("Press 2", True, WHITE), (80, 300))
        screen.blit(font2.render("Press 3", True, WHITE), (80,340))
        screen.blit(font2.render("Press 4", True, WHITE), (280,260))
        screen.blit(font2.render("Press 5", True, WHITE), (280,300))
        screen.blit(font2.render("Press 6", True, WHITE), (280,340))
        screen.blit(font4.render("Choose mode and bird color to start:", True, WHITE), (30,175))
        screen.blit(font4.render("EASY", True, WHITE), (70,215))
        screen.blit(font4.render("HARD", True, WHITE), (270,215))
        screen.blit(flappy_im, (100, 40))
        headline = font1.render("Options", True, WHITE)
        screen.blit(headline, (100, 120))
        line5 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line5, (70, 490))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu()
                if event.key == pygame.K_1:
                    flap('easy', 'red')
                if event.key == pygame.K_2:
                    flap('easy', 'yellow')
                if event.key == pygame.K_3:
                    flap('easy', 'blue')
                if event.key == pygame.K_4:
                    flap('hard', 'red')
                if event.key == pygame.K_5:
                    flap('hard', 'yellow')
                if event.key == pygame.K_6:
                    flap('hard', 'blue')
        pygame.display.update()
        fps.tick(100)

def show_options():
    """
    Only show possible options of the game.
    """
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 25)
    font3 = pygame.font.SysFont('Consolas', 20)
    font4 = pygame.font.SysFont('arial', 20)
    screen.blit(background_day, (0, 0))
    show = True
    while show:
        screen.blit(flappy_im, (95, 40))
        screen.blit(load_image('redbird_mid.png'), (120, 300))
        screen.blit(load_image('yellowbird_mid.png'), (180, 300))
        screen.blit(load_image('bluebird_mid.png'), (240, 300))
        screen.blit(font2.render("In this game you have two possible", True, BLACK), (30, 175))
        screen.blit(font2.render("difficulty levels:   EASY   and   HARD", True, BLACK), (30,210))
        screen.blit(font2.render('and three bird colors to choose:', True, BLACK), (30,245))
        screen.blit(font4.render('You can choose them after clicking start button', True, BLACK), (23, 330))
        headline = font1.render("Options", True, WHITE)
        screen.blit(headline, (100, 120))
        line5 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line5, (70, 490))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu()
        pygame.display.update()
        fps.tick(100)


def show_records():
    """
    Show the screen with three high scores in easy and hard mode.
    """
    font1 = pygame.font.Font('font.TTF', 50)
    font2 = pygame.font.SysFont('arial', 30)
    font3 = pygame.font.SysFont('Consolas', 20)
    font4 = pygame.font.Font('font.TTF', 40)
    screen.blit(background_day, (0, 0))
    with open('high_score4.dat', 'rb') as file:
        score1 = pickle.load(file)
    with open('high_score3.dat', 'rb') as file:
        score2 = pickle.load(file)
    with open('high_score2.dat', 'rb') as file:
        score3 = pickle.load(file)
    with open('high_score7.dat', 'rb') as file:
        score4 = pickle.load(file)
    with open('high_score6.dat', 'rb') as file:
        score5 = pickle.load(file)
    with open('high_score5.dat', 'rb') as file:
        score6 = pickle.load(file)
    show = True
    while show:
        screen.blit(gold_medal, (15,205))
        screen.blit(silver_medal, (12,260))
        screen.blit(bronze_medal, (13,315))
        screen.blit(gold_medal, (215, 205))
        screen.blit(silver_medal, (212, 260))
        screen.blit(bronze_medal, (213, 315))
        screen.blit(flappy_im, (100, 40))
        headline = font1.render("High Scores", True, WHITE)
        screen.blit(headline, (50, 100))
        screen.blit(font2.render("EASY", True, WHITE), (50,160))
        screen.blit(font2.render("HARD", True, WHITE), (250,160))
        line1 = font4.render(str(score1), True, WHITE)
        screen.blit(line1, (70,205))
        line2 = font4.render(str(score2), True, WHITE)
        screen.blit(line2, (70, 260))
        line3 = font4.render(str(score3), True, WHITE)
        screen.blit(line3, (70, 315))
        line4 = font4.render(str(score4), True, WHITE)
        screen.blit(line4, (270, 205))
        line5 = font4.render(str(score5), True, WHITE)
        screen.blit(line5, (270, 260))
        line6 = font4.render(str(score6), True, WHITE)
        screen.blit(line6, (270, 315))
        line6 = font3.render("Press SPACE to go back.", True, RED)
        screen.blit(line6, (70, 490))
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

def update_easy_high_scores(score):
    """
    Update the high score of game easy mode and write it to the appropriate file.
    :param score: gained score
    """
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

def update_hard_high_scores(score):
    """
    Update the high score of game hard mode and write it to the appropriate file.
    :param score: gained score
    """
    with open('high_score7.dat', 'rb') as f7:
        last_high = pickle.load(f7)
        if score >= last_high:
            with open('high_score7.dat', 'wb') as f7:
                pickle.dump(score, f7)
        else:
            with open('high_score6.dat', 'rb') as f6:
                last_high = pickle.load(f6)
                if score >= last_high:
                    with open('high_score3.dat', 'wb') as f6:
                        pickle.dump(score, f6)
                else:
                    with open('high_score5.dat', 'rb') as f5:
                        last_high = pickle.load(f5)
                        if score > last_high:
                            with open('high_score2.dat', 'wb') as f5:
                                pickle.dump(score, f5)

def menu():
    """
    Show screen with the main menu.
    """
    font = pygame.font.Font('font.TTF', 30)
    font2 = pygame.font.SysFont('Consolas', 20)
    text = font2.render("Use arrow keys to navigate.", True, RED)
    text1 = font2.render("Press SPACE to choose.", True, RED)

    screen.blit(background_day, (0, 0))
    screen.blit(floor.floor, (0, 500))
    screen.blit(start_image, (100, 20))

    pygame.draw.rect(screen, RED, pygame.Rect(60, 340, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 340, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(60, 395, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 395, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(60, 450, 130, 40))
    pygame.draw.rect(screen, RED, pygame.Rect(210, 450, 130, 40))

    m = True
    selected = 'Start'

    while m:
        screen.blit(text, (60,530))
        screen.blit(text1, (80, 560))

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
                        choose_options()
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

def flap(mode, color):
    """
    Main game - Flappy Bird.
    :param mode: 'easy' or 'hard'
    :param color: color of the bird (red, yellow or blue)
    """
    if mode == 'easy':
        SHOWPIPE = pygame.USEREVENT
        pygame.time.set_timer(SHOWPIPE, 2300)
    elif mode == 'hard':
        SHOWPIPE = pygame.USEREVENT
        pygame.time.set_timer(SHOWPIPE, 1000)
    bird_mov = 0
    game = True
    score = 0
    sound = True

    while True:
        if mode == 'easy':
            screen.blit(background_day, (0, 0))
        elif mode == 'hard':
            screen.blit(background_night, (0,0))
        if color == 'red':
            screen.blit(bird.red_mid, bird.red_rect)
            bird_col = bird.red_rect
        elif color == 'yellow':
            screen.blit(bird.yellow_mid, bird.yellow_rect)
            bird_col = bird.yellow_rect
        elif color == 'blue':
            screen.blit(bird.blue_mid, bird.blue_rect)
            bird_col = bird.blue_rect
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
                        bird_col.center = (50, 270)
                        pipe.list_top.clear()
                        pipe.list_bottom.clear()
                        menu()

        bird_mov += 0.1
        bird_col.centery += bird_mov
        if game:
            if bird_col.centery <= 12:
                bird_col.centery = 12  #sufit
            if mode == 'hard':
                floor.position += -2
                pipe.move(2)
            if mode == 'easy':
                floor.position += -1
                pipe.move(1)
            floor.move()
            if floor.position <= -400:
                floor.position = 0
            for i in pipe.list_bottom:
                if i.centerx == bird_col.centerx - 45:
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
            if mode == 'easy':
                update_easy_high_scores(score)
                show_score(score, pickle.load(open('high_score4.dat', 'rb')), 'high_score')
            elif mode == 'hard':
                update_hard_high_scores(score)
                show_score(score, pickle.load(open('high_score7.dat', 'rb')), 'high_score')

        if pipe.collision(bird_col):
            game = False
            die_sound.play()
        elif bird_col.centery >= 490:
            bird_col.centery = 490
            game = False
            if sound:
                hit_sound.play()
                sound = False

        pygame.display.update()
        fps.tick(100)


menu()
