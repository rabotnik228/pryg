from numpy import arange


SIZES = {'normal': (74, 68),
         'little': (55, 50),
         'big': (100, 90)}
CATCHER_SIZE = {'normal': (301, 320),
                'little': (240, 254),
                'big': (360, 380)}
DOUBLECLICKTIME = 500
RANKS = {'S': [list(arange(97, 101, 1)), 'ranks/S.png', 'ranks/s_rank.png'],
         'A': [list(arange(90, 97, 1)), 'ranks/A.png', 'ranks/rank_a.png'],
         'B': [list(arange(79, 90, 1)), 'ranks/B.png', 'ranks/b_rank.png'],
         'C': [list(arange(65, 79, 1)), 'ranks/C.png', 'ranks/c_rank.png'],
         'D': [list(arange(0, 65, 1)), 'ranks/D.png', 'ranks/d_rank.png']}
note_offset = 0.0
buttons = []
conditions = []
mods_conditions = []
check = False
rank_image = None
rank_image_anime = None
playlist = None
playlist_playing = False
current_audio = None
current_name = None
pause_images = {
    'continue': 'pause-continue.png',
    'retry': 'pause-retry.png',
    'back': 'pause-back.png'
}
modes = ('flashlight', 'inverted', 'perfecto', 'nofail')
lol = 0.2
predel = 0.13
cur_pos = 0
max_fall = 20
was_played = False
current_index = 0
fallen = 0
current_fruit = None
mods_pics = {'inverted': '',
             'flashlight': '',
             'nofail': '',
             'perfecto': ''}
