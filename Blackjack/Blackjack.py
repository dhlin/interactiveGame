import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
    
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, \
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []   
        self.value = 0
        
    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.hand)):
            ans += ' ' + self.hand[i].get_suit() + self.hand[i].get_rank()
        return ans
        
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)        
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = 0
        ace = False
        if len(self.hand) == 0:
            return self.value
        else:
            for i in range(len(self.hand)):
                if self.hand[i].get_rank() == 'A':
                    ace = True
                self.value += VALUES[self.hand[i].get_rank()]    
            if not ace:
                return self.value       
            else:
                if self.value + 10 <= 21:
                    return self.value + 10
                else:
                    return self.value
 
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            card.draw(canvas, [pos[0], pos[1]])
            pos[0] += 100
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.card_list = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                card = Card(SUITS[i], RANKS[j])
                self.card_list.append(card)
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)       
        
    def deal_card(self):
        # deal a card object from the deck
        self.dealcard = self.card_list[-1]
        self.card_list.remove(self.card_list[-1])
        return self.dealcard
        
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.card_list)):
            ans += ' ' + self.card_list[i].get_suit() + self.card_list[i].get_rank()
        return ans

#define event handlers for buttons
def deal():
    global outcome, score, in_play, game_deck, my_hand, dealer_hand 
   
    if in_play:
        score -= 1
        outcome = "You give up and lose."
        in_play = False
    else:
        outcome = ""
        in_play = True
        
    game_deck = Deck()
    my_hand = Hand()
    dealer_hand = Hand()
    game_deck.shuffle()
    
    my_hand.add_card(game_deck.deal_card())
    my_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())

def hit():
    global in_play, score, outcome, game_deck, my_hand, dealer_hand
    
    # if the hand is in play, hit the player
    if in_play:
        my_hand.add_card(game_deck.deal_card())
        if my_hand.get_value() > 21:
            outcome = "You are busted and lose."
            score -= 1
            in_play = False
    
def stand():
    global in_play, score, outcome, game_deck, my_hand, dealer_hand
    
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game_deck.deal_card())
            
        if dealer_hand.get_value() > 21:
            outcome = "Dealer is busted and lose."
            score += 1
        else:
            if dealer_hand.get_value() >= my_hand.get_value():
                score -= 1
                outcome = "Dealer wins!"
            else:
                score += 1
                outcome = "You win!"
                
        in_play = False  
   
# draw handler    
def draw(canvas):
    global outcome, in_play, my_hand, dealer_hand
    canvas.draw_text("Blackjack", [50, 100], 50, "White")
    canvas.draw_text("Dealer", [50, 180], 25, "White")
    canvas.draw_text("Player", [50, 380], 25, "White")
    canvas.draw_text(outcome, [200, 180], 25, "White") 
    canvas.draw_text("Score:" + str(score), [400, 100], 35, "White")
    my_hand.draw(canvas, [100, 400])
    dealer_hand.draw(canvas, [100, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        canvas.draw_text("Hit or stand?", [200, 380], 25, "White")
    else:
        canvas.draw_text("New deal?", [200, 380], 25, "White")
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
