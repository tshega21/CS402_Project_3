"""
This program is an extension of server_pt1.py 
where server now requires certificate from the client and enforces minimum TLS version of 1.3.

Authors: Long Pham, Tanvi Shegaonkar, Lam Do
Date: March 28, 2026
CS402, Spring 2026
"""

import socket
import ssl
import json
import datetime
import logging

HOST = "127.0.0.1"
PORT = 8443

# Configure logging 
logging.basicConfig(
    filename="TLS_log_pt3.txt",
    level=logging.INFO,
    format = "%(asctime)s- %(message)s"
)

# Initialize TLS server context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# Load certificate and private key to TLS server context
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Enforce minimum TLS version of 1.3
context.minimum_version = ssl.TLSVersion.TLSv1_3

# Require client certificate
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('client.crt')

# Bind TCP Socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Secure server listening on {PORT}")

    # Wrap socket with TLS Context, perform handshake on connect
    with context.wrap_socket(sock, server_side=True, do_handshake_on_connect=True) as ssock:
        while True: 
            conn, addr = ssock.accept()
            session = conn.session
            print("Connection from", addr)
            
            # Add structured logging of TLS session details
            log_entry = {
                "event": "tls_connection",
                "client_addr": addr,
                "tls_version": conn.version(),
                "cipher_suite": conn.cipher(),
                "session_id": session.id.hex(),
                "session_time": datetime.datetime.fromtimestamp(session.time, tz=datetime.timezone.utc).isoformat(),
                "session_timeout": session.timeout,
                "session_has_ticket": session.has_ticket,
            }
            logging.info(json.dumps(log_entry))

            data = conn.recv(4096)
            request = json.loads(data.decode())

            if request.get("command") == "GET_TIME":
                response = {"time": datetime.datetime.now(
                    datetime.timezone.utc).isoformat()}
            else:
                response = {"error": "Unknown command"}

            conn.sendall(json.dumps(response).encode())
