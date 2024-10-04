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
    if val[0] in ['Jack', 'Queen', 'King']: # Assign value of 10 to Jack, King, Queen
        return 10
    elif val[0] == 'Ace':   # Assign 11 to Ace automatically
        return 11
    else:
        return int(val[0])  # Else return the number value of the card
################################Documentation Block#####################################
# Function name: gameStatusPrint							  	  
# Description: Prints the status of what the player and dealer currently have on dealers side
# Parameters: list - playerCards - A list of tuples of the players cards - output
#             int - playerSum - the total score of the players cards added up - output
#             list - dealerCards - A list of tuples of the dealers cards - output
#             int - dealerSum - the total score of the dealers cards added up - output
# Return Value: None			  														  
########################################################################################    
def gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum):    # Output current game status
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
def gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket):    # Game status to be sent
    message = [
            "----------------------------", "\n",
            "Player shows: ", str(playerCards), "\n",
            "Player score: ", playerSum, "\n",
            "Dealer shows: ", str(dealerCards[0]), "****", "\n",
            "Dealer score: ", dealer_score, "\n",
            "----------------------------", "\n",
        ]   
    
    message_str = " ".join(map(str, message))   # Format all types to string 
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
    while gameGoesOn:   # While true, continue playing
        # Show current game status
        #gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum)
        #gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket)
        # Receive player's answer (hit or stay)
        answer = connectionSocket.recv(1024).decode()

        if answer.lower() == "stay":    # Do this if player cooses to stay
            gameGoesOn = False
            # Call dealer's action and get the result
            dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, connectionSocket, dealersDeck)
            continue
        elif answer.lower() == "hit":   # Do this if player chooses to hit
            playerCards.append(dealersDeck.pop())   # Choose another card from the deck
            playerSum = addCards(playerCards)   # Add up the new card values
            if playerSum <= 21: # Print updated game status and player chooses again to hit or stay 
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
        if dealerSum < 17 and playerSum <= 21:  # If player didn't bust and dealer score is > 17, dealer must hit
            dealerCards.append(dealersDeck.pop())   # Dealer gets new card
            dealerSum = addCards(dealerCards)   # Add dealers new cards
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
    if playerSum > 21:                              #   PLayer busts
        print("Player busted dealer wins\n")
        message.append("Player busted dealer wins\n")
    elif dealerSum > 21:                            #   Dealer busts
        print("Dealer busted you win\n")
        message.append("Dealer busted you win\n")
    elif playerSum > dealerSum and playerSum <= 21: #   Player score beats dealer score
        print("You win. You beat the dealer\n")
        message.append("You win. You beat the dealer\n")
    elif playerSum < dealerSum:                     #   Dealer score beats player score
        print("House always wins. Dealer wins \n")
        message.append("House always wins. Dealer wins \n")
    else:
        print("It's a tie! \n")
        message.append("It's a tie!\n")             #   Player and dealer scores tie
    # Convert the reply to a string and send it to the client
    message_str = " ".join(map(str, message))
    connectionSocket.send(message_str.encode())

################################Documentation Block#####################################
# Function name: makeDeck							  	  
# Description: initializes the program
# Parameters: None
# Return Value: None			  														  
########################################################################################
def main():
    print("Starting server...")
    serverPort = 16666
    serverSocket = socket(AF_INET, SOCK_STREAM) # Setup socket
    serverSocket.bind(('', serverPort))    
    #serverSocket.listen(5)
    print('The server is ready to receive')
    serverSocket.listen(5)
    while True:
        
        connectionSocket, addr = serverSocket.accept()  # Variable for socket connection
        
        while True:
              # yes or no
            sentence = connectionSocket.recv(1024).decode() # Receive player input to start game
            if 'yes' == sentence:   
                reply = "Okay, let's play a game."
                connectionSocket.send(reply.encode())  # sends confirmation 
                dealersDeck = makeDeck()    # Make the deck of cards
                random.shuffle(dealersDeck) # Shuffle the deck 

                playerCards = []    # List to hold player's cards
                dealerCards = []    # List to hold dealer's cards

                # Deal initial cards
                playerCards.append(dealersDeck.pop())   # Draw player's 1st card 
                dealerCards.append(dealersDeck.pop())   # Draw dealer's 1st card
                playerCards.append(dealersDeck.pop())   # Draw player's 2nd card 
                dealerCards.append(dealersDeck.pop())   # Draw dealer's 2nd card

                playerSum = addCards(playerCards)   # Add player card values
                dealerSum = addCards(dealerCards)   # Add dealer card values
                dealer_score = values(dealerCards[0])   # Dealer score hiding 2nd card

                gameStatusPrint(playerCards, playerSum, dealerCards, dealerSum)
                naWinMes = [
                    "----------------------------", "\n",
                    "Player shows: ", str(playerCards), "\n",
                    "Player score: ", playerSum, "\n",
                    "Dealer shows: ", str(dealerCards),"\n",
                    "Dealer score: ", dealerSum, "\n",
                    "----------------------------", "\n",
                ]

                if dealerSum == 21 and playerSum == 21:     # If both player and dealer draw Blackjack on start
                    naWinMes.append("We both got 21 on the draw, what are the odds it's a tie.\n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    break                
                elif dealerSum == 21:   # Dealer draws Blackjack on start
                    naWinMes.append( "I won with BlackJack before the game even started, too bad so sad.\n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    connectionSocket.close()
                    break
                elif playerSum == 21:   # Player draws Blackjack on start
                    naWinMes.append("You win with Blackjack \n")
                    naturalWinsMessage = " ".join(map(str, naWinMes))
                    connectionSocket.send(naturalWinsMessage.encode())
                    break
                else:
                    youLose = "I didn't win right away, it's go time."
                    connectionSocket.send(youLose.encode())  # sends confirmation 
                
                
                gameStatusSend(playerCards, playerSum, dealerCards, dealer_score, connectionSocket) # Send game status after draw
                
                playerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck)    
                break
            elif 'no' == sentence:  # Player chooses not to play
                message = 'Too bad, I would have won.'
                connectionSocket.send(message.encode())
                break
            else:
                message = 'Invalid input.'  # Check for valid input at start
                connectionSocket.send(message.encode())
        
        connectionSocket.close()  # Close the connection after the game            
        break
    serverSocket.close  # Close server side socket connection

if __name__ == '__main__':
    main()
