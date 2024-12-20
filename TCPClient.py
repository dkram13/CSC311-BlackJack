##########Documentation Block ##################################
# Authors: Dustin Kramer, Jesse Quier                                       						
# Major: Computer Science                                       
# Creation Date: September 16, 2024                                
# Due Date: October 4, 2024                                   
# Course: CSC311 Section 010                                    
# Professor Name: Professor Jici Huang                       
# Assignment: Computer Networks                                        
# Filename: TCPClient.py                                    
# Purpose: Connects to the server and plays a game of Blackjack
#           
################################################################
from socket import *
################################Documentation Block#####################################
# Function name: main						  	  
# Description: initializes the program
# Parameters: None
# Return Value: None			  														  
########################################################################################
def main():
    serverName = '127.0.0.1'
    serverPort = 16666
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))  # Connects via socket
    print('\n Connect to:', '127.0.0.1, 16666')

    while True:
        intro = input('Would you like to play a game of black jack (yes or no only): ').lower()  # asks user if they want to play
        if intro != "yes" and intro != "no":
            print("please type either yes or no")
            continue
        clientSocket.send(intro.encode())  # sends user's answer
        if intro.lower() == "no":  # gets us out of game if user says no
            start_reply = clientSocket.recv(1024).decode()
            print(start_reply)
            break
        
        start_reply = clientSocket.recv(1024).decode()  # receives confirmation of game
        print(start_reply)
        heWon = clientSocket.recv(1024).decode()
        if "I won with" in heWon: # Dealer wins with Blackjack
            print(heWon)
            break
        elif "We both got 21" in heWon:  # Game results in tie
            print(heWon)
            break
        elif "You win with Blackjack" in heWon:  # Player wins with Blackjack
            print(heWon)
            break
        else:
            print(heWon)
        deal_message = clientSocket.recv(1024).decode()# receives the card draw message from server
        print(deal_message)
        iWannaPlay = True   # Boolean to start the loop into the game

        while iWannaPlay:
            
            hitOrStay = input("Would you like to hit or stay: ").lower()  # asks user to hit or stay
            if hitOrStay != "hit" and hitOrStay != "stay":  # Checks for valid input
                print("Either hit or stay can't be anything else")
                continue
            clientSocket.send(hitOrStay.encode())  # sends user's answer to the server
            
            if hitOrStay.lower() == "stay": # Player chooses to stay
                print(clientSocket.recv(1024).decode())
                iWannaPlay = False  # breaks the loop if the user chooses to stay
            elif hitOrStay.lower() == "hit":    # Player chooses to hit
                statusAfterHit = clientSocket.recv(1024).decode()
                print(statusAfterHit)   # Print updated game status after hitting
                if "win" in statusAfterHit or "tie" in statusAfterHit:  
                    break
        break
    clientSocket.close()    # Close the socket

if __name__ == '__main__':
    main()

