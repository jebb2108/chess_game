import pyghelpers
import pygame

from constants import *

from scene_auth import SceneAuth
from scene_play import ScenePlay
from scene_reg import SceneReg

FRAMES_PER_SECOND = 30

pygame.init()
pygame.display.set_caption('Chess Game')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

scene_auth = SceneAuth(window)
scene_reg = SceneReg(window)
scene_play = ScenePlay(window)

scenes_list = [
    scene_auth, scene_reg, scene_play
]

scene_mgr = pyghelpers.SceneMgr(scenes_list, FRAMES_PER_SECOND)

scene_mgr.run()