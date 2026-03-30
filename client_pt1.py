"""
This program implements a TLS client that verifies the server's certificate
Authors: Long Pham, Tanvi Shegaonkar, Lam Do
Date: March 28, 2026
CS402, Spring 2026
"""

import socket
import ssl
import json

HOST = "localhost"
PORT = 8443

# Initialize TLS client context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Trust server certificate
context.load_verify_locations('server.crt')

with socket.create_connection((HOST, PORT)) as sock:
    # Wrap socket with TLS Context, automatically check server certificate
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        request = {"command": "GET_TIME"}
        ssock.sendall(json.dumps(request).encode())

        response = ssock.recv(4096)
        print("Server Response:", response.decode())
