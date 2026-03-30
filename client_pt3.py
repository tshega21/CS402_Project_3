"""
This program is an extension of client_pt1.py 
where client now presents ceritificate to the server and enforces minimum TLS version of 1.3

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
# Load certificate and private key to TLS client context
context.load_cert_chain(certfile="client.crt", keyfile="client.key")

# Enforce minimum TLS version of 1.3
context.minimum_version = ssl.TLSVersion.TLSv1_3

# Trust server certificate
context.load_verify_locations('server.crt')

with socket.create_connection((HOST, PORT)) as sock:
    # Wrap socket with TLS Context
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        request = {"command": "GET_TIME"}
        ssock.sendall(json.dumps(request).encode())

        response = ssock.recv(4096)
        print("Server Response:", response.decode())
