openssl req -x509 -newkey rsa:4096 -keyout client.key -out client.crt \
  -days 365 -nodes -subj "/CN=localhost"