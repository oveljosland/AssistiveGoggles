import socket
import requests
import os



def send_simple_message(melding):
  	return requests.post(
  		"https://api.mailgun.net/v3/sandboxaf2a95ab3c2a42a783f05b8e267882ba.mailgun.org/messages",
  		auth=("api", "540ee7a6997fc805569756e9c607af46-784975b6-ef4347c1"),
  		data={"from": "Excited User <mailgun@sandboxaf2a95ab3c2a42a783f05b8e267882ba.mailgun.org>",
  			"to": "mathias.schiotz@hotmail.no",
  			"subject": "Melding fra Nvision",
  			"text": melding})

# Server details
server_ip = "0.0.0.0"  # Listen on all available network interfaces
server_port = 5003  # The port number to listen on

# Set up the socket for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

print(f"Listening for GPS data on {server_ip}:{server_port}...")

try:
    while True:
        # Receive data from the sender (maximum buffer size of 1024 bytes)
        data, addr = sock.recvfrom(1024)
        print(f"Received data from {addr}: {data.decode('utf-8')}")
        melding = data.decode('utf-8')
        send_simple_message(melding)

except KeyboardInterrupt:
    print("\nStopping the server...")

finally:
    sock.close()
