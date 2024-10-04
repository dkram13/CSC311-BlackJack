##########Documentation Block ##################################
# Authors: Dustin Kramer, Jesse Quier                                       						
# Major: Computer Science                                       
# Creation Date: September 16, 2024                                
# Due Date: October 4, 2024                                   
# Course: CSC311 Section 010                                    
# Professor Name: Professor Jici Huang                       
# Assignment: Computer Networks                                        
# Filename: TCPServer.py                                    
# Purpose: Looks for a client to play a game of Blackjack with and acts as the dealer
#          for the client.           
################################################################

from socket import *
import random

################################Documentation Block#####################################
# Function name: makeDeck							  	  
# Description: creates a tuple of a deck of cards that contains sets of card values and
#              card suites.
# Parameters: None
# Return Value: returns the list of tuples containing all the cards and numbers for
#               the cards.			  														  
########################################################################################
def makeDeck():
    cardSuits = ["Hearts", 'Diamonds', 'Spades', 'Clubs'] # a list of all the card suits
    cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] # a list of all the card numbers
    deck = [(val, suit) for val in cardValues for suit in cardSuits] # creates a list of tuples for   
    return deck
################################Documentation Block#####################################
# Function name: addCards							  	  
# Description: adds the cards in the hand of a player/dealer
# Parameters: list - cards - a list of tuples holding the cards in player/dealer hand - input 
# Return Value: returns the total value of the cards in hand of player/dealers			  														  
########################################################################################
def addCards(cards):
    cardsTotal = 0
    ace_count = 0

    for card in cards:
        if card[0] in ['Jack', 'Queen', 'King']:
            cardsTotal += 10
        elif card[0] == 'Ace':
            cardsTotal += 11  # Initially count Ace as 11
            ace_count += 1
        else:
            cardsTotal += int(card[0])  # Convert card value to int
    # Adjust for Aces if total exceeds 21
    while cardsTotal > 21 and ace_count:
        cardsTotal -= 10  # Count one Ace as 1 instead of 11
        ace_count -= 1

    return cardsTotal
################################Documentation Block#####################################
# Function name: values						  	  
# Description: adds a value to cards with a non-standard value
# Parameters: None
# Return Value: 			  														  
########################################################################################
def values(val):
    if val[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif val[0] == 'Ace':	
        return 11
    else:
        return int(val[0]) 
################################Documentation Block#####################################
# Function name: gameStatusPrint							  	  
# Description: Prints the status of what the player and dealer currently have on dealers side
# Parameters: list - playerCards - A list of tuples of the players cards - output
#             int - playerSum - the total score of the players cards added up - output
#             list - dealerCards - A list of tuples of the dealers cards - output
#             int - dealerSum - the total score of the dealers cards added up - output
# Return Value: None			  														  
########################################################################################    
def gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum):
    print("----------------------------")
    print("Player shows: ", playerCards)
    print("Player score: ", playerSum)
    print("Dealer shows: ", dealerCards)
    print("Dealer score: ", dealerSum )
    print("----------------------------")
################################Documentation Block#####################################
# Function name: gameStatusSend 							  	  
# Description: sends the game status to the client
# Parameters: list - playerCards - A list of tuples of the players cards - output
#             int - playerSum - the total score of the players cards added up - output
#             list - dealerCards - A list of tuples of the dealers cards - output
#             int - dealer_score - the card number for the first card in the dealers hand - output
#             connectionSocket - socket connection to the client - input/output
# Return Value: returns the list of tuples containing all the cards and numbers for
#               the cards.			  														  
########################################################################################
def gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket):
    message = [
            "----------------------------", "\n",
            "Player shows: ", str(playerCards), "\n",
            "Player score: ", playerSum, "\n",
            "Dealer shows: ", str(dealerCards[0]), "****", "\n",
            "Dealer score: ", dealer_score, "\n",
            "----------------------------", "\n",
        ]   
    
    message_str = " ".join(map(str, message))
    connectionSocket.send(message_str.encode())  # sends the card draw
################################Documentation Block#####################################
# Function name: playerHitOrStay						  	  
# Description: A loop that gives the player the option of either hit or stay
# Parameters: list - playerCards - A list of tuples of the players cards - output
#             int - playerSum - the total score of the players cards added up - output
#             list - dealerCards - A list of tuples of the dealers cards - output
#             int - dealerSum - the total score of the dealers cards added up - output
#             int - dealer_score - the card number for the first card in the dealers hand - output
#             connectionSocket - socket connection to the client - input/output
#             dealersDeck - A list of tuples that simulates a deck of cards  - input/output
# Return Value: None		  														  
########################################################################################
def playerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck):
    gameGoesOn = True
    while gameGoesOn:
        # Show current game status
        #gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum)
        #gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket)
        # Receive player's answer (hit or stay)
        answer = connectionSocket.recv(1024).decode()

        if answer.lower() == "stay":
            gameGoesOn = False
            # Call dealer's action and get the result
            dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, connectionSocket, dealersDeck)
            continue
        elif answer.lower() == "hit":
            playerCards.append(dealersDeck.pop())
            playerSum = addCards(playerCards)
            if playerSum <= 21:
                gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket)
            elif playerSum > 21:
                dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, connectionSocket, dealersDeck)
                gameGoesOn = False
################################Documentation Block#####################################
# Function name: dealerHitOrStay							  	  
# Description: A loop that makes the dealer hit if below 17 and less than the player as well
#             sending game results to the player on who won.
# Parameters: list - playerCards - A list of tuples of the players cards - output
#             int - playerSum - the total score of the players cards added up - output
#             list - dealerCards - A list of tuples of the dealers cards - output
#             int - dealerSum - the total score of the dealers cards added up - output
#             connectionSocket - socket connection to the client - input/output
#             dealersDeck - A list of tuples that simulates a deck of cards  - input/output
# Return Value: None			  														  
########################################################################################        
def dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, connectionSocket, dealersDeck):
    dealersTurn = True
    while dealersTurn:
        if dealerSum < 17 and playerSum <= 21:#and dealerSum < playerSum and playerSum > 21:
            dealerCards.append(dealersDeck.pop())
            dealerSum = addCards(dealerCards)
        else :#dealerSum >= 17 or dealerSum < playerSum:
            dealersTurn = False
    print("Its the dealers turn now")
    print("----------------------------")
    print("Player shows: ", playerCards)
    print("Player score: ", playerSum)
    print("Dealer shows: ", dealerCards)
    print("Dealer score: ", dealerSum)
    print("----------------------------")

    # Prepare the message to send to the client
    message = [
        "It's the dealers turn now \n"
        "----------------------------", "\n",
        "Player shows: ", str(playerCards), "\n",
        "Player score: ", playerSum, "\n",
        "Dealer shows: ", str(dealerCards),"\n",
        "Dealer score: ", dealerSum, "\n",
        "----------------------------", "\n",
    ]
    # Determine the winner
    if playerSum > 21:
        message.append("Player busted dealer wins\n")
    elif dealerSum > 21:
        message.append("Dealer busted you win\n")
    elif playerSum > dealerSum and playerSum <= 21:
        message.append("You win. You beat the dealer\n")
    elif playerSum < dealerSum:
        message.append("House always wins. Dealer wins \n")
    else:
        message.append("It's a tie!\n")
    # Convert the reply to a string and send it to the client
    message_str = " ".join(map(str, message))
    connectionSocket.send(message_str.encode())

################################Documentation Block#####################################
# Function name: makeDeck							  	  
# Description: creates a tuple of a deck of cards that contains sets of card values and
#              card suites.
# Parameters: None
# Return Value: returns the list of tuples containing all the cards and numbers for
#               the cards.			  														  
########################################################################################
def main():
    print("Starting server...")
    serverPort = 16666
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    #serverSocket.listen(5)
    print('The server is ready to receive')
    serverSocket.listen(5)
    while True:
        
        connectionSocket, addr = serverSocket.accept()
        
        while True:
              # yes or no
            sentence = connectionSocket.recv(1024).decode()
            if 'yes' == sentence:
                reply = "Okay, let's play a game."
                connectionSocket.send(reply.encode())  # sends confirmation 
                dealersDeck = makeDeck()
                random.shuffle(dealersDeck)

                playerCards = []
                dealerCards = []

                # Deal initial cards
                playerCards.append(dealersDeck.pop())
                dealerCards.append(dealersDeck.pop())
                playerCards.append(dealersDeck.pop())
                dealerCards.append(dealersDeck.pop())

                playerSum = addCards(playerCards)
                dealerSum = addCards(dealerCards)
                dealer_score = values(dealerCards[0])

                gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum)
                naWinMes = [
                    "----------------------------", "\n",
                    "Player shows: ", str(playerCards), "\n",
                    "Player score: ", playerSum, "\n",
                    "Dealer shows: ", str(dealerCards),"\n",
                    "Dealer score: ", dealerSum, "\n",
                    "----------------------------", "\n",
                ]

                if dealerSum == 21 and playerSum == 21:
                    naWinMes.append("We both got 21 on the draw, what are the odds it's a tie.\n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    break                
                elif dealerSum == 21:
                    naWinMes.append( "I won with BlackJack before the game even started, too bad so sad.\n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    connectionSocket.close()
                    break
                elif playerSum == 21:
                    naWinMes.append("You win with Blackjack \n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    break
                else:
                    youLose = "I didn't win right away, it's go time."
                    connectionSocket.send(youLose.encode())  # sends confirmation 
                
                
                gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket)
                
                playerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck)
                break
            elif 'no' == sentence:
                message = 'Too bad, I would have won.'
                connectionSocket.send(message.encode())
                break
            else:
                message = 'Invalid input.'
                connectionSocket.send(message.encode())
        
        connectionSocket.close()  # Close the connection after the game            
        break
    serverSocket.close

if __name__ == '__main__':
    main()
