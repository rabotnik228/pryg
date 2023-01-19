import random
import numba
import pygame
import librosa
from record_database import *
from design import load_image
from moving_catcher import Player
import os
import sys
import tkinter as tk
import consts
import pygame.gfxdraw
from numba import jit
import ctypes
import threading

pygame.init()
screen = pygame.display.set_mode((1920, 1080))

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
                    if self.pressed:
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

        def getValue(self) -> int:
            return int(self.sliderWidth / (self.outlineSize[0] / self.upperValue))

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
            self.start_ticks = 0

        def render(self, on=True):
            if on:
                pygame.draw.rect(self.screen, (0, 0, 0), self.rect_but, width=5, border_radius=15)
                if self.current_value:
                    screen.blit(self.image, (self.x + 3, self.y + 5))

        def change_value(self):
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if self.rect_but.collidepoint(mouse_pos):
                if mouse_click[0] and pygame.time.get_ticks() - self.start_ticks > 250:
                    self.start_ticks = pygame.time.get_ticks()
                    self.current_value = not self.current_value

        def get_value(self):
            return self.current_value

        def set_value(self, value):
            self.current_value = value


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
        screen.blit(render, (1920 - 200, 1080 - 100))


    def combo_render(combo, player_pos, screen):
        font_for_combo = pygame.font.SysFont('resourses/koblenz-serial-extralight-regular.ttf', 45)
        combo_rend = font_for_combo.render(str(combo), 0, (255, 255, 255))
        screen.blit(combo_rend, (1920 - 200, 1080 - 50))


    def pause_render(screen):
        contin = load_image(consts.pause_images['continue'])
        retry = load_image(consts.pause_images['retry'])
        back = load_image(consts.pause_images['back'])
        circle_contin = pygame.draw.circle(screen, (0, 0, 0), (1920 / 2, 1080 / 2 - 200), 42)
        circle_retry = pygame.draw.circle(screen, (0, 0, 0), (1920 / 2, 1080 / 2), 42)
        circle_back = pygame.draw.circle(screen, (0, 0, 0), (1920 / 2, 1080 / 2 + 200), 42)
        sounds = (pygame.mixer.Sound('resourses/music/pause-continue-click.mp3'), pygame.mixer.Sound('resourses/music'
                                                                                                     '/pause-retry'
                                                                                                     '-click.mp3'),
                  pygame.mixer.Sound('resourses/music/pause-back-click.mp3'))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        screen.fill((0, 0, 0))
        screen.blit(contin, (1920 / 2, 1080 / 2 - 200))
        screen.blit(retry, (1920 / 2, 1080 / 2))
        screen.blit(back, (1920 / 2, 1080 / 2 + 200))
        if circle_contin.collidepoint(mouse_pos):
            print('c')
            if mouse_click[0]:
                sounds[0].play()
                return 'con'
        if circle_retry.collidepoint(mouse_pos):
            print('r')
            if mouse_click[0]:
                sounds[1].play()
                return 'retry'
        if circle_back.collidepoint(mouse_pos):
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


    def create_achivment_file():
        if not os.path.exists(r'C:\pryg\sets\achivments.txt'):
            pass


    def create_settings_file():
        if not os.path.exists('C:/pryg/sets'):
            os.makedirs('C:/pryg/sets')
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ret = ctypes.windll.kernel32.SetFileAttributesW('C:/pryg/sets', FILE_ATTRIBUTE_HIDDEN)
        if not os.path.exists("C:/pryg/sets/settings.txt"):
            open(r"C:/pryg/sets/settings.txt", 'a').close()
        if os.stat("C:/pryg/sets/settings.txt").st_size == 0:
            with open("C:/pryg/sets/settings.txt", "w") as f:
                f.write('True True True 0')
                f.close()


    def get_value_from_sett():
        with open("C:/pryg/sets/settings.txt", "r") as f:
            values = list(f.readline().split(' '))
            consts.conditions = values
            return values


    def set_value(value, index):
        with open("C:/pryg/sets/settings.txt", 'r+') as file:
            file.truncate(0)
            file.close()
        with open("C:/pryg/sets/settings.txt", "w") as f:
            consts.conditions[index] = value
            values = consts.conditions
            values_str = ' '.join(list(map(str, values)))
            f.write(values_str)
            f.close()


    def set_offset(value, plus):
        if plus:
            consts.note_offset = value / 1000
        else:
            consts.note_offset = -value / 1000


    def menu(screen):
        global k
        k = True
        thread_for_begin = threading.Thread(target=show_gif_for_begin, args=(screen,))
        thread_for_begin.start()
        create_folder()
        global maps
        maps = CreateMpDb()
        create_f()
        create_settings_file()
        create_beatmap('nostalgic', 'resourses/music/Nostalgic.wav')
        create_beatmap('tomydream', 'resourses/music/tomydream.wav')
        create_beatmap('rickroll', 'resourses/music/its_alright.wav')
        create_beatmap('Hajimari_no_Toki', 'resourses/music/Hajimari_no_Toki.wav')
        create_beatmap('go go go', 'resourses/music/go.wav')
        maps.add_to_database('nostalgic', 'resourses/music/Nostalgic.wav')
        maps.add_to_database('tomydream', 'resourses/music/tomydream.wav')
        maps.add_to_database('rickroll', 'resourses/music/its_alright.wav')
        maps.add_to_database('Hajimari_no_Toki', 'resourses/music/Hajimari_no_Toki.wav')
        maps.add_to_database('go go go', 'resourses/music/go.wav')
        k = False
        threaded_for_end = threading.Thread(target=play_goodbye)
        global all_sprites
        consts.playlist = [pygame.mixer.Sound(maps.all_songs()[x][0]) for x in range(len(maps.all_songs()))]
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
        print(get_value_from_sett())
        for i in range(100):
            snow_list.append([random.randrange(0, 1920), random.randrange(0, 1080),
                              random.randrange(1, 5)])
        if not consts.playlist_playing:
            play_sound()
        menu_trigger = True
        menu_picture = pygame.image.load(f'resourses/bg/{random.randint(0, 9)}.jpg').convert_alpha()
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
            if get_value_from_sett()[0] == 'True':
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
                sett = main_window(screen)
                return sett
            if exitt.check_click():
                play_sound(stop=True)
                threaded_for_end.start()
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
                return options_window(screen, menu_picture)
            pygame.display.flip()
            clock.tick(20)


    def play_goodbye():
        a = pygame.mixer.Sound('resourses/music/goodbye.mp3')
        a.play()


    def playlist_on():
        if not pygame.mixer.get_busy():
            random.choice(consts.playlist).play()


    def cursor(sprite_of_arrow):
        if pygame.mouse.get_focused():
            coords = pygame.mouse.get_pos()
            sprite_of_arrow.rect.x = coords[0]
            sprite_of_arrow.rect.y = coords[1]


    def main_window(screen):
        main_window_trigger = True
        menu_picture = pygame.image.load(f'resourses/bg/{random.randint(0, 9)}.jpg').convert()
        add_song_image = pygame.image.load('resourses/plus.png').convert_alpha()
        buttons = []
        songs = []
        list_of_names = maps.all_maps()
        print(list_of_names)
        back = Button("Exit", "Exit?", 400, 150, (0, 1080 - 200), 5, buttons)
        rectang = pygame.Rect(0, 0, 60, 60)
        rectang.center = 1920 - 60, 60
        song = Button('nostalgic', 'nostalgic', 400, 150, (1920 - 500, 150), 5, songs)
        song1 = Button('tomydream', 'tomydream', 400, 150, (1920 - 500, 350), 5, songs)
        song2 = Button('rickroll', 'rickroll', 400, 150, (1920 - 500, 550), 5, songs)
        song3 = Button('Hajimari_no_Toki', 'Hajimari_no_Toki', 400, 150, (1920 - 500, 750), 5, songs)
        up = Button('up', 'up', 50, 50, (1920 - 250, 50), 5, buttons)
        down = Button('down', 'down', 50, 50, (1920 - 250, 1080 - 50), 5, buttons)
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
        back = Button("Exit", "Exit?", 400, 150, (0, 1080 - 200), 5, buttons)
        slider_for_offset = Slider((250, 100), 300, text='note_offset', sliderWidth=int(get_value_from_sett()[3]))
        if get_value_from_sett()[0] == 'True':
            check_for_snow = Checkbox(screen, (100, 300), True)
        elif get_value_from_sett()[0] == 'False':
            check_for_snow = Checkbox(screen, (100, 300), False)
        if get_value_from_sett()[1] == 'True':
            check_for_fps = Checkbox(screen, (100, 500), True)
        elif get_value_from_sett()[1] == 'False':
            check_for_fps = Checkbox(screen, (100, 500), False)
        if get_value_from_sett()[2] == 'True':
            plus = Checkbox(screen, (100, 100), True)
        elif get_value_from_sett()[2] == 'False':
            plus = Checkbox(screen, (100, 100), False)
        while options_trigger:
            pygame.event.get()
            screen.blit(fon, (0, 0))
            cursor(sprite_of_arrow)
            for i in buttons:
                i.draw(screen)
            plus.render()
            screen.blit(font.render("Setting up an offset", 1, (255, 255, 255)), (600, 100))
            screen.blit(font.render("Snow render", 1, (255, 255, 255)), (350, 300))
            screen.blit(font.render("Fps render", 1, (255, 255, 255)), (250, 500))
            slider_for_offset.render(True, screen)
            check_for_snow.render()
            check_for_fps.render()
            if back.check_click():
                set_value(check_for_fps.get_value(), 1)
                set_value(check_for_snow.get_value(), 0)
                set_value(plus.get_value(), 2)
                set_value(slider_for_offset.getValue(), 3)
                set_offset(slider_for_offset.getValue(), plus.get_value())
                options_trigger = False
                return menu(screen)
            check_for_snow.change_value()
            check_for_fps.change_value()
            slider_for_offset.changeValue()
            plus.change_value()
            all_sprites1.draw(screen)
            all_sprites1.update()
            pygame.display.flip()


    def end_render(screen):
        retry = load_image(consts.pause_images['retry'])
        back = load_image(consts.pause_images['back'])
        circle_retry = pygame.draw.circle(screen, (0, 0, 0), (1920 / 2, 1080 / 2), 42)
        circle_back = pygame.draw.circle(screen, (0, 0, 0), (1920 / 2, 1080 / 2 + 200), 42)
        sounds = (pygame.mixer.Sound('resourses/music/pause-retry-click.mp3'),
                  pygame.mixer.Sound('resourses/music/pause-back-click.mp3'))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        screen.fill(0)
        screen.blit(retry, (1920 / 2, 1080 / 2))
        screen.blit(back, (1920 / 2, 1080 / 2 + 200))
        if circle_retry.collidepoint(mouse_pos):
            print('r')
            if mouse_click[0]:
                sounds[0].play()
                return 'retry'
        if circle_back.collidepoint(mouse_pos):
            print('b')
            if mouse_click[0]:
                sounds[1].play()
                return 'back'
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
            pygame.mixer.music.play()
        if stop:
            pygame.mixer.music.unload()


    def results(screen, score, rank):
        rank = int(rank)
        print(rank)
        if not consts.check:
            if rank in consts.RANKS['S'][0]:
                consts.rank_image = load_image(consts.RANKS['S'][1])
                consts.rank_image_anime = load_image(consts.RANKS['S'][2])
                if not consts.was_played:
                    pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.unload()
                    consts.was_played = True
            elif rank in consts.RANKS['A'][0]:
                consts.rank_image = load_image(consts.RANKS['A'][1])
                consts.rank_image_anime = load_image(consts.RANKS['A'][2])
                if not consts.was_played:
                    pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.unload()
                    consts.was_played = True
            elif rank in consts.RANKS['B'][0]:
                consts.rank_image = load_image(consts.RANKS['B'][1])
                consts.rank_image_anime = load_image(consts.RANKS['B'][2])
                if not consts.was_played:
                    pygame.mixer.music.load('resourses/music/sectionpass.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.unload()
                    consts.was_played = True
            elif rank in consts.RANKS['C'][0]:
                consts.rank_image = load_image(consts.RANKS['C'][1])
                consts.rank_image_anime = load_image(consts.RANKS['C'][2])
                if not consts.was_played:
                    pygame.mixer.music.load('resourses/music/sectionfail.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.unload()
                    consts.was_played = True
            elif rank in consts.RANKS['D'][0]:
                consts.rank_image = load_image(consts.RANKS['D'][1])
                consts.rank_image_anime = load_image(consts.RANKS['D'][2])
                if not consts.was_played:
                    pygame.mixer.music.load('resourses/music/sectionfail.mp3')
                    pygame.mixer.music.play()
                    pygame.mixer.music.unload()
                    consts.was_played = True
            consts.check = True
        font = pygame.font.SysFont('Arial', 23)
        get_score = font.render(str(score), 1, (255, 255, 255))
        get_accuracy = font.render(str(rank), 1, (255, 255, 255))
        result_picture = pygame.image.load('resourses/для результатов.png').convert()
        screen.fill((0, 0, 0))
        screen.blit(result_picture, (1920 / 2 - 400, 1080 / 2 - 300))
        screen.blit(get_score, (1920 / 2 - 300, 1080 / 2 - 300))
        screen.blit(get_accuracy, (1920 / 2 - 200, 1080 / 2 - 300))
        screen.blit(consts.rank_image, (1920 / 2, 1080 / 2 - 300))
        screen.blit(consts.rank_image_anime, (1920 / 2, 1080 / 2))
        for b in consts.buttons:
            b.draw(screen)
        for b in consts.buttons:
            if b.check_click():
                play_sound(music='start')
                return 'exit'
        pygame.display.flip()


    def fps_render(clock, screen, on=True):
        button_font = pygame.font.SysFont('Arial', 20)
        display_fps = str(int(clock.get_fps()))
        render = button_font.render(display_fps, 0, (0, 250, 0))
        screen.blit(render, (1920 - 20, 1080 - 30))


    def snow(screen, snow_list, alpha=None):
        speed = 10
        for snowy in snow_list:
            snowy[1] += speed
            if snowy[1] > 1080:
                snowy[1] = 0

        for snowy in snow_list:
            pygame.draw.circle(screen, (255, 255, 255), (snowy[0], snowy[1]), snowy[2])


    def create_beatmap(name, audio):
        if not os.path.exists(f'C:/pryg/.beatmaps/beat_map_{name}.txt'):
            if name == '' or name in '1234567890':
                return False
            if not os.path.exists(audio):
                return False
            if not audio.endswith('.wav'):
                return False
            with open(f'C:/pryg/.beatmaps/beat_map_{name}.txt', 'w') as f:
                n = notes_seconds(audio)
                lit = [list(n)[x] for x in range(0, len(list(n)))]
                lit = list(map(str, lit))
                n2 = ' '.join(lit)
                name_of_audio = str(os.path.splitext(os.path.basename(audio))[0])
                a = f'resourses/music/{name_of_audio}.wav'
                os.replace(audio, a)
                maps.add_to_database(name, a)
                print('ok')
                f.write(n2)


    def open_beatmap(name):
        with open(f'C:/pryg/.beatmaps/beat_map_{name}.txt', 'r') as f:
            nots = list(map(float, f.readline().split(' ')))
            return nots


    def download_window():
        window = tk.Tk()
        window.title("Добавление песни")

        frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)

        frm_form.pack()

        lbl_first_name = tk.Label(master=frm_form, text="Название песни")
        ent_first_name = tk.Entry(master=frm_form, width=50)

        lbl_first_name.grid(row=0, column=0, sticky="e")
        ent_first_name.grid(row=0, column=1)

        lbl_last_name = tk.Label(master=frm_form, text="Путь к песне")
        ent_last_name = tk.Entry(master=frm_form, width=50)

        lbl_last_name.grid(row=1, column=0, sticky="e")
        ent_last_name.grid(row=1, column=1)

        frm_buttons = tk.Frame()
        frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        btn_submit = tk.Button(master=frm_buttons, text="Создать", command=lambda: create_beatmap(ent_first_name.get(),
                                                                                                  ent_last_name.get()))
        btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
        window.mainloop()


    def fun3_2_1():
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
            screen.fill(0)
            screen.blit(font.render(text, True, (random.choice(range(0, 255)), random.choice(range(0, 255)),
                                                 random.choice(range(0, 255)))), (1920 / 2,
                                                                                  1080 / 2))
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


    def show_gif_for_begin(screen):
        endless = pygame.mixer.Sound('resourses/music/бесконечность не предел.mp3')
        clock = pygame.time.Clock()
        loadning_mess = [pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading.', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading..', 1, (255, 255, 255)),
                         pygame.font.Font('resourses/210 Gulim 070.ttf', 40).render('Loading...', 1, (255, 255, 255))]
        currentFrame = 0
        endless.play()
        while k:
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
        otrygka = Button("Exit", "Exit?", 400, 150, (0, 1080 - 200), 5, consts.buttons)
        clicked1 = clicked
        global runnp
        runnp = True
        if open_menu:
            if clicked1:
                all = main_window(screen)
                audio = all[0][0][0]
                name = all[1][0][0]
                consts.current_name = name
                consts.current_audio = audio
            else:
                all = menu(screen)
                audio = all[0][0][0]
                name = all[1][0][0]
                consts.current_name = name
                consts.current_audio = audio
            clicked1 = True
        thread_for_loading = threading.Thread(target=show_gif, args=(screen,))
        thread_for_loading.start()
        score = 0
        combo = 1
        consts.fallen = 0
        frs = []
        fruits_on_korzina = 0
        all_fruits = 0
        sprites_with_trails = pygame.sprite.Group()
        fps = 60
        consts.check = False
        paused = False
        lox = False
        ress = False
        clock = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        catcher = pygame.sprite.Sprite()
        catcher.image = load_image("catcher_left.png")
        catcher.rect = catcher.image.get_rect()
        catcher.rect.x = 660
        catcher.rect.y = 921
        current_offset = 0.47
        all_sprites.add(catcher)
        sprites_with_trails.add(catcher)
        player = Player(catcher)
        sprite_of_arrow = pygame.sprite.Sprite()
        sprite_of_arrow.image = load_image("gachi_arrow.png")
        sprite_of_arrow.rect = sprite_of_arrow.image.get_rect()
        all_sprites.add(sprite_of_arrow)
        pygame.mouse.set_visible(False)
        copied_notes = open_beatmap(consts.current_name)
        copied = copied_notes
        copied_notes = [x for x in copied]
        print(len(copied_notes))
        to_delete = []
        for i in range(len(copied_notes) - 1):
            if abs(copied_notes[i] - copied_notes[i + 1]) <= consts.predel:
                to_delete.append(copied_notes[i])
        for i in to_delete:
            copied_notes.remove(i)
        runnp = False
        screen.fill(0)
        fun3_2_1()
        print(consts.current_audio)
        pygame.mixer.music.load(consts.current_audio)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.0)
        delt = 0.07
        print(len(copied_notes))
        start_ticks = 0
        print(consts.note_offset)
        running = True
        while running:
            pygame.event.get()
            cursor(sprite_of_arrow)
            if not pygame.mixer.music.get_busy() and not paused and not lox:
                ress = True
                accuracy = (fruits_on_korzina * 100) / all_fruits
                res = results(screen, score, accuracy)
                pygame.mouse.set_visible(True)
                if res == 'exit':
                    running = False
            keys = pygame.key.get_pressed()
            """if consts.fallen >= consts.max_fall:
                lox = True
                pygame.mouse.set_visible(True)
                pygame.mixer.music.pause()
                o = end_render(screen)
                if o == 'retry':
                    running = False
                    all_sprites.empty()
                    pygame.mouse.set_visible(False)
                    return gameloop(clicked=True, open_menu=False)
                if o == 'back':
                    running = False
                    pygame.mouse.set_visible(False)
                    all_sprites.empty()
                    return gameloop(clicked=True)"""
            if keys[pygame.K_SPACE] and pygame.time.get_ticks() - start_ticks > 250:
                start_ticks = pygame.time.get_ticks()
                paused = True
            if keys[pygame.K_BACKQUOTE]:
                running = False
                all_sprites.empty()
                pygame.mouse.set_visible(False)
                play_sound(music='pause_retry')
                pygame.mixer.music.pause()
                return gameloop(clicked=True, open_menu=False)
            if paused:
                pygame.mouse.set_visible(True)
                pygame.mixer.music.pause()
                pau = pause_render(screen)
                if pau == 'con':
                    paused = False
                    fun3_2_1()
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
            if not paused and not lox:
                if not ress:
                    screen.fill((0, 0, 0))
                    if get_value_from_sett()[1] == 'True':
                        fps_render(clock, screen)
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
                        if abs(current_position() + consts.note_offset + current_offset - copied_notes[i]) < delt:
                            frs.append(Fruits(player, catcher, 'flashlight', busted, all_sprites))
                            if len(frs) == 2:
                                if abs(frs[0].get_x() - frs[1].get_x()) > 300 or \
                                        abs(frs[0].get_y() - frs[1].get_y()) < 80:
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
                            if i.on_player:
                                score = score + (200 * combo)
                                combo += 1
                                fruits_on_korzina += i.count_korzina
                                consts.fallen -= 1
                                i.kill()
                            elif i.za_player:
                                consts.fallen += 1
                                combo = 1
                            if i.rect.y >= 1080:
                                i.kill()
                    all_sprites.draw(screen)
                    all_sprites.update()
                    pygame.display.flip()
                    clock.tick(fps)
        print(all_fruits)
        consts.check = False
        return gameloop(clicked1)


    gameloop(clicked)
