import pygame
import sys
import random
import math
from pygame import mixer
from ButtonClass import Button
from Testgame import SpaceshipGame

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
#game options
def play():
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    OPTIONS_BACK_GAME = Button(image=None, pos=(500, 660),
                               text_input="BACK TO MENU", font=get_font(45), base_color="Black",
                               hovering_color="Green")
    OPTIONS_BACK_GAME.changeColor(OPTIONS_MOUSE_POS)
    OPTIONS_BACK_GAME.update(WIN)
    game = SpaceshipGame()
    game.run_game()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if OPTIONS_BACK_GAME.checkForInput(OPTIONS_MOUSE_POS):
                main_menu()
def options():
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
                    main_menu()
                if OPTIONS_MUSIC_TURNOFF.checkForInput(OPTIONS_MOUSE_POS):
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)
                if OPTIONS_MUSIC_TURNON.checkForInput(OPTIONS_MOUSE_POS):
                    volume += 0.1
                    pygame.mixer.music.set_volume(volume)
        pygame.display.update()
def main_menu():
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
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
main_menu()