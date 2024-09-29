from socket import *

def main():
    serverName = '127.0.0.1'
    serverPort = 16666
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print('\n Connect to:', '127.0.0.1, 16666')
    while True:
        intro = input('Would you like to play a game of black jack: ')   # asks user if they want to play
        clientSocket.send(intro.encode()) # sends users answer
        if intro.lower() == "no": # gets us out of game if users says no
            print("Exiting the game.") 
            break
        start_reply = clientSocket.recv(1024).decode() # receives the reply could be one of three
        print(start_reply)
        
        deal_message = clientSocket.recv(1024).decode()
        print(deal_message)

        flag = clientSocket.recv(1024).decode()
        while flag == 'True':
            hit_message = input('Hit / Stay: ')
            clientSocket.send(hit_message.encode())
            #ace_message = clientSocket.recv(1024).decode()
        if flag == 'False':
            message = clientSocket.recv(1024).decode()
            print(message)
        elif flag == 'Ace':
            ace_choice = input('Choose value of Ace (1 / 11): ')
            clientSocket.send(ace_choice.encode())
            
        
        

        #hit_message = input('Hit / Stay: ')
        #clientSocket.send(hit_message.encode())

        reply = clientSocket.recv(1024).decode()
        print(reply)

    clientSocket.close()

if __name__ == '__main__':
    main()