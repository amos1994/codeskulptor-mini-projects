__author__ = 'sachin'


class Button:
    def __init__(self):
        return

class Timer:
    def __init__(self):
        return

    def start(self):
        return


class Canvas:
    def __init__(self):
        return

    def draw_polygon(self, point_list, line_width, line_color, fill_color=None):
        return

    def draw_polyline(self, point_list, line_width, line_color, fill_color=None):
        return


    def draw_text(self, text, position, width, color):
        return

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        return

    def draw_line(self,point1, point2, line_width, line_color):
        return




class Frame:

    def add_button(self, text, button_handler, width):
        button = Button()
        return button

    def add_button(self, text, button_handler, width=None):
        button = Button()
        return button

    def add_input(self, text, button_handler, width):
        button = Button()
        return button

    def start(self):
        return

    def set_draw_handler(self, draw_handler):
        return

    def set_keydown_handler(self, keydown):
        return

    def set_keyup_handler(self, keyup):
        return

    def set_canvas_background(self, color):
        return

def create_frame( label, canvas_width, canvas_height, control_width=200):
    frame = Frame()
    return frame

def create_timer(interval, timer_handler):
    timer = Timer()
    return timer

