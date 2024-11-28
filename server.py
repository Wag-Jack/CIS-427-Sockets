import socket
from socket import socket, AF_INET, SOCK_STREAM

# Define the server port (using the last 5 digits of Fatima's UMID)
serverPort = 50841
serverSocket = socket(AF_INET, SOCK_STREAM)
print("Socket created successfully.")

#Bind the socket to the server address and port
serverSocket.bind(('', serverPort))
print("Socket bound to port:", serverPort)


#Start listening for incoming connections 
#queue size set to 1
serverSocket.listen(1)
print("Listening for incoming connections...")


print('The server is ready to receive!')


# Default message of the day (motd) and password for for SHUTDOWN

motd = "An apple a day keeps the doctor away"
password = "123!abc"

# Infinite loop to handle multiple client connections
while True:
    # Accept a connection from a client
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")

    while True:
        # Receive data from the client
        sentence = connectionSocket.recv(1024).decode().strip()

        # If no data is received, close the connection
        if not sentence:
            break

        print(f"Received: {sentence}")

        # Handle MSGGET command
        if sentence == "MSGGET":
            response = f"200 OK\n{motd}\n"
            connectionSocket.send(response.encode())

        # Handle MSGSTORE command
        elif sentence == "MSGSTORE":
            connectionSocket.send("200 OK\n".encode())  # Acknowledge client
            new_message = connectionSocket.recv(1024).decode().strip()
            if new_message:
                motd = new_message  # Update the MOTD
                connectionSocket.send("200 OK\n".encode())
            else:
                connectionSocket.send("400 BAD REQUEST\n".encode())

        # Handle QUIT command
        elif sentence == "QUIT":
            connectionSocket.send("200 OK\n".encode())
            print("Client disconnected.")
            break  # Break the inner loop to close client connection

        # Handle SHUTDOWN command
        elif sentence == "SHUTDOWN":
            connectionSocket.send("300 PASSWORD REQUIRED\n".encode())
            password = connectionSocket.recv(1024).decode().strip()
            if password == password:
                connectionSocket.send("200 OKAY\n".encode())
                print("Server shutting down...")
                connectionSocket.close()
                serverSocket.close()
                exit()  # Terminate the server
            else:
                connectionSocket.send("301 WRONG PASSWORD\n".encode())

        # Handle unknown commands
        else:
            connectionSocket.send("400 BAD REQUEST\n".encode())

    # Close the connection 
    connectionSocket.close()
    print("Connection closed.")