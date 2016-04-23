from __future__ import division, print_function, unicode_literals
import six

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pyglet
from cocos.director import director
from MainScene import *

def init():
    pyglet.resource.path.append('res')
    pyglet.font.add_directory('res')
    pyglet.resource.reindex()
    director.init(resizable=True, width=960, height=640, autoscale=True, caption='Maze')
    # director.set_show_FPS(True)

def run(scene):
    director.run(scene)

def main():
    init()
    run(get_main_scene())

if __name__ == '__main__':
    main()