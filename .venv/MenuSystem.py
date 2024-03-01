import pygame
import sys
from ButtonClass import Button

pygame.init()
SCREEN = pygame.display.set_mode((1000, 800))  # Изменено разрешение экрана
pygame.display.set_caption("Menu")
BG = pygame.image.load("spaceimage.jpg")

def get_font(size):
    return pygame.font.Font("font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 260))  # Изменены координаты текста
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        PLAY_BACK = Button(image=None, pos=(500, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(500, 260))  # Изменены координаты текста
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(500, 460), text_input="BACK", font=get_font(75),
                              base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")  # Изменен размер текста
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))  # Изменены координаты текста

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(500, 250),
                             text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")  # Изменен размер текста
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(500, 400),
                                text_input="OPTIONS", font=get_font(60), base_color="#d7fcd4", hovering_color="White")  # Изменен размер текста
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(500, 550),
                             text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")  # Изменен размер текста
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
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
