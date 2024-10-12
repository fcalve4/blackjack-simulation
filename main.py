import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# CONSTANTS
        
NUM_SIMULATIONS = 1000000

NUM_DEKCS = 6
H17 = False # If H17 is True, dealer hits soft17, if false, dealer stands on soft17
DAS = True
MAX_SPLITS = 4 # Not factored in yet
RSA = True # Not factored in yet
HSA = False # Not factored in yet
LS = True
BJ_PAY = 1.5
PENN = 0.8

BANKROLL = 1000000000
WAGER_SIZE = 10

class BlackjackSimulation():
    def __init__(self):
        



        # Initialize attributes
        self.bankroll = BANKROLL
        self.wager_size = WAGER_SIZE
        self.num_simulations = NUM_SIMULATIONS
        self.running_count = 0 # The running count for the simulation

        self.num_decks = NUM_DEKCS
        self.h17 = H17
        self.das = DAS
        self.max_splits = MAX_SPLITS
        self.rsa = RSA
        self.hsa = HSA
        self.ls = LS
        self.bj_pay = BJ_PAY
        self.penn = PENN

        # Ini
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 'A'] * 4 
        



    def deal_card(self, shoe):
        # Deal a card from the shoe
        card = shoe.pop()

        # Update running count
        if (card == 'A' or card == 10):
            self.running_count -= 1
        elif card <=6:
            self.running_count += 1

        return card
    

    def check_for_blackjack(self, player_hand, dealer_hand):

        player_natural = False
        dealer_natural = False 

    
        if (10 in player_hand and 'A' in [card for card in player_hand if isinstance(card, str)]):
            player_natural = True
        
        if (10 in dealer_hand and 'A' in [card for card in dealer_hand if isinstance(card, str)]):
            dealer_natural = True
     

        return player_natural, dealer_natural


    def calculate_hand_total(self, hand):
        total = 0
        aces = 0

        for card in hand:
            if card == 'A':
                aces += 1
                total += 11
            else:
                total += card

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total, 'soft' if aces else 'hard'
    

    def is_hand_splittable(self, hand):
        # Check if the hand is splittable (two cards of the same rank)
        return len(hand) == 2 and hand[0] == hand[1]
    

    def is_hand_doublable(self, hand):
        return len(hand) == 2
    

    def check_strategy_sheet(self, player_hand, dealer_hand):
        # Find the strategy sheet and save it
        strategy_sheet = pd.read_csv('strategy.csv', index_col = 0)

        player_total, soft_or_hard = self.calculate_hand_total(player_hand)

        
        dealer_upcard = str(dealer_hand[0])

        splitable = self.is_hand_splittable(player_hand)
        doublable = self.is_hand_doublable(player_hand)


        # SURRENDER CASE
        if (self.ls == True and len(player_hand) == 2):
            # Checks the strategy sheet for surrenders only if LS is active
            try:
                row_label = 'surrender' + str(player_total)
                action = strategy_sheet.loc[row_label, dealer_upcard]
                
                if (action == 'Y'):
                    return 'surrender'
                
            except KeyError as e:
                pass

        # SPLITABLE CASE
        if (splitable == True):
            row_label = 'split' + str(player_hand[0])
            action = strategy_sheet.loc[row_label, dealer_upcard]

            if (action == 'Y'):
                return 'split'
                

        # Hard totals 
        if (soft_or_hard == 'hard'):
            # checks the strategy sheet for hard totals
            row_label = 'hard' + str(player_total)
            action = strategy_sheet.loc[row_label, dealer_upcard]

            if (action == 'D' and doublable == True):
                return 'double'
            elif (action == 'D' and doublable == False):
                return 'hit'
            elif (action == 'H'):
                return 'hit'
            else:
                return 'stand'
            


        # Soft totals
        elif (soft_or_hard == 'soft'):
            row_label = 'soft' + str(player_total)
            action = strategy_sheet.loc[row_label, dealer_upcard]

            if (action == 'D' and doublable == True):
                return 'double'
            elif (action == 'D' and doublable == False):
                return 'hit'
            elif (action == 'Ds' and doublable == True):
                return 'double'
            elif (action == 'Ds' and doublable == False):
                return 'stand'
            elif (action == 'H'):
                return 'hit'
            else:
                return 'stand'

    def dealer_logic(self, shoe, dealer_hand):
        dealer_total, soft_or_hard = self.calculate_hand_total(dealer_hand)
        if self.h17 == True:
            while dealer_total < 17 or (dealer_total == 17 and soft_or_hard == 'soft'):
                dealer_hand.append(self.deal_card(shoe))
                dealer_total, soft_or_hard = self.calculate_hand_total(dealer_hand)
                #print("new dealer hand:" + str(dealer_hand))
        else:
            while dealer_total < 17:
                dealer_hand.append(self.deal_card(shoe))
                dealer_total, soft_or_hard = self.calculate_hand_total(dealer_hand)
                #print("new dealer hand:" + str(dealer_hand))
        #print ("dealer total: " + str(dealer_total))
        return dealer_total
    


    def initial_deal(self, shoe):
        # Deal two cards to the player
        player_hand = [self.deal_card(shoe), self.deal_card(shoe)]

        dealer_hand = [self.deal_card(shoe), self.deal_card(shoe)]

        return player_hand, dealer_hand



   

    def play_hand_with_logic(self, shoe, player_hand, dealer_hand):
        #print("Running play_hand_with_logic")
        # Reset wager size
        self.wager_size =  WAGER_SIZE 

        hand_count = 1
        
        ##########################################################################################################################################################
        # Find the player and dealer hand totals, as well as whether or not they are splitable, soft, should double, or surrenderable OR IF IT IS A BLACKJACK!!!!.
        ############################################################################################################################################################
        
        # First check for naturals
        player_natural, dealer_natural = self.check_for_blackjack(player_hand, dealer_hand)

        if (player_natural and dealer_natural):
            #print("Both players have naturals, Push")
            return 0
        elif (player_natural and not dealer_natural):
            #print("Player natural! Won 1.5x wager")
            return self.wager_size * self.bj_pay
            
        elif (not player_natural and dealer_natural):
            #print("Dealer has a natural, lost wager")
            return self.wager_size * -1

        while (self.calculate_hand_total(player_hand)[0] <= 21):    
            # Check what action the player should take
            action = self.check_strategy_sheet(player_hand, dealer_hand)
            #print("Checking strategy sheet.......")
            #print("player hand:" + str(player_hand) + "--------" + "dealer hand:" + str(dealer_hand) + "--------" + "action: " + action)

            if (action == 'stand'):
                # Dealer logic and compare totals
                dealer_total = self.dealer_logic(shoe, dealer_hand)
                player_total = self.calculate_hand_total(player_hand)
                #print("Player standing on: " + str(player_total))
                if (player_total[0] > dealer_total or dealer_total > 21):
                    #print("Won 1x wager")
                    return self.wager_size * 1
                elif (player_total[0] < dealer_total):
                    #print("Lost 1x wager")
                    return self.wager_size * -1
                
                else:
                    #print("Push")
                    return 0

            elif (action == 'hit'):
                # Add card for the player and check strategy again
                player_total = self.calculate_hand_total(player_hand)
                #print("Player hitting on: " + str(player_total))
                new_card = self.deal_card(shoe)
                player_hand.append(new_card)
                #print("Player has been dealt a " + str(new_card) + " for a new total of " + str(self.calculate_hand_total(player_hand)))

            elif (action == 'double'):
                # Double the wager, give the player a card, and do dealer logic and compare totals
                player_total = self.calculate_hand_total(player_hand)
                #print("Player doubling on: " + str(player_total))
                new_card = self.deal_card(shoe)
                player_hand.append(new_card)
                #print("Player has been dealt a " + str(new_card) + " for a new total of " + str(self.calculate_hand_total(player_hand)))
                #print("Players new hand is: " + str(player_hand))
                dealer_total = self.dealer_logic(shoe, dealer_hand)
                player_total = self.calculate_hand_total(player_hand)

                if (player_total[0] > dealer_total or dealer_total > 21):
                    self.wager_size = self.wager_size * 2
                    #print("Win 2x wager")
                    return self.wager_size
                elif (player_total[0] < dealer_total):
                    self.wager_size = self.wager_size * 2
                    #print("Lose 2x wager")
                    return self.wager_size * -1
                    
                else:
                    #print("Push")
                    return 0

            elif (action == 'split'):
                # Implement split logic
                # Play the hand out twice using recursion
                #print("PLAYER SPLITTING")
                hand_count += 1
                shoe1 = shoe
                shoe2 = shoe
                player_hand1 = []
                player_hand2 = []
                player_hand1.append(player_hand.pop())   
                player_hand1.append(shoe.pop())     
                player_hand2.append(player_hand.pop())
                player_hand2.append(shoe.pop())     

                #print("Playerhand 1: " + str(player_hand1))
                #print("Playerhand 2: " + str(player_hand2))
                
                return self.play_hand_with_logic(shoe1, player_hand1, dealer_hand) + self.play_hand_with_logic(shoe2, player_hand2, dealer_hand)

            elif (action == 'surrender'):
                #print("Player surrendering on " + str(self.calculate_hand_total(player_hand)) + "vs dealer " + str(dealer_hand[0])) 
                #print("Lost 0.5x wager")
                return self.wager_size * 0.5 * -1

        return self.wager_size * -1


    def game_loop(self):

        # Create the shoe
        shoe = self.deck * self.num_decks

        # Shuffle the shoe
        random.shuffle(shoe)

        # Initialize counters
        net_credits = 0
        num_hands = 0
        num_wagered = 0
        total_credits_won = 0 
        


        # Plot Datasets
        x = []
        y = []

        for _ in range(self.num_simulations): # range of 10 to test <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< NUMBER OF SIMULATIONS <<<<<<<<<<<<<<<<<<<<<<<<<<

            # Shuffle the shoe at the cut
            if (len(shoe) < 52 * self.num_decks * (1 - self.penn)):
                shoe = self.deck * self.num_decks
                random.shuffle(shoe)
                self.running_count = 0
            # Play the hand
            player_hand, dealer_hand = self.initial_deal(shoe)
            num_credits_won_or_lost_during_hand = self.play_hand_with_logic(shoe, player_hand, dealer_hand)
            # Update the counters
            net_credits += num_credits_won_or_lost_during_hand
            if num_credits_won_or_lost_during_hand >= 0:
                total_credits_won += num_credits_won_or_lost_during_hand
                total_credits_won += self.wager_size
            num_wagered += self.wager_size
            num_hands += 1

            
            


            
            print("Net credits: " + str(net_credits) + " ----- Num hands:" + str(num_hands) +  "------num won:" + str(total_credits_won) +" ----- Num wagered:"  + str(num_wagered) 
                  + " ----- RTP :" + str(total_credits_won / num_wagered * 100))

            # Add data points to plot variables
            x.append(num_hands)
            y.append(net_credits)

        # Fit a linear trendline (1st degree polynomial)
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        trendline = polynomial(x)
        plt.plot(x, trendline, 'r--', label='Trendline')  # Trendline
        plt.plot(x, y, marker='o', linestyle='-', color='b', linewidth=1)
        plt.legend()

        plt.grid(True)
        plt.xlabel('Number of hands')
        plt.ylabel('Net credits')
        plt.title("Blackjack Simulation Graph")

        plt.show()

        # Return the net credits won or lost
        return net_credits





if __name__ == '__main__':
    
    bj_sim = BlackjackSimulation()


    bj_sim.game_loop()