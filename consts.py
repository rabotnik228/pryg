from numpy import arange
import pygame

pygame.init()
SIZES = {'normal': (74, 68),
         'little': (55, 50),
         'big': (100, 90)}
CATCHER_SIZE = {'normal': (301, 320),
                'little': (240, 254),
                'big': (360, 380)}
DOUBLECLICKTIME = 500
RANKS = {'S': [list(arange(97, 100, 0.01)), 'ranks/S.png'],
         'A': [list(arange(90, 96, 0.01)), 'ranks/A.png'],
         'B': [list(arange(79, 89, 0.01)), 'ranks/B.png'],
         'C': [list(arange(65, 78, 0.01)), 'ranks/C.png'],
         'D': [list(arange(0, 64, 0.01)), 'ranks/D.png']}
note_offset = 1.0
current_audio = None
pause_images = {
    'continue': 'pause-continue.png',
    'retry': 'pause-retry.png',
    'back': 'pause-back.png'
}
lol = 0.18
