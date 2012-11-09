__author__ = 'sachin'
# Implementation of classic arcade game Pong

import simplegui
import random
import math
from simplegui import Canvas

# initialize globals - pos and vel encode vertical info for paddles
WIDTH,HEIGHT,SCORE_HEIGHT = 600,400,100
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

CANVAS_WIDTH,CANVAS_HEIGHT=WIDTH,HEIGHT+SCORE_HEIGHT

SCORE_BOX = [[0,HEIGHT], [WIDTH,HEIGHT], [WIDTH, CANVAS_HEIGHT], [0,CANVAS_HEIGHT]]
SCORE_CENTER = ([HALF_WIDTH,HEIGHT],[HALF_WIDTH,CANVAS_HEIGHT])
SCORE_LEFT = (HALF_WIDTH/2, HEIGHT+SCORE_HEIGHT/2)
SCORE_RIGHT = (SCORE_LEFT[0] + HALF_WIDTH, SCORE_LEFT[1] )

center = (0+HALF_WIDTH, 0+HALF_HEIGHT)
CENTER_X, CENTER_Y = HALF_WIDTH, HALF_HEIGHT

LEFT_SCORE, RIGHT_SCORE = (CENTER_X/2, CENTER_Y), (1.5 * CENTER_X, CENTER_Y)
SCORE_TEXT = (0,HEIGHT+SCORE_HEIGHT/2)

SCORE_RADIUS = 40
BALL_RADIUS, PAD_WIDTH, PAD_HEIGHT = 20, 8, 80


#gx = Gutter in x direction
#gy = Gutter in y direction
#Account for the ball radius as well.
bounds = {
    'top'   : BALL_RADIUS,
    'bottom': HEIGHT - BALL_RADIUS,
    "left"  : PAD_WIDTH + BALL_RADIUS,
    "right" : WIDTH - PAD_WIDTH - BALL_RADIUS
    }

bounds_horizon = (0 + PAD_WIDTH + BALL_RADIUS, WIDTH - PAD_WIDTH - BALL_RADIUS)
bounds_vertical  = (0 + BALL_RADIUS, HEIGHT - BALL_RADIUS)

#Paddles move in the Y direction. Hence X coordinates will remain constant.
PADDLE_LEFT_CENTER = (PAD_WIDTH,HALF_HEIGHT-PAD_HEIGHT/2)
PADDLE_RIGHT_CENTER = (WIDTH-PAD_WIDTH, HALF_HEIGHT-PAD_HEIGHT/2)

paddle_left_pos = []
paddle_right_pos = []

paddle_left_pos = [PADDLE_LEFT_CENTER[0], PADDLE_LEFT_CENTER[1]]
paddle_right_pos = [PADDLE_RIGHT_CENTER[0], PADDLE_RIGHT_CENTER[1]]

paddle_left_vel, paddle_right_vel = 0,0 #Only Y component changes


paddle_vertical_bounds = (0,HEIGHT-PAD_HEIGHT)

HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

center = (0 + CENTER_X, 0 + CENTER_Y)
score_left, score_right = 0,0
ball_pos, ball_vel = [0,0], [0,0]

#Speed in pixels per second
#Suggested speed in pixels per second
# X = 120 to 240
# Y =  60 to 180
# The screen is refreshed 60 times per second
XVEL_MIN, XVEL_MAX = 2,4
YVEL_MIN, YVEL_MAX = 1,3

#Paddle velocity
PADDLE_VELOCITY = 4

#List of ball states
BALL_IN_FLIGHT, BALL_HIT_RAILS, BALL_HIT_GUTTER, BALL_HIT_PADDLE  = 100,200,300,400
NO_PLAYER, LEFT_PLAYER, RIGHT_PLAYER = 100, 200,300
BALL_ADVANCE_ERROR, PLAYER_ERROR = 999,999

HIT_TOP_BIT, HIT_BOTTOM_BIT, HIT_LEFT_BIT, HIT_RIGHT_BIT = 0,1,2,3
HIT_TOP    = (1 << HIT_TOP_BIT)
HIT_BOTTOM = (1 << HIT_BOTTOM_BIT)
HIT_LEFT   = (1 << HIT_LEFT_BIT)
HIT_RIGHT  = (1 << HIT_RIGHT_BIT)
HIT_GUTTER, HIT_RAILS = (HIT_LEFT | HIT_RIGHT), (HIT_TOP | HIT_BOTTOM)

MAX_X_STRIKE_VEL = 4
MAX_Y_STRIKE_VEL = 4

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    global paddle_left_vel, paddle_right_vel
    global paddle_left_pos, paddle_right_pos
    global score_left, score_right

    ball_pos = [CENTER_X, 0 + random.randrange(BALL_RADIUS, HEIGHT-BALL_RADIUS)]
    direction = 1 if right else -1
    ball_vel = [direction * random.randrange(XVEL_MIN, XVEL_MAX), random.randrange(YVEL_MIN, YVEL_MAX)]

    #Return paddles to the center
    paddle_left_pos, paddle_right_pos = list(PADDLE_LEFT_CENTER), list(PADDLE_RIGHT_CENTER)
    return

# define event handlers
def init():
    global paddle_left_pos, paddle_right_pos, paddle1_vel, paddle2_vel  # these are floats
    global score_left, score_right  # these are ints

    #Reset the scores
    score_left, score_right = 0,0

    #Set a random direction for the ball to start
    ball_init(random.randrange(HEIGHT) & 1)

    pass


def strike_ball( ball_vel ):
    #Get a random increase in velocity
    x_spin = random.randrange(MAX_X_STRIKE_VEL)
    y_spin = random.randrange(MAX_Y_STRIKE_VEL)

    #Change direction and add speed
    ball_vel[0] = -ball_vel[0]
    ball_vel[0] += x_spin if ball_vel[0] > 0 else -x_spin

    #Add speed
    ball_vel[1] += y_spin if ball_vel[1] > 0 else -y_spin

    return

#Function will return the state of the ball
#It will also return the loser player if applicable
def advance_ball( ):
    global ball_pos
    #Move the ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    #Ensure x coordinate bounds in the horizontal direction.
    new_ball = list(ball_pos)

    new_ball[0] = max(new_ball[0], bounds['left'])
    new_ball[0] = min(new_ball[0], bounds['right'])

    #Ensure y coordinate bounds in the vertical direction
    new_ball[1] = max(new_ball[1], bounds['top'])
    new_ball[1] = min(new_ball[1], bounds['bottom'])

    if new_ball == ball_pos:
        #There has been no change in the coordinates. Hence the ball is
        #within bounds.
        return BALL_IN_FLIGHT, NO_PLAYER

    #Update the new in-bound coordinates.
    ball_pos = list(new_ball)

    hit_edges = 0
    hit_edges |= (int(new_ball[0] == bounds['left']) << HIT_LEFT_BIT)
    hit_edges |= (int(new_ball[0] == bounds['right']) << HIT_RIGHT_BIT)
    hit_edges |= (int(new_ball[1] == bounds['top']) << HIT_TOP_BIT)
    hit_edges |= (int(new_ball[1] == bounds['bottom']) << HIT_BOTTOM_BIT)

    #Only the Y-component of the velocity is made opposite
    if hit_edges & HIT_RAILS:
        ball_vel[1] = -ball_vel[1]

        if not hit_edges & HIT_GUTTER:
            #The ball probably hit only the top rails
            return BALL_HIT_RAILS, NO_PLAYER

    #The ball hit gutter. Ensure it can't hit both gutters
    assert (hit_edges & HIT_GUTTER) != HIT_GUTTER, "Ball can't hit both gutters at same time"

    #Get the appropriate paddle position
    if hit_edges & HIT_LEFT:
        player_name, paddle_start = LEFT_PLAYER, paddle_left_pos[1]
    else:
        player_name, paddle_start = RIGHT_PLAYER, paddle_right_pos[1]

    if ball_pos[1] >= paddle_start and ball_pos[1] <= paddle_start + PAD_HEIGHT:
        #Need to alter the direction of the velocity
        strike_ball( ball_vel )
        return BALL_HIT_PADDLE, player_name
    else:
        #Hit the gutter. Deduct point
        return BALL_HIT_GUTTER, player_name

    #Return for any error case
    return BALL_ADVANCE_ERROR, PLAYER_ERROR


def draw_paddles(c):
    global paddle_left_pos, paddle_right_pos, paddle_left_vel, paddle_right_vel
    draw_paddle(c, paddle_left_pos,  paddle_left_vel)
    draw_paddle(c, paddle_right_pos, paddle_right_vel)


def draw_paddle(c, paddle_pos, paddle_vel):

    paddle_pos[1] += paddle_vel
    paddle_pos[1] = max(0, paddle_pos[1])
    paddle_pos[1] = min(HEIGHT - PAD_HEIGHT, paddle_pos[1])

    paddle_start = list(paddle_pos)
    paddle_end = [paddle_start[0], paddle_start[1] + PAD_HEIGHT]

    #Draw the paddle at the appropriate location
    c.draw_line(paddle_start, paddle_end, PAD_WIDTH, "Red")
    return

def update_score(loser):
    global score_right, score_left
    if loser == LEFT_PLAYER:
        score_right += 1
    else:
        score_left += 1
    return

def draw_score(c):
    global score_left, score_right, LEFT_SCORE, RIGHT_SCORE, SCORE_RADIUS
    # update the scores
    c.draw_polygon( SCORE_BOX, 8, "Olive", "Khaki")
    c.draw_polyline(SCORE_CENTER, 8, "Olive")
    font_width = 20
    c.draw_text(str(score_left), SCORE_LEFT, font_width, "Olive")
    c.draw_text(str(score_right), SCORE_RIGHT, font_width, "Olive")
    return

def draw_lines(c):
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    return

def draw(c):
    global ball_pos
    draw_lines(c) #Draw lines

    draw_paddles(c) #Draw paddles

    ball_state, loser_player = advance_ball() #Advance ball in play
    if ball_state == BALL_HIT_GUTTER:
        #Update the score and reset the ball position
        update_score(loser_player)
        ball_init(loser_player == LEFT_PLAYER)

    draw_score(c) #Draw score

    c.draw_circle( ball_pos, BALL_RADIUS, 1, "Orange", "Orange") #Draw ball

    return


def keydown(key):
    global paddle_left_vel, paddle_right_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle_left_vel = min(0, paddle_left_vel) - PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["s"]:
        paddle_left_vel = max(0, paddle_left_vel) + PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["up"]:
        paddle_right_vel = min(0, paddle_right_vel) - PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["down"]:
        paddle_right_vel = max(0, paddle_right_vel) + PADDLE_VELOCITY
    else:
        print "No mapping for key=", key

    return


def keyup(key):
    global paddle_left_vel, paddle_right_vel

    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        #Left player released the paddle.
        paddle_left_vel = 0

    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        #Right player released the paddle.
        paddle_right_vel = 0

    return

# create frame
frame = simplegui.create_frame("Pong", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("Green")
frame.set_draw_handler(draw)

#Set key handler
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()


#The reviewers should ignore the following code. It is used for testing
def __test__ball_init():
    for i in range(20):
        if random.randrange(10) & 1:
            direction = True
        else:
            direction = False

        ball_init(direction)
        print "right=", direction, "pos=", ball_pos, "v=", ball_vel

    return

def __test__game():
    init()
    canvas = Canvas()
    for i in range(5000):
        draw(canvas)
        if ball_pos[0] == center[0]:
            center_msg = "[Ball in Center]"
            print ball_pos, ball_vel, center_msg
        else:
            center_msg = ""

        #print ball_pos, ball_vel, center_msg


#The pretest module is loaded in the test runner
if __name__ != '__main__':
    __running_codeskulptor__ = False
    import pretest
    pretest.pretest(__name__, True)
