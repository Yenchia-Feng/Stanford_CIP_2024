import tkinter as tk
import random
import numpy as np

# Written by Yenchia Feng
# Final project for Code in Place 2024

CANVAS_WIDTH = 1900
CANVAS_HEIGHT = 1000
NUMBERS = [i for i in range(1,8)]
PRICES = [10, 100, 500, 10000, 100000, 500000, 1000000]
OFFER_RATIO = [0.1, 0.2, 0.4, 0.7, 1.1, 1.15]
BG_COLOR = "#fcfffc"

def main():
 
    # Create the window
    root = tk.Tk()
    make_window(root, 0, 0)

    # Create the canvas
    c = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BG_COLOR)
    c.pack()

    # Location of the upper-left corner suitcase
    x = 200
    y = 280

    # distance between each suitcase
    dx = 280
    dy = 250

    # Make game graphics
    make_all_suitcase(c, x, y, dx, dy, BG_COLOR)
    make_game_prompt_box(c, x, y, dx, dy)
    make_player_suitcase_box(c, x, y, dx, dy, BG_COLOR)
    make_all_prices(c, x, y, dx, dy)
    make_game_title(c, CANVAS_WIDTH)
    first_game_prompt(c, x, y, dx)
    how_to_play(c, x, y, dx, dy)

    # Shuffle the cash amounts and assign them to the suitcases
    suitcase_prices = shuffle_case(NUMBERS,PRICES)

    # hidden_suitcase is a dictionary that tracks the number and cash prizes of un-opened suitcase
    hidden_suitcase = suitcase_prices

    # open suitcase is a dictionary that tracks the number and cash prizes of opened suitcase
    open_suitcase = {}
    
    # list of numbers of suitcases that haven't been clicked on yet
    num_list = [1, 2, 3, 4, 5, 6, 7]

    # round is used to track the number of legal clicks
    round = []

    # player_num is a list used to store the number of the player's suitcase
    player_num = []

    # Binds the mouse click event to the canvas
    # click_suitcase function is the main game function
    c.bind("<Button-1>", lambda event: click_suitcase(event, c, round, player_num, num_list, suitcase_prices, PRICES, hidden_suitcase, open_suitcase, x, y, dx, dy))


    root.mainloop()


















################################### GUI FUNCTIONS #########################################################################################

# This will have to trigger the actual suitcase opening
# Clicking no longer works after 1 suitcase is revealed
def click_suitcase(event, c, round, player_num, num_list, suitcase_prices, PRICES, hidden_suitcase, open_suitcase, x, y, dx, dy):

    case_width = 200
    case_height =  150

    # Find what objects are clicked (object IDs)
    overlapping = c.find_overlapping(event.x, event.y, event.x, event.y)
    print("Objects clicked:", overlapping)

    if overlapping and overlapping[0] <= 56:

        # Get suitcase number from object ID
        num = overlapping[0] // 8 + 1

        if num in num_list:

            # Find the object ID of the main suitcase body
            if overlapping[0] % 8 != 3:
                object =  overlapping[0] + 3 - overlapping[0] % 8
            else:
                object = overlapping[0]

            #print("Items overlapping with the click point:", object)

            # Get the X, Y coordinates of the suitcase
            suitcase_x = get_left_x(c, object)
            suitcase_y = get_top_y(c, object)
            
            # First round: player picks a suitcase
            if len(num_list) == 7:

                # The number of the player's suitcase
                player_num.append(num)
                # print("Player num = "+str(player_num))
                # print("num = "+str(num))

                # "Move" the player-picked suitcase to the player suitcase box
                cover_suitcase(c, suitcase_x, suitcase_y)
                make_player_suitcase(c, x, y, dx, dy, BG_COLOR, num)

                # Update prompt box
                make_game_prompt_box(c, x, y, dx, dy)
            
                c.create_text(x+3*dx/2+450, y+50, font=('Arial Bold', 25), text='Click on any of the', fill='black')
                c.create_text(x+3*dx/2+450, y+100, font=('Arial Bold', 25), text='remaning suitcase to', fill='black')
                c.create_text(x+3*dx/2+450, y+150, font=('Arial Bold', 25), text='reveal an offer.', fill='black')

                round.append(1)
                # print("legal game clicks = "+str(len(round)))

                # Remove num from num_list
                num_list.remove(num)
                # print(num_list)    
            
            # Player reveals the prizes inside suitcases
            elif len(num_list) > 0 and (len(round) % 2 == 1):

                # print("Player num = "+str(player_num))
                # print("num = "+str(num))
                # print(num_list)

                # Reveal what's inside the suitcase
                round_rectangle(c, suitcase_x-60, suitcase_y, suitcase_x+140, suitcase_y+150, radius=60, width=7, fill="black", outline="grey70")
                c.create_text(suitcase_x+40, suitcase_y+75, font=('Arial Bold', 25), text="$"+str(suitcase_prices[num]), fill='white')

                # Grey out the prize from the available prizes
                grey_out_price(c, x, y, dx, dy, PRICES.index(suitcase_prices[num]))

                # Update dictionaries of hidden and open suitcases
                update_suitcase(num, hidden_suitcase, open_suitcase)

                # Update game prompt dialogue 
                make_game_prompt_box(c, x, y, dx, dy)
                c.create_text(x+3*dx/2+450, y+25, font=('Arial Bold', 25), text="The banker offers to", fill='black')
                c.create_text(x+3*dx/2+450, y+75, font=('Arial Bold', 25), text="buy your suitcase for", fill='black')
                c.create_text(x+3*dx/2+450, y+125, font=('Arial Bold', 25), text="$"+str(banker_offer(PRICES, hidden_suitcase, open_suitcase, player_num)), fill='black')
                c.create_text(x+3*dx/2+450, y+175, font=('Arial Bold', 25), text="Deal or no deal?", fill='black')

                round.append(1)
                print("legal game clicks = "+str(len(round)))

                # Remove num from num_list
                num_list.remove(num)
                # print(num_list)

                if len(round) == 2:
                    # Make deal and no deal buttons
                    make_Deal_NoDeal_button(c, x, y, dx, dy)
                
    # Deal
    elif overlapping and (overlapping[0] == 115 or overlapping == 116) and (len(round) % 2 != 1):

        # print("Deal!")
        make_game_prompt_box(c, x, y, dx, dy)
        c.create_text(x+3*dx/2+450, y+50, font=('Arial Bold', 25), text="Congratulations!", fill='black')
        c.create_text(x+3*dx/2+450, y+100, font=('Arial Bold', 25), text=" You won", fill='black')
        c.create_text(x+3*dx/2+450, y+150, font=('Arial Bold', 25), text="$"+str(banker_offer(PRICES, hidden_suitcase, open_suitcase, player_num))+"!", fill='black')
        round_rectangle(c, x+3*dx/2+350, y+470, x+3*dx/2+350+case_width, y+470+case_height, radius=60, width=7, fill="black", outline="grey70")
        c.create_text(x+3*dx/2+450, y+545, font=('Arial Bold', 25), text="$"+str(suitcase_prices[player_num[0]]), fill='white')
        c.unbind("<Button-1>")
    
    # No Deal
    elif overlapping and (overlapping[0] == 117 or overlapping == 118):

        # print("No deal!")
        make_game_prompt_box(c, x, y, dx, dy)
        c.create_text(x+3*dx/2+450, y+25, font=('Arial Bold', 25), text="Sounds good!", fill='black')
        c.create_text(x+3*dx/2+450, y+75, font=('Arial Bold', 25), text="Click on another", fill='black')
        c.create_text(x+3*dx/2+450, y+125, font=('Arial Bold', 25), text="suitcase to reveal", fill='black')
        c.create_text(x+3*dx/2+450, y+175, font=('Arial Bold', 25), text="a new offer.", fill='black')

        round.append(1)
        print("legal game clicks = "+str(len(round)))

        if len(num_list) == 1:
            make_game_prompt_box(c, x, y, dx, dy)
            c.create_text(x+3*dx/2+450, y+50, font=('Arial Bold', 25), text="Congratulations!", fill='black')
            c.create_text(x+3*dx/2+450, y+100, font=('Arial Bold', 25), text=" You won", fill='black')
            c.create_text(x+3*dx/2+450, y+150, font=('Arial Bold', 25), text="$"+str(suitcase_prices[player_num[0]])+"!", fill='black')
            round_rectangle(c, x+3*dx/2+350, y+470, x+3*dx/2+350+case_width, y+470+case_height, radius=60, width=7, fill="black", outline="grey70")
            c.create_text(x+3*dx/2+450, y+545, font=('Arial Bold', 25), text="$"+str(suitcase_prices[player_num[0]]), fill='white')
            c.unbind("<Button-1>")

# Get the first element of the coordinates, which is the left x
def get_left_x(c, object_id):
    return c.coords(object_id)[0]  

# Get the second element of the coordinates, which is the top y
def get_top_y(c, object_id):
    return c.coords(object_id)[1]  


################################### GRAPHICS FUNCTIONS ####################################################################################
# Create a window
def make_window(root, x_offset, y_offset):
    root.resizable(False, False)
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    win_x = root_x + x_offset
    win_y = root_y + y_offset
    root.geometry(f'+{win_x}+{win_y}')
    root.title("Deal or No Deal")

# Make rectangles with rounded corners
# code source: https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Make suitcases with numbers
def make_suitcase(c, x, y, num, BG_COLOR):
    case_width = 200
    case_height = 150
    handle_width_1 = 80
    handle_height_1 = 40
    handle_width_2 = 50
    handle_height_2 = 25
    # Make a suitcase with number
    handle = round_rectangle(c, 
                             x+(case_width-handle_width_1)/2, y-handle_height_1, 
                             x+(case_width+handle_width_1)/2, y+handle_height_1, 
                             radius=50, width=5, fill="grey20", outline="grey10")
    handle_inner = round_rectangle(c, 
                             x+(case_width-handle_width_2)/2, y-handle_height_2, 
                             x+(case_width+handle_width_2)/2, y+handle_height_2, 
                             radius=20, width=5, fill=BG_COLOR, outline="grey10")
    case = round_rectangle(c, x, y, x+case_width, y+case_height, radius=60, width=7, fill="grey90", outline="grey70")
    c.create_line(x, y+20, x+case_width, y+20, width=5, fill="grey70")
    c.create_line(x, y+35, x+case_width, y+35, width=5, fill="grey70")
    c.create_line(x, y+115, x+case_width, y+115, width=5, fill="grey70")
    c.create_line(x, y+130, x+case_width, y+130, width=5, fill="grey70")
    main_text = c.create_text(x + case_width / 2, y + case_width / 2 - 25, font=('Arial Bold', 100), text=str(num), fill='black')

# Make the seven suitcases
def make_all_suitcase(c, x, y, dx, dy, BG_COLOR):
    suitcase_1 = make_suitcase(c, x, y+2*dy, 1, BG_COLOR)
    suitcase_2 = make_suitcase(c, x+dx, y+2*dy, 2, BG_COLOR)
    suitcase_3 = make_suitcase(c, x-dx/2, y+dy, 3, BG_COLOR)
    suitcase_4 = make_suitcase(c, x+dx/2, y+dy, 4, BG_COLOR)
    suitcase_5 = make_suitcase(c, x+3*dx/2, y+dy, 5, BG_COLOR)
    suitcase_6 = make_suitcase(c, x, y, 6, BG_COLOR)
    suitcase_7 = make_suitcase(c, x+dx, y, 7, BG_COLOR)

# Make game prompt box
def make_game_prompt_box(c, x, y, dx, dy):
    round_rectangle(c, x+3*dx/2+250, y-30, x+3*dx/2+650, y+220, radius=30, width=7, fill="white", outline="forest green")

# Explain game rules
def how_to_play(c, x, y, dx, dy):
    shift = -40
    c.create_text(x+5.4*dx, y+shift, font=('Arial Bold', 30), text="How to Play", fill='forest green')
    c.create_text(x+5.4*dx, y+75+shift, font=('Arial Bold', 25), text="1. Pick a suitcase. ", fill='forest green')
    c.create_text(x+5.4*dx, y+135+shift, font=('Arial Bold', 25), text="2. Open a different", fill='forest green')
    c.create_text(x+5.4*dx, y+195+shift, font=('Arial Bold', 25), text="suitcase to reveal", fill='forest green')
    c.create_text(x+5.4*dx, y+255+shift, font=('Arial Bold', 25), text="the prize inside.", fill='forest green')
    c.create_text(x+5.4*dx, y+315+shift, font=('Arial Bold', 25), text="3. Banker offers a  ", fill='forest green')
    c.create_text(x+5.4*dx, y+375+shift, font=('Arial Bold', 25), text="deal based on the", fill='forest green')
    c.create_text(x+5.4*dx, y+435+shift, font=('Arial Bold', 25), text="remaining prizes.", fill='forest green')
    c.create_text(x+5.4*dx, y+495+shift, font=('Arial Bold', 25), text='4. Click "Deal" to   ', fill='forest green')
    c.create_text(x+5.4*dx, y+555+shift, font=('Arial Bold', 25), text="accept the offer, or", fill='forest green')
    c.create_text(x+5.4*dx, y+615+shift, font=('Arial Bold', 25), text='click "No Deal" to', fill='forest green')
    c.create_text(x+5.4*dx, y+675+shift, font=('Arial Bold', 25), text="continue playing.", fill='forest green')

# Make game title
def make_game_title(c, CANVAS_WIDTH):
    c.create_text(CANVAS_WIDTH /2 , 40, font=('Arial Bold', 25), text="Welcome to A Game of", fill='forest green')
    c.create_text(CANVAS_WIDTH /2 , 120, font=('Arial Bold', 80), text="DEAL or NO DEAL", fill='forest green')

# First game prompt
def first_game_prompt(c, x, y, dx):
    c.create_text(x+3*dx/2+450, y+20, font=('Arial Bold', 25), text="Pick a suitcase as", fill='black')
    c.create_text(x+3*dx/2+450, y+70, font=('Arial Bold', 25), text="YOUR suitcase", fill='black')
    c.create_text(x+3*dx/2+450, y+120, font=('Arial Bold', 25), text="by clicking on any", fill='black')
    c.create_text(x+3*dx/2+450, y+170, font=('Arial Bold', 25), text="suitcase on the left.", fill='black')

# Deal button and No deal button
def make_Deal_NoDeal_button(c, x, y, dx, dy):
    round_rectangle(c, x+3*dx/2+250, y+240, x+3*dx/2+440, y+310, radius=30, width=5, fill="blue2", outline="blue4")
    Deal_text = c.create_text(x+3*dx/2+345, y+275, font=('Arial Bold', 30), text="Deal", fill='white')
    round_rectangle(c, x+3*dx/2+460, y+240, x+3*dx/2+650, y+310, radius=30, width=5, fill="red3", outline="red4")
    NoDeal_text = c.create_text(x+3*dx/2+555, y+275, font=('Arial Bold', 30), text="No deal", fill='white')

# Player suitcase box
def make_player_suitcase_box(c, x, y, dx, dy, BG_COLOR):
    PlayerSuitcase_text = c.create_text(x+3*dx/2+450, y+370, font=('Arial Bold', 30), text="Your Suitcase", fill='forest green')
    round_rectangle(c, x+3*dx/2+250, y+400, x+3*dx/2+650, y+650, radius=30, width=7, fill=BG_COLOR, outline="forest green")

# Player suitcase
def make_player_suitcase(c, x, y, dx, dy, BG_COLOR, num):
    make_suitcase(c, x+3*dx/2+350, y+470, num, BG_COLOR)

 # Availble prices
def make_all_prices(c, x, y, dx, dy):
    shift = -40
    Prizes_text = c.create_text(x+4.35*dx, y+shift, font=('Arial Bold', 32), text="Prizes", fill='forest green')
    for i in range(7):
        round_rectangle(c, x+3*dx/2+700, y+22+95*i, x+3*dx/2+900, y+82+95*i, radius=30, width=3, fill="black", outline="forest green")
        Cash_text = c.create_text(x+3*dx/2+800, y+52+95*i, font=('Arial Bold', 25), text=["$"+str(PRICES[i])], fill='white')

# Grey out revealed prices
def grey_out_price(c, x, y, dx, dy, i):
    round_rectangle(c, x+3*dx/2+700, y+22+95*i, x+3*dx/2+900, y+82+95*i, radius=30, width=3, fill="black", outline="forest green")
    Cash_text = c.create_text(x+3*dx/2+800, y+52+95*i, font=('Arial Bold', 25), text=["$"+str(PRICES[i])], fill='grey30')

# Cover up a suitcase
def cover_suitcase(c, x, y):
    handle_height_1 = 40
    case_height = 150
    case_width = 200
    round_rectangle(c, x-60, y-handle_height_1, x+case_width-60, y+case_height, radius=30, width=7, fill="white", outline="white")
    #c.create_rectangle(x-50, y-handle_height_1, x+case_width-50, y+case_height, width=7, fill="red", outline=BG_COLOR)



################################### BASE GAME FUNCTIONS ###################################################################################

# Banker offers to buy the player's suitcase
def banker_offer(PRICES, hidden_suitcase, open_suitcase, player_num):
    player_cash = hidden_suitcase[player_num[0]]
    cash_hidden = np.sum(PRICES) - np.sum(list(open_suitcase.values())) + player_cash
    offer =  OFFER_RATIO[-len(hidden_suitcase)] * cash_hidden / (len(hidden_suitcase) + 1) + np.sqrt(player_cash)
    offer = int(offer)
    if offer >= 1000000:
        offer = 925000
    elif offer >= np.max(list(hidden_suitcase.values())):
        offer = np.max(list(hidden_suitcase.values())) * 0.75
    return offer

# Remove key-value pair with key "num" from dict1 and add to dict2
def move(num, dict1, dict2):
    if num in dict1:
        dict2[num] = dict1[num]
        del dict1[num]
    return dict1, dict2

# Shuffle the cash amounts and assign them to the suitcases
# Outputs a dictionary of {'suitcase number': $ cash amount} pairs
def shuffle_case(NUMBERS,PRICES):
    suitcase_prices = {}
    prices_shuffled = random.sample(PRICES,  len(PRICES))
    for i in range(len(NUMBERS)):
        suitcase_prices[NUMBERS[i]] = prices_shuffled[i]
    return suitcase_prices

# Update dictionaries of hidden and revealed suitcase based on selected suitcase number
# Display the remaining (hidden) suitcase numbers
def update_suitcase(num, dict1, dict2):
    dict1, dict2 = move(num, dict1, dict2)


if __name__ == '__main__':
    main()
