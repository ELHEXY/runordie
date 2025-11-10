# video.py
# author: Elhex
#
# Description: video transition effect for the game (2D/3D)
#

from ursina import *
import glob, os

class VideoPlayer(Entity):
    """
    class for playing frame-by-frame video in Ursina.
    """
    def __init__(self, frames_folder, fps=20, on_finish=None):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(2, 2),
            color=color.white,
            z=-999
        )
        self.frames = []
        frames_list = sorted(glob.glob(os.path.join(frames_folder, '*.jpg')))
        if not frames_list:
            if on_finish:
                on_finish()
            self.disable()
            return

        # preload all frames
        self.frames = [load_texture(f) for f in frames_list]

        self.index = 0
        self.fps = fps
        self.on_finish = on_finish

    def update(self):
        self.index += self.fps * time.dt
        if self.index >= len(self.frames):
            self.disable()
            if self.on_finish:
                self.on_finish()
        else:
            self.texture = self.frames[int(self.index)]
