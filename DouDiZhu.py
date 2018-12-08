from AI import ExpectiMiniMaxAI, HillClimbAI, SimulatedAnnealingAI, Other
import Cards
import sys
import numpy as np

""" debug code for hydrogen
class ExpectiMiniMaxAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'ExpectiMiniMaxAI ' + str(order)

    def get_move(self, a, b):
        return []
class HillClimbAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'HillClimbAI ' + str(order)

    def get_move(self, a, b):
        return [Card(1,"a")]

class SimulatedAnnealingAI:
    #order is the order the AIs go: 0, 1, 2 for first, second, third
    def __init__(self, order):
        self.order = order
        self.str = 'SimulatedAnnealingAI ' + str(order)

    def get_move(self, a, b):
        return [Card(2,"b")]
"""

class DDZ:
    def __init__(self, player1, player2, player3):
        self.players = [player1, player2, player3]
        self.current_player = 0 #0 represents player1, 1 represents player2 and 2 represents player3
        self.game_over = False
        self.field = []
        self.origDeck = [Card(3,'diamonds'),Card(3,'clubs'),Card(3,'hearts'),Card(3,'spades'),
                         Card(4,'diamonds'),Card(4,'clubs'),Card(4,'hearts'),Card(4,'spades'),
                         Card(5,'diamonds'),Card(5,'clubs'),Card(5,'hearts'),Card(5,'spades'),
                         Card(6,'diamonds'),Card(6,'clubs'),Card(6,'hearts'),Card(6,'spades'),
                         Card(7,'diamonds'),Card(7,'clubs'),Card(7,'hearts'),Card(7,'spades'),
                         Card(8,'diamonds'),Card(8,'clubs'),Card(8,'hearts'),Card(8,'spades'),
                         Card(9,'diamonds'),Card(9,'clubs'),Card(9,'hearts'),Card(9,'spades'),
                         Card(10,'diamonds'),Card(10,'clubs'),Card(10,'hearts'),Card(10,'spades'),
                         Card(11,'diamonds'),Card(11,'clubs'),Card(11,'hearts'),Card(11,'spades'),
                         Card(12,'diamonds'),Card(12,'clubs'),Card(12,'hearts'),Card(12,'spades'),
                         Card(13,'diamonds'),Card(13,'clubs'),Card(13,'hearts'),Card(13,'spades'),
                         Card(14,'diamonds'),Card(14,'clubs'),Card(14,'hearts'),Card(14,'spades'),
                         Card(15,'diamonds'),Card(15,'clubs'),Card(15,'hearts'),Card(15,'spades'),
                         Card(16,'joker'),Card(17,'joker')]
                         #The original deck of 54 cards including the jokers
        self.landlord = 0 # The landlord represented as an integer
        self.currentPlay = [] #Current play on the board
        self.turn = 0 #Turn number



        #Shuffle cards
        np.random.shuffle(self.origDeck)
        self.deck1 = self.origDeck[:18]
        self.deck1.sort(key = lambda x: x.value)
        self.deck2 = self.origDeck[18:36]
        self.deck2.sort(key = lambda x: x.value)
        self.deck3 = self.origDeck[36:52]
        self.deck3.sort(key = lambda x: x.value)
        self.hands = [self.deck1,self.deck2,self.deck3] #Hands for all of the players in the order of p1,p2,p3
        #the hidden cards in the center of the table
        self.hidden_cards = self.origDeck[52:] #Get from parsing the Game

    #get the stakes [1,2,3] from current_player for the hidden cards.
    def stakes(self):
        return 3

    def unPlayed(self,current_player):
        [card for card in self.origDeck not in (self.field + hands[current_player])]


    def updateCurrentPlay(self,move):
        self.currentPlay.clear()
        self.currentPlay = move



    #get the move they wish to make from current_player.
    def move(self, current_player):
        if(current_player == 0):
            self.players[current_player].get_move(self.deck2, self.currentPlay)
#        self.players[current_player].get_move(self.deck1,len(self.deck2),len(self.deck3),unPlayed())
        elif(current_player == 1):
            self.players[current_player].get_move(self.deck2, self.currentPlay)
        else:
            self.players[current_player].get_move(self.deck3,self.turn, self.currentPlay)


    #update the Game State in response to a move
    def update_game_state(self,move, current_player):
        for ele in move:
            self.hands[current_player].remove(ele) #Removes every card that is being played
            self.field.append(ele) #Append it to the list representing the table
        # if one of the players has no more cards, then they win, and if they're not the landlord, then, their
        # partner wins as well.
        if(len(self.deck1) == 0 or len(self.deck2) == 0 or len(self.deck3) == 0):
            game_over(current_player)
        else: # Otherwise, we update the game state with the moves of each of the players after every turn.
            update_game_state(move(current_player),(current_player+1)%3)
            updateCurrentPlay(move(current_player))
            self.turn += 1

    #Note for this function I have not decided how the stakes function should run yet so I have just hard coded it for now
    def game_over(self, current_player):
        if(self.game_over == true and self.deck1 == 0): #if the game is over and player1's hand is empty
            print ("You have won Landlord!!")
            print ("Game over filthy Peasants")
        elif(self.game_over == false and self.deck2 == 0): #if the game is over and player2's hand is empty
            print ("You and your partner have won " + current_player)
            print ("Game over Landlord")
        else:  #if the game is over and player3's hand is empty
            print ("You and your partner have won " + current_player)
            print ("Game over Landlord")

    def updateLandlord(self,current_player):
        return evalueate_other_player(17,hand,unplayed(current_player))

def create_player(type, order):
    if type == 'ExpectiMiniMaxAI':
        return ExpectiMiniMaxAI(order)
    elif type == 'HillClimbAI':
        return HillClimbAI(order)
    elif type == 'SimulatedAnnealingAI':
        return SimulatedAnnealingAI(order)
    elif type == 'Other':
        return Other(order)

#main function
def main():
    #Parse players from Game State
#    Player1 = 'ExpectiMiniMaxAI'
    Player1 = 'HillClimbAI'
    Player2 = 'HillClimbAI'
    Player3 = 'SimulatedAnnealingAI'

    DDZ(create_player(Player1, 1), create_player(Player2, 2), create_player(Player3, 3))
    DDZ.landlord = updateLandlord(self.current_player)
    DDZ.hands[DDZ.landlord] = DDZ.hands[DDZ.landlord] + DDZ.hidden_cards

if __name__== '__main__':
    main()
