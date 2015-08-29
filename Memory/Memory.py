import simplegui
import random

number_list = range(8) * 2
init_num_pos = [15, 70]
init_rect_pos = [25, 50]
expose = [False, False, False, False, False, False, False, False, \
          False, False, False, False, False, False, False, False,]
num_expose = 0
compare = [0, 0]
turn = 0

# helper function to initialize globals
def new_game():
    global number_list, num_expose, expose, turn
    random.shuffle(number_list)  
    num_expose = 0
    expose = [False, False, False, False, False, False, False, False, \
              False, False, False, False, False, False, False, False,]
    turn = 0
    label.set_text("Turns = " + str(turn))
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global num_expose, expose, compare, turn
    
    ind_expose = pos[0] / 50
    if expose[ind_expose] != True:
        if num_expose == 0:
            num_expose = 1
            compare[num_expose - 1] = ind_expose
            expose[ind_expose] = True
        elif num_expose == 1:
            num_expose = 2
            compare[num_expose - 1] = ind_expose
            expose[ind_expose] = True
            turn += 1
            label.set_text("Turns = " + str(turn))
        else:
            num_expose = 1
            if number_list[compare[0]] != number_list[compare[1]]:
                expose[compare[0]] = False
                expose[compare[1]] = False
            compare[num_expose - 1] = ind_expose
            expose[ind_expose] = True
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    init_num_pos[0] = 15
    for number in number_list:
        canvas.draw_text(str(number), init_num_pos, 50, "White")
        init_num_pos[0] += 50
    init_rect_pos[0] = 25
    for state in expose:
        if state == False:
            canvas.draw_polygon([[init_rect_pos[0] - 25, init_rect_pos[1] - 50], 
                                 [init_rect_pos[0] - 25, init_rect_pos[1] + 50], 
                                 [init_rect_pos[0] + 25, init_rect_pos[1] + 50], 
                                 [init_rect_pos[0] + 25, init_rect_pos[1] - 50]], 
                                2, "Red", "Green")
            init_rect_pos[0] += 50
        else:
            init_rect_pos[0] += 50
            

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
