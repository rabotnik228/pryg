import random
import pygame
import win32con
from win32api import GetSystemMetrics
import win32api
import librosa
from record_database import *
from design import load_image
from moving_catcher import Player
import os
import sys
from tkinter import *
from tkinter import ttk
import consts
import pygame.gfxdraw
from numba import jit
import ctypes
import threading

pygame.init()
screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)))

from fruti import Fruits

runnp = True
if __name__ == '__main__':

    def pointInRectanlge(px, py, rw, rh, rx, ry):
        if px > rx and px < rx + rw:
            if py > ry and py < ry + rh:
                return True
        return False


    class Button:
        def __init__(self, text, translation, width, height, pos, elevation, buttons):
            self.pressed = False
            self.elevation = elevation
            self.dynamic_elecation = elevation
            self.original_y_pos = pos[1]
            self.top_rect = pygame.Rect(pos, (width, height))
            self.top_color = '#475F77'
            self.translation = translation
            self.bottom_rect = pygame.Rect(pos, (width, height))
            self.bottom_color = '#354B5E'
            self.gui_font = pygame.font.Font(None, 30)
            self.text = text
            self.text_surf = self.gui_font.render(self.text, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
            buttons.append(self)

        def change_text(self, newtext):
            self.text_surf = self.gui_font.render(newtext, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
            self.text = newtext

        def draw(self, screen):
            # elevation logic
            self.top_rect.y = self.original_y_pos - self.dynamic_elecation
            self.text_rect.center = self.top_rect.center

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

            pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
            pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
            screen.blit(self.text_surf, self.text_rect)

        def check_click(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.top_rect.collidepoint(mouse_pos):
                self.top_color = '#D74B4B'
                if pygame.mouse.get_pressed()[0]:
                    self.dynamic_elecation = 0
                    self.pressed = True
                else:
                    self.dynamic_elecation = self.elevation
                    if self.pressed == True:
                        print('click')
                        self.pressed = False
                        return True
            else:
                self.dynamic_elecation = self.elevation
                self.top_color = '#475F77'

        def get_name(self):
            return self.text


    class Slider:
        def __init__(self, position: tuple, upperValue: int = 10, sliderWidth: int = 30,
                     text: str = "Text slider",
                     outlineSize: tuple = (300, 100)) -> None:
            self.position = position
            self.outlineSize = outlineSize
            self.text = text
            self.sliderWidth = sliderWidth
            self.upperValue = upperValue

        def getValue(self) -> float:
            return self.sliderWidth / (self.outlineSize[0] / self.upperValue)

        def render(self, on, display: pygame.display) -> None:
            if on:
                pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1],
                                                      self.outlineSize[0], self.outlineSize[1]), 3)

                pygame.draw.rect(display, (0, 0, 0), (self.position[0], self.position[1],
                                                      self.sliderWidth, self.outlineSize[1] - 10))

                self.font = pygame.font.Font(pygame.font.get_default_font(), int((15 / 100) * self.outlineSize[1]))

                valueSurf = self.font.render(f"{self.text}: {round(self.getValue())}", True, (255, 0, 0))

                textx = self.position[0] + (self.outlineSize[0] / 2) - (valueSurf.get_rect().width / 2)
                texty = self.position[1] + (self.outlineSize[1] / 2) - (valueSurf.get_rect().height / 2)

                display.blit(valueSurf, (textx, texty))

        def changeValue(self) -> None:
            mousePos = pygame.mouse.get_pos()
            if pointInRectanlge(mousePos[0], mousePos[1]
                    , self.outlineSize[0], self.outlineSize[1], self.position[0], self.position[1]):
                if pygame.mouse.get_pressed()[0]:
                    self.sliderWidth = mousePos[0] - self.position[0]

                    if self.sliderWidth < 1:
                        self.sliderWidth = 0
                    if self.sliderWidth > self.outlineSize[0]:
                        self.sliderWidth = self.outlineSize[0]


    class Checkbox:
        def __init__(self, screen, pos, value):
            self.image = load_image('gal.png')
            self.x, self.y = pos[0], pos[1]
            self.size = 100, 85
            self.current_value = value
            self.screen = screen
            self.rect_but = pygame.Rect((self.x, self.y), self.size)

        def render(self, on=True):
            if on:
                pygame.draw.rect(self.screen, (0, 0, 0), self.rect_but, width=5, border_radius=15)
                if self.current_value:
                    screen.blit(self.image, (self.x, self.y + 6))

        def change_value(self):
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if self.rect_but.collidepoint(mouse_pos):
                if mouse_click[0]:
                    self.current_value = not self.current_value

        def get_value(self):
            return self.current_value


    class RadioButton:
        def __init__(self, screen, pos, value, radiobuttonsGroup):
            self.image = load_image('gal.png')
            self.x, self.y = pos[0], pos[1]
            self.size = 100, 85
            self.current_value = value
            self.screen = screen
            self.rect_but = pygame.Rect((self.x, self.y), self.size)
            self.l = radiobuttonsGroup
            radiobuttonsGroup.append(self)

        def render(self, on=True):
            if on:
                pygame.draw.rect(self.screen, (0, 0, 0), self.rect_but, width=5, border_radius=15)
                if self.current_value:
                    screen.blit(self.image, (self.x, self.y + 6))

        def change_value(self, second_radio_button):
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if self.rect_but.collidepoint(mouse_pos):
                if mouse_click[0]:
                    self.current_value = not self.current_value
                    second_radio_button.current_value = not second_radio_button.current_value

        def get_value(self):
            return self.current_value


    @jit()
    def notes_seconds(audio):
        y, sr = librosa.load(audio)
        notes = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        return notes


    @jit()
    def detect_silent(audio):
        y, sr = librosa.load(audio)
        yt, index = librosa.effects.trim(y)
        return [librosa.get_duration(y), librosa.get_duration(yt)]


    def get_active_notes(list_of_onsets, current_time):
        active_notes = []
        for onset in list_of_onsets:
            time_before_appearance = onset - current_time
            if time_before_appearance < 0:
                continue
            elif time_before_appearance <= consts.note_offset:
                active_notes.append(onset)
            elif time_before_appearance > consts.note_offset:
                break
        return active_notes


    def current_position():
        return pygame.mixer.music.get_pos() / 1000


    def score_render(score):
        button_font = pygame.font.SysFont('resourses/koblenz-serial-extralight-regular.ttf', 50)
        render = button_font.render(str(score), 0, (0, 250, 0))
        screen.blit(render, (GetSystemMetrics(0) - 200, GetSystemMetrics(1) - 100))


    def combo_render(combo, player_pos, screen):
        font_for_combo = pygame.font.SysFont('resourses/koblenz-serial-extralight-regular.ttf', 45)
        combo_rend = font_for_combo.render(str(combo), 0, (255, 255, 255))
        our_pos = (player_pos[0] + 75, player_pos[1] + 183)
        screen.blit(combo_rend, (500, 500))


    def pause_render(screen, background):
        contin = load_image(consts.pause_images['continue'])
        retry = load_image(consts.pause_images['retry'])
        back = load_image(consts.pause_images['back'])
        rectang_contin = pygame.Rect(0, 0, 60, 60)
        rectang_contin.center = GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2 - 200
        rectang_retry = pygame.Rect(0, 0, 60, 60)
        rectang_retry.center = GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2
        rectang_back = pygame.Rect(0, 0, 60, 60)
        rectang_back.center = GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2 + 200
        sounds = (pygame.mixer.Sound('resourses/music/pause-continue-click.mp3'), pygame.mixer.Sound('resourses/music'
                                                                                                     '/pause-retry'
                                                                                                     '-click.mp3'),
                  pygame.mixer.Sound('resourses/music/pause-back-click.mp3'))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        background.set_alpha(100)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(contin, (GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2 - 200))
        screen.blit(retry, (GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2))
        screen.blit(back, (GetSystemMetrics(0) / 2, GetSystemMetrics(1) / 2 + 200))
        pygame.draw.rect(screen, (0, 0, 0), rectang_contin)
        pygame.draw.rect(screen, (0, 0, 0), rectang_retry)
        pygame.draw.rect(screen, (0, 0, 0), rectang_back)
        if rectang_contin.collidepoint(mouse_pos):
            print('c')
            if mouse_click[0]:
                sounds[0].play()
                return 'con'
        if rectang_retry.collidepoint(mouse_pos):
            print('r')
            if mouse_click[0]:
                sounds[1].play()
                return 'retry'
        if rectang_back.collidepoint(mouse_pos):
            print('b')
            if mouse_click[0]:
                sounds[2].play()
                return 'back'
        pygame.display.flip()


    def create_folder():
        newpath = r'C:\pryg'
        if not os.path.exists(newpath):
            os.makedirs(newpath)


    def create_f():
        newpath = r'C:\pryg\.beatmaps'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ret = ctypes.windll.kernel32.SetFileAttributesW(newpath, FILE_ATTRIBUTE_HIDDEN)


    def create_settings_file():
        open(r'C:\pryg\settings.txt', 'a').close()
        newpath = 'pryg/settings.txt'
        if not os.path.exists(newpath):
            win32api.SetFileAttributes(r'C:\pryg\settings.txt', win32con.FILE_ATTRIBUTE_HIDDEN)


    def set_offset(value):
        consts.note_offset = value


    def menu(screen):
        create_folder()
        create_f()
        create_settings_file()
        global maps
        maps = CreateMpDb()
        global all_sprites
        list_of_names = maps.all_maps()
        all_sprites = pygame.sprite.Group()
        global sprite_of_arrow
        sprite_of_arrow = pygame.sprite.Sprite()
        sprite_of_arrow.image = load_image("gachi_arrow.png")
        sprite_of_arrow.rect = sprite_of_arrow.image.get_rect()
        all_sprites.add(sprite_of_arrow)
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        global snow_list
        snow_list = []
        buttons = []
        for i in range(100):
            snow_list.append([random.randrange(0, GetSystemMetrics(0)), random.randrange(0, GetSystemMetrics(1)),
                              random.randrange(1, 5)])
        play_sound()
        menu_trigger = True
        menu_picture = pygame.image.load('resourses/lol2.jpg').convert_alpha()
        label_font = pygame.font.SysFont('Arial', 400)

        start = Button("Start", "Start", 400, 150, (200, 500), 5, buttons)
        exitt = Button("Exit", "Exit?", 400, 150, (200, 700), 5, buttons)
        options = Button("Options", "Options", 400, 150, (200, 900), 5, buttons)
        alpha = 255
        direction = 2
        run = True
        while menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    sys.exit()
            screen.blit(menu_picture, (0, 0))
            cursor(sprite_of_arrow)
            all_sprites.draw(screen)
            for b in buttons:
                b.draw(screen)

            color = random.randrange(60)
            label = label_font.render('PRYG!', 1, (color, color, color))
            screen.blit(label, (15, -30))
            snow(screen, snow_list)
            if start.check_click():
                play_sound(music='start')
                play_sound(stop=True)
                while run:
                    alpha -= direction + 5
                    menu_picture.set_alpha(alpha)
                    screen.fill((0, 0, 0))
                    screen.blit(menu_picture, (0, 0))
                    if alpha > 60:
                        for b in buttons:
                            b.draw(screen)
                        color = random.randrange(60)
                        label = label_font.render('PRYG!', 1, (color, color, color))
                        screen.blit(label, (15, -30))
                    pygame.display.flip()
                    if alpha <= 20:
                        pygame.time.delay(200)
                        run = False
                menu_trigger = False
                snow_list = []
                slider = None
                sett = main_window(screen)
                return sett
            if exitt.check_click():
                play_sound(stop=True)
                play_sound(music='exit')
                while True:
                    alpha -= direction
                    menu_picture.set_alpha(alpha)
                    screen.fill((0, 0, 0))
                    screen.blit(menu_picture, (0, 0))
                    for b in buttons:
                        b.draw(screen)
                    color = random.randrange(60)
                    label = label_font.render('PRYG!', 1, (color, color, color))
                    screen.blit(label, (15, -30))
                    pygame.display.flip()
                    if alpha <= 80:
                        quit()
                        sys.exit()
            if options.check_click():
                options_window(screen, menu_picture)
            pygame.display.flip()
            clock.tick(20)


    def cursor(sprite_of_arrow):
        if pygame.mouse.get_focused():
            coords = pygame.mouse.get_pos()
            sprite_of_arrow.rect.x = coords[0]
            sprite_of_arrow.rect.y = coords[1]


    def main_window(screen):
        main_window_trigger = True
        menu_picture = pygame.image.load('resourses/lol2.jpg').convert()
        add_song_image = pygame.image.load('resourses/plus.png').convert_alpha()
        buttons = []
        songs = []
        list_of_names = maps.all_maps()
        print(list_of_names)
        back = Button("Exit", "Exit?", 400, 150, (0, GetSystemMetrics(1) - 200), 5, buttons)
        rectang = pygame.Rect(0, 0, 60, 60)
        rectang.center = GetSystemMetrics(0) - 60, 60
        song = Button('nostalgic', 'nostalgic', 400, 150, (GetSystemMetrics(0) - 500, 150), 5, songs)
        song1 = Button('tomydream', 'tomydream', 400, 150, (GetSystemMetrics(0) - 500, 350), 5, songs)
        song2 = Button('rickroll', 'rickroll', 400, 150, (GetSystemMetrics(0) - 500, 550), 5, songs)
        song3 = Button('Hajimari_no_Toki', 'Hajimari_no_Toki', 400, 150, (GetSystemMetrics(0) - 500, 750), 5, songs)
        up = Button('up', 'up', 50, 50, (GetSystemMetrics(0) - 250, 50), 5, buttons)
        down = Button('down', 'down', 50, 50, (GetSystemMetrics(0) - 250, GetSystemMetrics(1) - 50), 5, buttons)
        while main_window_trigger:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
            screen.blit(menu_picture, (0, 0))
            all_sprites.draw(screen)
            cursor(sprite_of_arrow)
            pygame.draw.rect(screen, (0, 0, 0), rectang)
            screen.blit(add_song_image, add_song_image.get_rect(center=rectang.center))
            for b in buttons:
                b.draw(screen)
            for song in songs:
                song.draw(screen)
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if back.check_click():
                play_sound(music='back')
                main_window_trigger = False
                return menu(screen)
            if up.check_click():
                if len(list_of_names) > 4:
                    if consts.current_index != -(len(list_of_names) + 1):
                        songs[0].change_text(list_of_names[consts.current_index][0])
                        songs[1].change_text(list_of_names[(consts.current_index + 1) % len(list_of_names)][0])
                        songs[2].change_text(list_of_names[(consts.current_index + 2) % len(list_of_names)][0])
                        songs[3].change_text(list_of_names[(consts.current_index + 3) % len(list_of_names)][0])
                        consts.current_index -= 1
                    else:
                        consts.current_index = 0
            if down.check_click():
                if len(list_of_names) > 4:
                    if consts.current_index != len(list_of_names):
                        songs[0].change_text(list_of_names[consts.current_index][0])
                        songs[1].change_text(list_of_names[(consts.current_index + 1) % len(list_of_names)][0])
                        songs[2].change_text(list_of_names[(consts.current_index + 2) % len(list_of_names)][0])
                        songs[3].change_text(list_of_names[(consts.current_index + 3) % len(list_of_names)][0])
                        consts.current_index += 1
                    else:
                        consts.current_index = 0
            for song in songs:
                if song.check_click():
                    play_sound(music='start')
                    main_window_trigger = False
                    a = maps.open_a_song(song.get_name())
                    print(a, maps.get_song_name(a[0][0]))
                    return a, maps.get_song_name(a[0][0])
            if rectang.collidepoint(mouse_pos):
                if mouse_click[0]:
                    download_window()
            pygame.display.flip()


    def options_window(screen, fon):
        options_trigger = True
        font = pygame.font.Font('resourses/210 Gulim 070.ttf', 40)
        sprite_of_arrow = pygame.sprite.Sprite()
        sprite_of_arrow.image = load_image("gachi_arrow.png")
        sprite_of_arrow.rect = sprite_of_arrow.image.get_rect()
        all_sprites1 = pygame.sprite.Group()
        all_sprites1.add(sprite_of_arrow)
        buttons = []
        plus = Checkbox(screen, (100, 100), True)
        back = Button("Exit", "Exit?", 400, 150, (0, GetSystemMetrics(1) - 200), 5, buttons)
        slider_for_offset = Slider((250, 100), 300, text='note_offset', sliderWidth=0)
        slider_for_back = Slider((100, 300), 255, text='background', sliderWidth=0)
        check_for_snow = Checkbox(screen, (100, 500), True)
        check_for_fps = Checkbox(screen, (100, 700), True)
        while options_trigger:
            pygame.event.get()
            screen.blit(fon, (0, 0))
            cursor(sprite_of_arrow)
            for i in buttons:
                i.draw(screen)
            plus.render()
            screen.blit(font.render("Setting up an offset", 1, (255, 255, 255)), (600, 150))
            screen.blit(font.render("Setting up a backgroung", 1, (255, 255, 255)), (450, 350))
            screen.blit(font.render("Fps render", 1, (255, 255, 255)), (350, 500))
            screen.blit(font.render("Snow render", 1, (255, 255, 255)), (250, 700))
            slider_for_offset.render(True, screen)
            slider_for_back.render(True, screen)
            check_for_snow.render()
            check_for_fps.render()
            if back.check_click():
                check_for_snow.render(on=False)
                check_for_fps.render(on=False)
                slider_for_offset.render(False, screen)
                slider_for_back.render(False, screen)
                options_trigger = False
                return menu(screen)
            check_for_snow.change_value()
            check_for_fps.change_value()
            slider_for_offset.changeValue()
            slider_for_back.changeValue()
            plus.change_value()
            all_sprites1.draw(screen)
            all_sprites1.update()
            pygame.display.flip()


    def play_sound(stop=False, music='', pause=False):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        start = pygame.mixer.Sound('resourses/music/menu-play-click.MP3')
        exit = pygame.mixer.Sound('resourses/music/menu-exit-click.mp3')
        back = pygame.mixer.Sound('resourses/music/menu-back-click.mp3')
        pause_continue = pygame.mixer.Sound('resourses/music/pause-continue-click.mp3')
        pause_retry = pygame.mixer.Sound('resourses/music/pause-retry-click.mp3')
        pause_back = pygame.mixer.Sound('resourses/music/pause-back-click.mp3')
        if music == 'MariannE.wav':
            pygame.mixer.music.load('MariannE.wav')
            pygame.mixer.music.play()
            if pause:
                pygame.mixer.pause()
            elif not pause:
                pygame.mixer.unpause()
        elif music == 'back':
            back.play()
        elif music == 'exit':
            exit.play()
        elif music == 'start':
            start.play()
        elif music == 'pause_back':
            pause_back.play()
        elif music == 'pause_continue':
            pause_continue.play()
        elif music == 'pause_retry':
            pause_retry.play()
        else:
            pygame.mixer.music.load('resourses/music/fon.mp3')
            pygame.mixer.music.play(10)
        if stop:
            pygame.mixer.music.unload()


    def results(screen, score, rank):
        rank = "%0.2f" % rank
        rank = float(rank)
        font = pygame.font.SysFont('Arial', 23)
        back = font.render('Back', 1, pygame.Color('green'))
        button_back = pygame.Rect(0, 0, 400, 150)
        button_back.center = 200, GetSystemMetrics(1) - 75
        get_score = font.render(str(score), 1, (255, 255, 255))
        get_accuracy = font.render(str(rank), 1, (255, 255, 255))
        result_picture = pygame.image.load('resourses/для результатов.png').convert_alpha()
        was_played = False
        screen.blit(result_picture, (GetSystemMetrics(0) / 2 - 400, GetSystemMetrics(1) / 2 - 300))
        pygame.draw.rect(screen, 'black', button_back, border_radius=25, width=10)
        screen.blit(back, (button_back.centerx - 130, button_back.centery - 70))
        screen.blit(get_score, (GetSystemMetrics(0) / 2 - 300, GetSystemMetrics(1) / 2 - 300))
        screen.blit(get_accuracy, (GetSystemMetrics(0) / 2 - 200, GetSystemMetrics(1) / 2 - 300))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_back.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'black', button_back, border_radius=25)
            screen.blit(back, (button_back.centerx - 130, button_back.centery - 70))
            if mouse_click[0]:
                running = False
                play_sound(music='start')
                return 'exit'
        if rank in consts.RANKS['S'][0]:
            screen.blit(load_image(consts.RANKS['S'][1]),
                        (GetSystemMetrics(0) / 2 - 500, GetSystemMetrics(1) / 2 - 500))
            if not was_played:
                pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.unload()
                was_played = True
        elif rank in consts.RANKS['A'][0]:
            screen.blit(load_image(consts.RANKS['A'][1]),
                        (GetSystemMetrics(0) / 2 - 500, GetSystemMetrics(1) / 2 - 500))
            if not was_played:
                pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.unload()
                was_played = True
        elif rank in consts.RANKS['B'][0]:
            screen.blit(load_image(consts.RANKS['B'][1]),
                        (GetSystemMetrics(0) / 2 - 500, GetSystemMetrics(1) / 2 - 500))
            if not was_played:
                pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.unload()
                was_played = True
        elif rank in consts.RANKS['C'][0]:
            screen.blit(load_image(consts.RANKS['C'][1]),
                        (GetSystemMetrics(0) / 2 - 500, GetSystemMetrics(1) / 2 - 500))
            if not was_played:
                pygame.mixer.music.load('resourses/music/sectionfail.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.unload()
                was_played = True
        elif rank in consts.RANKS['D'][0]:
            screen.blit(load_image(consts.RANKS['D'][1]),
                        (GetSystemMetrics(0) / 2 - 500, GetSystemMetrics(1) / 2 - 500))
            if not was_played:
                pygame.mixer.music.load('resourses/music/sectionfail.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.unload()
                was_played = True
        pygame.display.flip()


    def fps_render(clock, screen, on=True):
        button_font = pygame.font.SysFont('Arial', 20)
        display_fps = str(int(clock.get_fps()))
        render = button_font.render(display_fps, 0, (0, 250, 0))
        screen.blit(render, (GetSystemMetrics(0) - 20, GetSystemMetrics(1) - 30))


    def snow(screen, snow_list, alpha=None):
        speed = 10
        for snowy in snow_list:
            snowy[1] += speed
            if snowy[1] > GetSystemMetrics(1):
                snowy[1] = 0

        for snowy in snow_list:
            pygame.draw.circle(screen, (255, 255, 255), (snowy[0], snowy[1]), snowy[2])


    def check_for_unrechtable():
        """for download_window
         проверка на пустоту и неправильный путь"""


    def create_beatmap(name, audio):
        with open(f'C:/pryg/.beatmaps/beat_map_{name}.txt', 'w') as f:
            n = notes_seconds(audio)
            lit = [list(n)[x] for x in range(0, len(list(n)))]
            lit = list(map(str, lit))
            n2 = ' '.join(lit)
            f.write(n2)


    def open_beatmap(name):
        with open(f'C:/pryg/.beatmaps/beat_map_{name}.txt', 'r') as f:
            nots = list(map(float, f.readline().split(' ')))
            return nots


    def download_window():
        window = Tk()
        window.title("Добавление песни")
        window.geometry('400x250')
        combo = ttk.Combobox(window)
        combo['values'] = ("Easy", "Normal", "Hard")
        combo.current(1)
        combo.grid(column=0, row=0)
        rad1 = Radiobutton(window, text='Сгенерировать beatmap', value=1)
        rad2 = Radiobutton(window, text='Создать beatmap', value=2)
        rad1.grid(column=0, row=3)
        rad2.grid(column=0, row=4)
        lbl = Label(window, text="Название карты")
        lbl.grid(column=0, row=1)
        txt = Entry(window, width=20)
        txt.grid(column=1, row=1)
        lbl2 = Label(window, text="Путь или имя файла с песней")
        lbl2.grid(column=0, row=2)
        txt2 = Entry(window, width=20)
        txt2.grid(column=1, row=2)
        but = Button(window, text="А", clicked=create_beatmap(txt2.get()))
        but.grid(column=0, row=5)
        window.mainloop()


    def sorting(key=None):
        pass


    def fun3_2_1(fon):
        clock = pygame.time.Clock()
        counter, text = 3, '3'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        font = pygame.font.SysFont('Consolas', 50)
        run = True
        while run:
            for e in pygame.event.get():
                if e.type == pygame.USEREVENT:
                    counter -= 1
                    text = str(counter).rjust(3) if counter > 0 else 'START!'
                    if counter == 0:
                        run = False
            screen.blit(fon, (0, 0))
            screen.blit(font.render(text, True, (random.choice(range(0, 255)), random.choice(range(0, 255)),
                                                 random.choice(range(0, 255)))), (GetSystemMetrics(0) / 2,
                                                                                  GetSystemMetrics(1) / 2))
            pygame.display.flip()
            clock.tick(60)


    def show_gif(screen):
        endless = pygame.mixer.Sound('resourses/music/бесконечность не предел.mp3')
        clock = pygame.time.Clock()
        loadning_mess = [pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading.', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading..', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading...', 1, (255, 255, 255))]
        currentFrame = 0
        endless.play()
        while runnp:
            clock.tick(3)
            pygame.event.get()
            screen.fill(0)
            screen.blit(loadning_mess[currentFrame], (1920 / 2, 1080 / 2))
            currentFrame = (currentFrame + 1) % len(loadning_mess)
            pygame.display.flip()
        endless.stop()


    clicked = False
    count = 0


    def gameloop(clicked, open_menu=True):
        clicked1 = clicked
        global runnp
        runnp = True
        if open_menu:
            if clicked1:
                all = main_window(screen)
                audio = all[0][0][0]
                name = all[1][0][0]
                print(audio)
                print(name)
                consts.current_name = name
                consts.current_audio = audio
            else:
                all = menu(screen)
                audio = all[0][0][0]
                name = all[1][0][0]
                print(audio)
                print(name)
                consts.current_name = name
                consts.current_audio = audio
            clicked1 = True
        thread_for_loading = threading.Thread(target=show_gif, args=(screen,))
        thread_for_loading.start()
        score = 0
        combo = 1
        frs = []
        fruits_on_korzina = 0
        all_fruits = 0
        background = pygame.image.load('resourses/новый god.jpg').convert_alpha()
        sprites_with_trails = pygame.sprite.Group()
        fps = 60
        paused = False
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        catcher = pygame.sprite.Sprite()
        catcher.image = load_image("catcher_left.png")
        catcher.rect = catcher.image.get_rect()
        catcher.rect.x = 660
        catcher.rect.y = 921
        all_sprites.add(catcher)
        sprites_with_trails.add(catcher)
        player = Player(catcher)
        sprite_of_arrow = pygame.sprite.Sprite()
        sprite_of_arrow.image = load_image("gachi_arrow.png")
        sprite_of_arrow.rect = sprite_of_arrow.image.get_rect()
        all_sprites.add(sprite_of_arrow)
        pygame.mouse.set_visible(False)
        copied_notes = open_beatmap(consts.current_name)
        print(len(copied_notes))
        if len(copied_notes) > 800:
            copied = copied_notes
            copied_notes = [copied[x] for x in range(0, len(copied), 2)]
        runnp = False
        screen.blit(background, (0, 0))
        fun3_2_1(background)
        print(consts.current_audio)
        pygame.mixer.music.load(consts.current_audio)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
        delt = 0.07
        print(len(copied_notes))
        start_ticks = 0
        running = True
        while running:
            if not pygame.mixer.music.get_busy() and not paused:
                accuracy = (fruits_on_korzina * 100) / all_fruits
                res = results(screen, score, accuracy)
                if res == 'exit':
                    running = False
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            if keys[pygame.K_SPACE] and pygame.time.get_ticks() - start_ticks > 250:
                start_ticks = pygame.time.get_ticks()
                """paused = not paused"""
                paused = True
            if paused:
                print('paused')
                pygame.mouse.set_visible(True)
                pygame.mixer.music.pause()
                pau = pause_render(screen, background)
                if pau == 'con':
                    paused = False
                    fun3_2_1(background)
                    pygame.mixer.music.unpause()
                elif pau == 'back':
                    running = False
                    pygame.mouse.set_visible(False)
                    all_sprites.empty()
                    return gameloop(clicked=True)
                elif pau == 'retry':
                    running = False
                    all_sprites.empty()
                    pygame.mouse.set_visible(False)
                    return gameloop(clicked=True, open_menu=False)
            if not paused:
                print('not paused')
                screen.blit(background, (0, 0))
                fps_render(clock, screen)
                cursor(sprite_of_arrow)
                player.moving()
                current_position()
                score_render(score)
                combo_render(combo, (catcher.rect.x, catcher.rect.y), screen)
                if fruits_on_korzina == 10:
                    pass
                deleted_notes = []
                for i in range(len(copied_notes) - 1):
                    busted = False
                    if copied_notes[i + 1] - copied_notes[i] < consts.lol:
                        busted = True
                    if abs(current_position() + consts.note_offset - copied_notes[i]) < delt:
                        frs.append(Fruits(player, catcher, 'flashlight', busted, all_sprites))
                        if len(frs) == 2:
                            if abs(frs[0].get_x() - frs[1].get_x()) > 300 or abs(frs[0].get_y() - frs[1].get_y()) < 80:
                                frs[0].forsag = True
                                print(frs)
                                frs = []
                        deleted_notes.append(copied_notes[i])
                        all_fruits += 1
                        print(current_position())
                for i in deleted_notes:
                    copied_notes.remove(i)
                for i in all_sprites:
                    if isinstance(i, Fruits):
                        if i.on_korzina:
                            score = score + (200 * combo)
                            combo += 1
                            fruits_on_korzina += i.count_korzina
                            i.kill()
                        else:
                            combo = 1
                        if i.rect.y >= GetSystemMetrics(1):
                            i.kill()
                all_sprites.draw(screen)
                all_sprites.update()
                pygame.display.flip()
                clock.tick(fps)
        print(all_fruits)
        return gameloop(clicked1)


    gameloop(clicked)
