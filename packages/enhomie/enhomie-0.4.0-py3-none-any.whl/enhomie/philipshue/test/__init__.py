"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path



SAMPLES = (
    Path(__file__).parent
    .joinpath('samples'))



SCENE_PHIDS = [

    ('5808a516-aab3-3ec3'
     '-8eee-4db5152b07b5'),

    ('9678ff8b-d452-49f3'
     '-861c-74e5c5b2ca7c')]

SCENE_PATHS = [

    ('https://192.168.1.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[0]}'),

    ('https://192.168.2.10'
     '/clip/v2/resource/scene'
     f'/{SCENE_PHIDS[1]}')]
