from __future__ import division, print_function, unicode_literals
import six

import pyglet
from pyglet.gl import *

from cocos.director import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.layer import MultiplexLayer, Layer
from cocos.actions import *
from cocos.sprite import Sprite

import random
rr = random.randrange

GAME_NAME = 'Maze'
FONT_TTF = 'You Are Loved'

class Fire:
    def __init__(self, x, y, vy, frame, size):
        self.x, self.y, self.vy, self.frame, self.size = x, y, vy, frame, size


class FireManager(Layer):
    def __init__(self, view_width, num):
        super(FireManager, self).__init__()

        self.view_width = view_width
        self.goodies = []
        self.batch = pyglet.graphics.Batch()
        self.fimg = pyglet.resource.image('fire.jpg')
        self.group = pyglet.sprite.SpriteGroup(self.fimg.texture,
                                               blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE)
        self.vertex_list = self.batch.add(4 * num, GL_QUADS, self.group,
                                          'v2i', 'c4B', ('t3f', self.fimg.texture.tex_coords * num))
        for n in range(0, num):
            f = Fire(0, 0, 0, 0, 0)
            self.goodies.append(f)
            self.vertex_list.vertices[n * 8:(n + 1) * 8] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.vertex_list.colors[n * 16:(n + 1) * 16] = [0, 0, 0, 0, ] * 4

        self.schedule(self.step)

    def step(self, dt):
        w, h = self.fimg.width, self.fimg.height
        fires = self.goodies
        verts, clrs = self.vertex_list.vertices, self.vertex_list.colors
        for n, f in enumerate(fires):
            if not f.frame:
                f.x = rr(0, self.view_width)
                f.y = rr(-120, -80)
                # f.vy = rr(40, 70) / 80.0
                f.vy = rr(40, 70) / 100.0
                f.frame = rr(50, 250)
                f.size = 8 + pow(rr(0.0, 100) / 100.0, 2.0) * 32
                f.scale = f.size / 32.0

            x = f.x = f.x + rr(-50, 50) / 100.0
            y = f.y = f.y + f.vy * 4
            c = 3 * f.frame / 255.0
            r, g, b = (min(255, int(c * 0xc2)), min(255, int(c * 0x41)), min(255, int(c * 0x21)))
            f.frame -= 1
            ww, hh = w * f.scale, h * f.scale
            x -= ww / 2
            if six.PY2:
                vs = map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh])
            else:
                vs = list(map(int, [x, y, x + ww, y, x + ww, y + hh, x, y + hh]))
            verts[n * 8:(n + 1) * 8] = vs
            clrs[n * 16:(n + 1) * 16] = [r, g, b, 255] * 4

    def draw(self):
        glPushMatrix()
        self.transform()

        self.batch.draw()

        glPopMatrix()


# menu items effect
def rotate_effect():
    angle = 360
    duration = 0.5
    return Accelerate(RotateBy(angle, duration), 0.15)

def rotate_effect_back():
    return RotateTo(0, 0.01)
#

class MainMenu(Menu):
    def __init__(self):
        # call superclass with the title
        super(MainMenu, self).__init__("Maze")

        # you can override the font that will be used for the title and the items
        self.font_title['font_name'] = FONT_TTF
        self.font_title['font_size'] = 72
        self.font_title['font_size'] = 180

        self.font_item['font_name'] = FONT_TTF
        self.font_item_selected['font_name'] = FONT_TTF

        # you can also override the font size and the colors. see menu.py for
        # more info

        # example: menus can be vertical aligned and horizontal aligned
        self.menu_valign = CENTER
        self.menu_halign = CENTER

        items = []

        items.append(MenuItem('New Game', self.on_new_game))
        items.append(MenuItem('Options', self.on_options))
        items.append(MenuItem('Scores', self.on_scores))
        items.append(MenuItem('Quit', self.on_quit))

        # self.create_menu(items, zoom_in(), zoom_out())
        self.create_menu(items, rotate_effect(), rotate_effect_back())

    # Callbacks
    def on_new_game(self):
        import GameScene
        director.push(GameScene.get_game_scene())

    def on_scores(self):
        self.parent.switch_to(2)

    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        director.pop()


class OptionMenu(Menu):
    def __init__(self):
        super(OptionMenu, self).__init__(GAME_NAME)

        self.font_title['font_name'] = FONT_TTF
        self.font_title['font_size'] = 72

        self.font_item['font_name'] = FONT_TTF
        self.font_item_selected['font_name'] = FONT_TTF

        self.menu_valign = BOTTOM
        self.menu_halign = RIGHT

        items = []
        items.append(MenuItem('Fullscreen', self.on_fullscreen))
        items.append(ToggleMenuItem('Show FPS: ', self.on_show_fps, True))
        items.append(MenuItem('OK', self.on_quit))
        self.create_menu(items, shake(), shake_back())

    # Callbacks
    def on_fullscreen(self):
        director.window.set_fullscreen(not director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)

    def on_show_fps(self, value):
        director.show_FPS = value


class ScoreMenu(Menu):
    def __init__(self):
        super(ScoreMenu, self).__init__(GAME_NAME)

        self.font_title['font_name'] = FONT_TTF
        self.font_title['font_size'] = 72
        self.font_item['font_name'] = FONT_TTF
        self.font_item_selected['font_name'] = FONT_TTF

        self.menu_valign = BOTTOM
        self.menu_halign = LEFT

        self.create_menu([MenuItem('Go Back', self.on_quit)])

    def on_quit(self):
        self.parent.switch_to(0)

def get_main_scene():
    firelayer = FireManager(director.get_window_size()[0], 250)
    menulayer = MultiplexLayer(MainMenu(), OptionMenu(), ScoreMenu())

    scene = Scene(firelayer, menulayer)
    return scene
