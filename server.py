"""
server.py
Authors:
Description: 
"""

import socket
import ssl
import json
import datetime
import logging

HOST = "127.0.0.1"
PORT = 8443
logging.basicConfig(filename="TLS_log.txt", level=logging.INFO)

# Initialize TLS Server context object
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# Load certificate and private key to TLS Server Context object
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Bind TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Secure server listening on {PORT}")

    # Wrap socket with TLS Context, perform handshake on connect
    with context.wrap_socket(sock, server_side=True, do_handshake_on_connect=True) as ssock:
        while True: 
            conn, addr = ssock.accept()
            print("Connection from", addr)
            # Log negotitated TLS version and cipher suite
            logging.info(f"Connection from {addr}")
            logging.info(f"TLS version: {conn.version()}")
            logging.info(f"Cipher suite: {conn.cipher()}")

            data = conn.recv(4096)
            request = json.loads(data.decode())

            if request.get("command") == "GET_TIME":
                response = {"time": datetime.datetime.now(
                    datetime.timezone.utc).isoformat()}
            else:
                response = {"error": "Unknown command"}

            conn.sendall(json.dumps(response).encode())
