# preloader.py
# author: Elhex
#
# Description: script to preload large resources (textures, models, frames).
#              This helps avoid lags when switching scenes or first time usage.

import glob
import os
from ursina import load_texture, load_model

from constants import PORTAL_FRAMES_FOLDER, GUN_3D_MODEL, GUN_3D_TEXTURE


def preload_resources():
    """
    Preload large resources so that Ursina won't freeze
    """
    frames_list = sorted(glob.glob(os.path.join(PORTAL_FRAMES_FOLDER, '*.jpg')))
    for f in frames_list:
        load_texture(f)

    load_model(GUN_3D_MODEL)
    load_texture(GUN_3D_TEXTURE)

