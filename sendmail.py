import socket

# Server details
server_ip = "10.22.100.123"  # Replace with the server's IP address
server_port = 5003  # Port number for the server

# Set up the socket for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(melding):
    # Send melding til serveren
    try:
        sock.sendto(melding.encode('utf-8'), (server_ip, server_port))
        print("Data sent successfully.")
    except Exception as e:
        print(f"Error sending data: {e}")