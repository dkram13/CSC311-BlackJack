from socket import *

def main():
    serverName = '127.0.0.1'
    serverPort = 16666
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
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
        if "I won with" in heWon:
            print(heWon)
            break
        elif "We both got 21" in heWon:  # Fixing the indentation here
            print(heWon)
            break
        elif "You win with Blackjack" in heWon:  # Fixing the indentation here
            print(heWon)
            break
        else:
            print(heWon)
        deal_message = clientSocket.recv(1024).decode()# receives the card draw message from server
        print(deal_message)
        iWannaPlay = True

        while iWannaPlay:
            
            hitOrStay = input("Would you like to hit or stay: ").lower()  # asks user to hit or stay
            if hitOrStay != "hit" and hitOrStay != "stay":
                print("Either hit or stay can't be anything else")
                continue
            clientSocket.send(hitOrStay.encode())  # sends user's answer to the server
            
            if hitOrStay.lower() == "stay":
                print(clientSocket.recv(1024).decode())
                iWannaPlay = False  # breaks the loop if the user chooses to stay
            elif hitOrStay.lower() == "hit":
                statusAfterHit = clientSocket.recv(1024).decode()
                print(statusAfterHit)
                if "win" in statusAfterHit or "tie" in statusAfterHit:
                    break
        break
    clientSocket.close()

if __name__ == '__main__':
    main()
## Server sends cards and asks to Hit or Stay
## if the dealer is dealt 21 games over right away
## server starts and get the cards ready to send
## client receives cards and sends back an answer
