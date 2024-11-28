from socket import *

# Define the server name and port
serverName = '127.0.0.1'  # Use localhost for testing
serverPort = 50841

# Create a TCP client socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverName, serverPort))
print(f"Connected to server at {serverName}:{serverPort}")

while True:
    # Prompt the user for a command
    print("\nAvailable commands: MSGGET, MSGSTORE, QUIT, SHUTDOWN")
    command = input("Enter command: ").strip()

    # Send the command to the server
    clientSocket.send(command.encode())

    # Handle MSGGET command
    if command == "MSGGET":
        response = clientSocket.recv(1024).decode()
        print(f"From Server:\n{response}")

    # Handle MSGSTORE command
    elif command == "MSGSTORE":
        # Wait for server acknowledgment
        response = clientSocket.recv(1024).decode()
        print(f"From Server: {response}")

        # Only proceed if the server acknowledges
        if "200 OK" in response:
            new_message = input("Enter new message of the day: ")
            clientSocket.send(new_message.encode())
            # Receive final response from the server
            final_response = clientSocket.recv(1024).decode()
            print(f"From Server: {final_response}")

    # Handle QUIT command
    elif command == "QUIT":
        response = clientSocket.recv(1024).decode()
        print(f"From Server: {response}")
        print("Closing connection...")
        break  # Exit the loop and close the client

    # Handle SHUTDOWN command
    elif command == "SHUTDOWN":
        # Wait for the server's password request
        response = clientSocket.recv(1024).decode()
        print(f"From Server: {response}")

        # Proceed only if the server requests the password
        if "300 PASSWORD REQUIRED" in response:
            password = input("Enter password: ")
            clientSocket.send(password.encode())

            # Receive final response from the server
            final_response = clientSocket.recv(1024).decode()
            print(f"From Server: {final_response}")

            # If shutdown is successful, close the client
            if "200 OKAY" in final_response:
                print("Server is shutting down. Closing connection...")
                break

    # Handle invalid command
    else:
        response = clientSocket.recv(1024).decode()
        print(f"From Server: {response}")

# Close the client socket
clientSocket.close()
print("Connection closed.")
 