import socket

def start_client(host='127.0.0.1', port=8888):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send data to the server
        message = "Hello, Server!"
        client_socket.sendall(message.encode())
        print(f"Sent: {message}")

        # Receive data from the server
        data = client_socket.recv(1024)
        print(f"Received: {data.decode()}")

    finally:
        # Close the client socket
        client_socket.close()

# Run the client
#start_client()


# Run the server
if __name__ == "__main__":
    start_client()
