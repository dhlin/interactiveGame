import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
paddle2_pos = [WIDTH - PAD_WIDTH / 2, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel       # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] 

    # initillize ball's velocity randomly     
    if direction == LEFT:
        ball_vel[0] = -random.randrange(5, 10)
        ball_vel[1] = -random.randrange(3, 6) 
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(5, 10)
        ball_vel[1] = -random.randrange(3, 6)     

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global BALL_RADIUS, paddle1_vel, paddle2_vel, score1, score2 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bounces if the ball meets the top and buttom 
    if (ball_pos[1] - BALL_RADIUS <= 0) or (ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
        
    # the case that the ball meets the left gutter and paddle    
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS: 
        if (ball_pos[1] < paddle1_pos[1] - PAD_HEIGHT / 2) or (ball_pos[1] > paddle1_pos[1] + PAD_HEIGHT / 2):
            spawn_ball(RIGHT)
            score2 += 1
        else:
            ball_vel[0] = -ball_vel[0] * 1.1
            
    # the case that the ball meets the right gutter and paddle      
    if ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS: 
        if (ball_pos[1] < paddle2_pos[1] - PAD_HEIGHT / 2) or (ball_pos[1] > paddle2_pos[1] + PAD_HEIGHT / 2):
            spawn_ball(LEFT)
            score1 += 1
        else: 
            ball_vel[0] = -ball_vel[0] * 1.1

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White","White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    if paddle1_pos[1] < PAD_HEIGHT / 2:
        paddle1_pos[1] = PAD_HEIGHT / 2
    if paddle1_pos[1] > HEIGHT - PAD_HEIGHT / 2:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT / 2
    if paddle2_pos[1] < PAD_HEIGHT / 2:
        paddle2_pos[1] = PAD_HEIGHT / 2
    if paddle2_pos[1] > HEIGHT - PAD_HEIGHT / 2:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT / 2
    
    # draw paddles
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1] - PAD_HEIGHT / 2], \
                     [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT / 2], 8, "White")
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1] - PAD_HEIGHT / 2], \
                     [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT / 2], 8, "White")
    
    # draw scores
    canvas.draw_text(str(score1), [100, 100], 30, "White")
    canvas.draw_text(str(score2), [500, 100], 30, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] += 10
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] -= 10
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] += 10   
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] -= 10
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = 0

# button_handler that reset the game
def button_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', button_handler, 200)

# start frame
new_game()
frame.start()
