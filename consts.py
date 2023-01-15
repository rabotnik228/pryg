from numpy import arange


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
note_offset = 0.0
conditions = (False, False, False, False, False)
current_alpha_of_back = None
current_audio = None
current_name = None
pause_images = {
    'continue': 'pause-continue.png',
    'retry': 'pause-retry.png',
    'back': 'pause-back.png'
}
modes = ('flashlight', 'inverted', 'perfecto', 'nofail')
lol = 0.18
cur_pos = 0
max_fall = 10
know_game = False
current_index = 0
resolution_list = ((1920, 1080), ())
current_fruit = None
mods_pics = {'inverted': '',
             'flashlight': '',
             'nofail': '',
             'perfecto': ''}
