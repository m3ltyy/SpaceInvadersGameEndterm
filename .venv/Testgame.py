import pygame
import random
import math
from pygame import mixer
from ButtonClass import Button

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
BGMenu = pygame.image.load("spaceimage4.jpeg")
mixer.music.load("backgroundmsuic.wav")
clock = pygame.time.Clock()
fps = 60

def get_font(size):
    return pygame.font.Font("font.ttf", size)

class MenuGame:
    def play(self):
        game = SpaceshipGame()
        game.run_game()
    def play_2level(self):
        game = SpaceshipGame2()
        game.run_game()
    def play_3level(self):
        game = SpaceshipGame3()
        game.run_game()
    def options(self):
        volume = 1
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            WIN.blit(BGMenu, (0,0))
            OPTIONS_MUSIC = get_font(25).render(f"Volume:{volume} ", True, "Black")
            OPTIONS_RECT = OPTIONS_MUSIC.get_rect(center=(500, 150))
            WIN.blit(OPTIONS_MUSIC, OPTIONS_RECT)
            OPTIONS_MUSIC_TURNOFF = Button(image=None, pos=(500, 260),
                                  text_input="Music lower", font=get_font(45), base_color="Black", hovering_color="Blue")
            OPTIONS_MUSIC_TURNOFF.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_MUSIC_TURNOFF.update(WIN)
            OPTIONS_MUSIC_TURNON = Button(image=None, pos=(500, 360),
                                           text_input="Music higher", font=get_font(45), base_color="Black",
                                           hovering_color="Blue")
            OPTIONS_MUSIC_TURNON.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_MUSIC_TURNON.update(WIN)
            OPTIONS_BACK = Button(image=None, pos=(500, 660),
                                  text_input="BACK", font=get_font(45), base_color="Black", hovering_color="Green")
            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(WIN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if OPTIONS_MUSIC_TURNOFF.checkForInput(OPTIONS_MOUSE_POS):
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)
                    if OPTIONS_MUSIC_TURNON.checkForInput(OPTIONS_MOUSE_POS):
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)
            pygame.display.update()

    def main_menu(self):
        mixer.music.play()
        while True:
            WIN.blit(BGMenu, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))
            PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(500, 250),
                                 text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(500, 400),
                                    text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(500, 550),
                                 text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
            WIN.blit(MENU_TEXT, MENU_RECT)
            #buttons
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(WIN)
            #menu events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
MainMenuFromGame = MenuGame()
class SpaceshipGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        WIDTH, HEIGHT = 1000, 800
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders Game")
        self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                        text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                        hovering_color="Green")
        self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
        self.OPTIONS_BACK_GAME.update(self.WIN)

        # Interface & music
        self.BG = pygame.transform.scale(pygame.image.load("lastcosmos.png"), (WIDTH, HEIGHT))
        self.score_font = pygame.font.SysFont("arial",30, 'bold')
        self.remaining_enemies_font = pygame.font.SysFont("arial",20)
        self.level_font = pygame.font.SysFont("arial", 30, 'bold')
        self.gameover_font = pygame.font.SysFont("arial",64,'bold')
        self.win_font = pygame.font.SysFont("arial",64,'bold')
        mixer.music.load("backgroundmsuic.wav")
        mixer.music.play(-1)

        self.gameover_flag = False
        self.deletespaceship = True
        self.tp = False
        self.score = 0
        self.score_save = 0

        # Player
        self.spaceshipimage = pygame.image.load("mainship.png")
        self.spaceshipX = 450
        self.spaceshipY = 700
        self.changeX = 0
        self.changeY = 0

        # Laser
        self.laserimage = pygame.image.load("laser.png")
        self.boomimage = pygame.image.load("boomimage.png")
        self.checkSpaceKey = False
        self.laserX = 466
        self.laserY = 670

        # Enemies
        self.number_of_enemies = 6
        self.remaining_enemies = self.number_of_enemies
        self.enemyimage = []
        self.alienX = []
        self.alienY = []
        self.alienspeedX = []
        self.alienspeedY = []
        for i in range(self.number_of_enemies):
            self.enemyimage.append(pygame.image.load("enemy.png"))
            self.alienX.append(random.randint(0, 935))
            self.alienY.append(random.randint(0, 5))
            self.alienspeedX.append(1)
            self.alienspeedY.append(60)

    def interface(self):
        self.WIN.blit(self.BG, (0, 0))
        if not self.gameover_flag and self.remaining_enemies > 0:
            score_label = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            remaining_enemeis_label = self.remaining_enemies_font.render(f"Enemies left: {self.remaining_enemies}", 1,(255, 255, 255))
            Level_label = self.level_font.render(f"Level: 1", True, (255, 255, 255))
            self.WIN.blit(remaining_enemeis_label, (10, 45))
            self.WIN.blit(score_label, (8, 10))
            self.WIN.blit(Level_label, (880, 10))
        elif self.gameover_flag:
            gameover_label = get_font(60).render('GAME OVER', True, (255, 255, 255))
            gameover_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(gameover_label, (240, 350))
            self.WIN.blit(gameover_score_label, (425, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()
        elif self.remaining_enemies == 0:
            tp = True
            win_label = get_font(60).render("YOU WON!", True, (255, 255, 255))
            win_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(win_label, (280, 350))
            self.WIN.blit(win_score_label, (415, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(520, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            self.OPTIONS_NEXT_GAME = Button(image=None, pos=(520, 750),
                                            text_input="NEXT LEVEL", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_NEXT_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_NEXT_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()
                    if self.OPTIONS_NEXT_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.play_2level()

    def gameover(self):
        self.gameover_flag = True
    def enemy(self, x, y, i):
        self.WIN.blit(self.enemyimage[i], (x, y))
    def run_game(self):
        run  = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                # Connecting keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.changeX = -1.2
                    if event.key == pygame.K_RIGHT:
                        self.changeX = 1.2
                    if event.key == pygame.K_UP:
                        self.changeY = -1.2
                    if event.key == pygame.K_DOWN:
                        self.changeY = 1.2
                    if event.key == pygame.K_SPACE:
                        if not self.checkSpaceKey:
                            laserSound = mixer.Sound("laser.wav")
                            laserSound.play()
                            self.checkSpaceKey = True
                            self.laserX = self.spaceshipX + 16
                            self.laserY = self.spaceshipY
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.changeX = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.changeY = 0
            # Borders (width, height)
            if self.spaceshipX <= 0:
                self.spaceshipX = 0
            elif self.spaceshipX >= 936:
                self.spaceshipX = 936
            if self.spaceshipY <= 0:
                self.spaceshipY = 0
            elif self.spaceshipY >= 736:
                self.spaceshipY = 736
            # Laser
            if self.laserY <= 0:
                self.laserY == 670
                self.checkSpaceKey = False
            #Gameover
            for i in range(self.number_of_enemies):
                distance_spaceship = math.sqrt(math.pow(self.alienX[i] - self.spaceshipX, 2) + math.pow(self.alienY[i] - self.spaceshipY, 2))
                if self.alienY[i] > 650 and self.alienY[i] < 850:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                elif distance_spaceship <= 35:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                if self.deletespaceship == False:
                    self.spaceshipY = 15000
            # Changing coordinates of aliens
            for i in range(self.number_of_enemies):
                self.alienX[i] += self.alienspeedX[i]
                if self.alienX[i] <= 0:
                    self.alienspeedX[i] = 1
                    self.alienY[i] += self.alienspeedY[i]
                elif self.alienX[i] >= 936:
                    self.alienspeedX[i] = -1
                    self.alienY[i] += self.alienspeedY[i]
                # Checking if laser hit enemy
                distance = math.sqrt(math.pow(self.laserX - self.alienX[i], 2) + math.pow(self.laserY - self.alienY[i], 2))
                if distance < 27:
                    self.WIN.blit(self.boomimage, (self.laserX - 10, self.laserY - 10))
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.laserY = 670
                    self.checkSpaceKey = False
                    self.score += 10
                    self.score_save = self.score
                    self.alienY[i] = 100000
                    self.remaining_enemies -= 1
                self.enemy(self.alienX[i], self.alienY[i], i)
            # Changing coordinates of main spaceship
            self.spaceshipX += self.changeX
            self.spaceshipY += self.changeY
            # Teleport if win
            if self.remaining_enemies == 0:
                self.spaceshipY = 10000
            # Calling laser & collision
            if self.checkSpaceKey == True:
                self.WIN.blit(self.laserimage, (self.laserX, self.laserY))
                self.laserY -= 2.5
            # Calling functions and interface
            self.WIN.blit(self.spaceshipimage, (self.spaceshipX, self.spaceshipY))
            pygame.display.update()
            self.interface()
        pygame.quit()

class SpaceshipGame2:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        WIDTH, HEIGHT = 1000, 800
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders Game")
        self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                        text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                        hovering_color="Green")
        self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
        self.OPTIONS_BACK_GAME.update(self.WIN)

        # Interface & music
        self.BG = pygame.transform.scale(pygame.image.load("lastcosmos.png"), (WIDTH, HEIGHT))
        self.score_font = pygame.font.SysFont("arial",30, 'bold')
        self.remaining_enemies_font = pygame.font.SysFont("arial",20)
        self.level_font = pygame.font.SysFont("arial", 30, 'bold')
        self.gameover_font = pygame.font.SysFont("arial",64,'bold')
        self.win_font = pygame.font.SysFont("arial",64,'bold')
        mixer.music.load("backgroundmsuic.wav")
        mixer.music.play(-1)

        self.gameover_flag = False
        self.deletespaceship = True
        self.tp = False
        self.score = 0
        self.score_save = 0

        # Player
        self.spaceshipimage = pygame.image.load("mainship.png")
        self.spaceshipX = 450
        self.spaceshipY = 700
        self.changeX = 0
        self.changeY = 0

        # Laser
        self.laserimage = pygame.image.load("laser.png")
        self.boomimage = pygame.image.load("boomimage.png")
        self.checkSpaceKey = False
        self.laserX = 466
        self.laserY = 670

        # Enemies
        self.number_of_enemies = 10
        self.remaining_enemies = self.number_of_enemies
        self.enemyimage = []
        self.alienX = []
        self.alienY = []
        self.alienspeedX = []
        self.alienspeedY = []
        for i in range(self.number_of_enemies):
            self.enemyimage.append(pygame.image.load("enemy2.png"))
            self.alienX.append(random.randint(0, 935))
            self.alienY.append(random.randint(0, 5))
            self.alienspeedX.append(1)
            self.alienspeedY.append(60)

    def interface(self):
        self.WIN.blit(self.BG, (0, 0))
        if not self.gameover_flag and self.remaining_enemies > 0:
            score_label = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            remaining_enemeis_label = self.remaining_enemies_font.render(f"Enemies left: {self.remaining_enemies}", 1,(255, 255, 255))
            Level_label = self.level_font.render(f"Level: 2", True, (255, 255, 255))
            self.WIN.blit(remaining_enemeis_label, (10, 45))
            self.WIN.blit(score_label, (8, 10))
            self.WIN.blit(Level_label, (880, 10))
        elif self.gameover_flag:
            gameover_label = get_font(60).render('GAME OVER', True, (255, 255, 255))
            gameover_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(gameover_label, (240, 350))
            self.WIN.blit(gameover_score_label, (425, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()
        elif self.remaining_enemies == 0:
            tp = True
            win_label = get_font(60).render("YOU WON!", True, (255, 255, 255))
            win_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(win_label, (280, 350))
            self.WIN.blit(win_score_label, (415, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(520, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            self.OPTIONS_NEXT_GAME = Button(image=None, pos=(520, 750),
                                            text_input="NEXT LEVEL", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_NEXT_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_NEXT_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()
                    if self.OPTIONS_NEXT_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.play_3level()

    def gameover(self):
        self.gameover_flag = True
    def enemy(self, x, y, i):
        self.WIN.blit(self.enemyimage[i], (x, y))
    def run_game(self):
        run  = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                # Connecting keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.changeX = -1.2
                    if event.key == pygame.K_RIGHT:
                        self.changeX = 1.2
                    if event.key == pygame.K_UP:
                        self.changeY = -1.2
                    if event.key == pygame.K_DOWN:
                        self.changeY = 1.2
                    if event.key == pygame.K_SPACE:
                        if not self.checkSpaceKey:
                            laserSound = mixer.Sound("laser.wav")
                            laserSound.play()
                            self.checkSpaceKey = True
                            self.laserX = self.spaceshipX + 16
                            self.laserY = self.spaceshipY
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.changeX = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.changeY = 0
            # Borders (width, height)
            if self.spaceshipX <= 0:
                self.spaceshipX = 0
            elif self.spaceshipX >= 936:
                self.spaceshipX = 936
            if self.spaceshipY <= 0:
                self.spaceshipY = 0
            elif self.spaceshipY >= 736:
                self.spaceshipY = 736
            # Laser
            if self.laserY <= 0:
                self.laserY == 670
                self.checkSpaceKey = False
            #Gameover
            for i in range(self.number_of_enemies):
                distance_spaceship = math.sqrt(math.pow(self.alienX[i] - self.spaceshipX, 2) + math.pow(self.alienY[i] - self.spaceshipY, 2))
                if self.alienY[i] > 650 and self.alienY[i] < 850:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                elif distance_spaceship <= 35:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                if self.deletespaceship == False:
                    self.spaceshipY = 15000
            # Changing coordinates of aliens
            for i in range(self.number_of_enemies):
                self.alienX[i] += self.alienspeedX[i]
                if self.alienX[i] <= 0:
                    self.alienspeedX[i] = 1
                    self.alienY[i] += self.alienspeedY[i]
                elif self.alienX[i] >= 936:
                    self.alienspeedX[i] = -1
                    self.alienY[i] += self.alienspeedY[i]
                # Checking if laser hit enemy
                distance = math.sqrt(math.pow(self.laserX - self.alienX[i], 2) + math.pow(self.laserY - self.alienY[i], 2))
                if distance < 27:
                    self.WIN.blit(self.boomimage, (self.laserX - 10, self.laserY - 10))
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.laserY = 670
                    self.checkSpaceKey = False
                    self.score += 10
                    self.score_save = self.score
                    self.alienY[i] = 100000
                    self.remaining_enemies -= 1
                self.enemy(self.alienX[i], self.alienY[i], i)
            # Changing coordinates of main spaceship
            self.spaceshipX += self.changeX
            self.spaceshipY += self.changeY
            # Teleport if win
            if self.remaining_enemies == 0:
                self.spaceshipY = 10000
            # Calling laser & collision
            if self.checkSpaceKey == True:
                self.WIN.blit(self.laserimage, (self.laserX, self.laserY))
                self.laserY -= 2.5
            # Calling functions and interface
            self.WIN.blit(self.spaceshipimage, (self.spaceshipX, self.spaceshipY))
            pygame.display.update()
            self.interface()
        pygame.quit()

class SpaceshipGame3:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        WIDTH, HEIGHT = 1000, 800
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders Game")
        self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                        text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                        hovering_color="Green")
        self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
        self.OPTIONS_BACK_GAME.update(self.WIN)

        # Interface & music
        self.BG = pygame.transform.scale(pygame.image.load("lastcosmos.png"), (WIDTH, HEIGHT))
        self.score_font = pygame.font.SysFont("arial",30, 'bold')
        self.remaining_enemies_font = pygame.font.SysFont("arial",20)
        self.level_font = pygame.font.SysFont("arial", 30, 'bold')
        self.gameover_font = pygame.font.SysFont("arial",64,'bold')
        self.win_font = pygame.font.SysFont("arial",64,'bold')
        mixer.music.load("backgroundmsuic.wav")
        mixer.music.play(-1)

        self.gameover_flag = False
        self.deletespaceship = True
        self.tp = False
        self.score = 0
        self.score_save = 0

        # Player
        self.spaceshipimage = pygame.image.load("mainship.png")
        self.spaceshipX = 450
        self.spaceshipY = 700
        self.changeX = 0
        self.changeY = 0

        # Laser
        self.laserimage = pygame.image.load("laser.png")
        self.boomimage = pygame.image.load("boomimage.png")
        self.checkSpaceKey = False
        self.laserX = 466
        self.laserY = 670

        # Enemies
        self.number_of_enemies = 15
        self.remaining_enemies = self.number_of_enemies
        self.enemyimage = []
        self.alienX = []
        self.alienY = []
        self.alienspeedX = []
        self.alienspeedY = []
        for i in range(self.number_of_enemies):
            self.enemyimage.append(pygame.image.load("enemy3.png"))
            self.alienX.append(random.randint(0, 935))
            self.alienY.append(random.randint(0, 5))
            self.alienspeedX.append(1)
            self.alienspeedY.append(60)

    def interface(self):
        self.WIN.blit(self.BG, (0, 0))
        if not self.gameover_flag and self.remaining_enemies > 0:
            score_label = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
            remaining_enemeis_label = self.remaining_enemies_font.render(f"Enemies left: {self.remaining_enemies}", 1,(255, 255, 255))
            Level_label = self.level_font.render(f"Level: 3", True, (255, 255, 255))
            self.WIN.blit(remaining_enemeis_label, (10, 45))
            self.WIN.blit(score_label, (8, 10))
            self.WIN.blit(Level_label, (880, 10))
        elif self.gameover_flag:
            gameover_label = get_font(60).render('GAME OVER', True, (255, 255, 255))
            gameover_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(gameover_label, (240, 350))
            self.WIN.blit(gameover_score_label, (425, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()
        elif self.remaining_enemies == 0:
            tp = True
            win_label = get_font(60).render("YOU WON!", True, (255, 255, 255))
            win_score_label = get_font(20).render(f"Score: {self.score_save}", True, (255, 255, 255))
            self.WIN.blit(win_label, (280, 350))
            self.WIN.blit(win_score_label, (415, 430))
            self.OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK_GAME = Button(image=None, pos=(520, 660),
                                            text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                                            hovering_color="Green")
            self.OPTIONS_BACK_GAME.changeColor(self.OPTIONS_MOUSE_POS)
            self.OPTIONS_BACK_GAME.update(self.WIN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK_GAME.checkForInput(self.OPTIONS_MOUSE_POS):
                        MainMenuFromGame.main_menu()


    def gameover(self):
        self.gameover_flag = True
    def enemy(self, x, y, i):
        self.WIN.blit(self.enemyimage[i], (x, y))
    def run_game(self):
        run  = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                # Connecting keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.changeX = -1.2
                    if event.key == pygame.K_RIGHT:
                        self.changeX = 1.2
                    if event.key == pygame.K_UP:
                        self.changeY = -1.2
                    if event.key == pygame.K_DOWN:
                        self.changeY = 1.2
                    if event.key == pygame.K_SPACE:
                        if not self.checkSpaceKey:
                            laserSound = mixer.Sound("laser.wav")
                            laserSound.play()
                            self.checkSpaceKey = True
                            self.laserX = self.spaceshipX + 16
                            self.laserY = self.spaceshipY
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.changeX = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.changeY = 0
            # Borders (width, height)
            if self.spaceshipX <= 0:
                self.spaceshipX = 0
            elif self.spaceshipX >= 936:
                self.spaceshipX = 936
            if self.spaceshipY <= 0:
                self.spaceshipY = 0
            elif self.spaceshipY >= 736:
                self.spaceshipY = 736
            # Laser
            if self.laserY <= 0:
                self.laserY == 670
                self.checkSpaceKey = False
            #Gameover
            for i in range(self.number_of_enemies):
                distance_spaceship = math.sqrt(math.pow(self.alienX[i] - self.spaceshipX, 2) + math.pow(self.alienY[i] - self.spaceshipY, 2))
                if self.alienY[i] > 650 and self.alienY[i] < 850:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                elif distance_spaceship <= 35:
                    for j in range(self.number_of_enemies):
                        self.alienY[j] = 20000
                    self.gameover()
                    self.deletespaceship = False
                    break
                if self.deletespaceship == False:
                    self.spaceshipY = 15000
            # Changing coordinates of aliens
            for i in range(self.number_of_enemies):
                self.alienX[i] += self.alienspeedX[i]
                if self.alienX[i] <= 0:
                    self.alienspeedX[i] = 1
                    self.alienY[i] += self.alienspeedY[i]
                elif self.alienX[i] >= 936:
                    self.alienspeedX[i] = -1
                    self.alienY[i] += self.alienspeedY[i]
                # Checking if laser hit enemy
                distance = math.sqrt(math.pow(self.laserX - self.alienX[i], 2) + math.pow(self.laserY - self.alienY[i], 2))
                if distance < 27:
                    self.WIN.blit(self.boomimage, (self.laserX - 10, self.laserY - 10))
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.laserY = 670
                    self.checkSpaceKey = False
                    self.score += 10
                    self.score_save = self.score
                    self.alienY[i] = 100000
                    self.remaining_enemies -= 1
                self.enemy(self.alienX[i], self.alienY[i], i)
            # Changing coordinates of main spaceship
            self.spaceshipX += self.changeX
            self.spaceshipY += self.changeY
            # Teleport if win
            if self.remaining_enemies == 0:
                self.spaceshipY = 10000
            # Calling laser & collision
            if self.checkSpaceKey == True:
                self.WIN.blit(self.laserimage, (self.laserX, self.laserY))
                self.laserY -= 2.5
            # Calling functions and interface
            self.WIN.blit(self.spaceshipimage, (self.spaceshipX, self.spaceshipY))
            pygame.display.update()
            self.interface()
        pygame.quit()

if __name__ == "__main__":
    menu = MenuGame()
    menu.main_menu()
