
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *

UI_height = 64

class UI(ColorLayer):
    def __init__(self):
        super(UI, self).__init__(100, 0, 0, 255, width=960, height=UI_height)

    def on_enter(self):
        super(UI, self).on_enter()


class WorldMap(ScrollableLayer):
    is_event_handler = True

    def update_focus(self, dx=0, dy=0):
        def deal_in_world():
            size = self.win_size
            if self.scroll_x < size[0] / 2:
                self.scroll_x = size[0] / 2
            if self.scroll_y < size[1] / 2:
                self.scroll_y = size[1] / 2
            if self.world_width - self.scroll_x < size[0] / 2:
                self.scroll_x = self.world_width - size[0] / 2
            if self.world_height - self.scroll_y < size[1] / 2 - UI_height:
                self.scroll_y = self.world_height - size[1] / 2 + UI_height

        self.scroll_x = self.scroll_x - dx
        self.scroll_y = self.scroll_y - dy
        deal_in_world()
        self.scroller.set_focus(self.scroll_x, self.scroll_y)
        

    def on_enter(self):
        super(WorldMap, self).on_enter()
        self.scroller = self.get_ancestor(ScrollingManager)
        self.update_focus()

    # def on_mouse_motion(self, sx, sy, dx, dy):
    #     print("on_mouse_motion" , sx, sy, dx, dy)
    # def on_mouse_leave(self, sx, sy):
    #     print("on_mouse_leave" , sx, sy)
    def on_mouse_press(self, x, y, buttons, modifiers):
        # print("on_mouse_press" , x, y, buttons, modifiers)
        pass
    def on_mouse_release(self, sx, sy, button, modifiers):
        # print("on_mouse_release" , sx, sy, button, modifiers)
        pass
    def on_mouse_drag(self, sx, sy, dx, dy, buttons, modifiers):
        # print("on_mouse_drag" , sx, sy, dx, dy, buttons, modifiers)
        self.update_focus(dx, dy)
        pass
    # def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    #     print("on_mouse_scroll" , x, y, scroll_x, scroll_y)

    def __init__(self):
        self.world_width = 960 * 2
        self.world_height = 640 * 2
        super(WorldMap, self).__init__()

        self.win_size = director.get_window_size()
        self.scroll_x = self.world_width / 2
        self.scroll_y = self.world_height / 2

        #dummy objects in the world: a big framed background and squares
        bg = ColorLayer(170,
                                    170,
                                    0,
                                    255,
                                    width=self.world_width,
                                    height=self.world_height)
        self.add(bg, z=0)
        margin = int(self.world_width * 0.01)
        self.margin = margin
        bg = ColorLayer(0,
                                    170,
                                    170,
                                    255,
                                    width=self.world_width - 2 * margin,
                                    height=self.world_height - 2 * margin)
        bg.position = (margin, margin)
        self.add(bg, z=1)

        mod = (self.world_width - 2.0 * margin) / 10.0
        y = margin + mod
        while y < self.world_height - mod:
            x = margin + mod
            while x < self.world_width - mod:
                red = 55 + int(200.0 * x / self.world_width)
                blue = 55 + int(200.0 * y / self.world_height)
                actor = ColorLayer(red,
                                               0,
                                               blue,
                                               255,
                                               width=2 * int(mod),
                                               height=2 * int(mod))
                actor.position = x, y
                self.add(actor, z=3)
                x += 3 * mod
            y += 3 * mod


def get_game_scene():
    ui = UI()
    ui.anchor = (0, 1)
    ui.x = 0
    ui.y = director.get_window_size()[1] - UI_height

    scrolling_manager = ScrollingManager()
    scrolling_manager.add(WorldMap())

    scene = Scene(scrolling_manager, ui)
    return scene

def test():
    director.init(resizable=True, width=960, height=640, autoscale=True)
    director.run(get_game_scene())

if __name__ == '__main__':
    test()