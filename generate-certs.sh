#!/usr/bin/env bash
set -e
mkdir -p /certs/ca /certs/server /certs/selfsigned /certs/attacker
cd /certs

echo "[*] Generating CA..."
openssl genrsa -out ca/ca-key.pem 2048
openssl req -x509 -new -nodes -key ca/ca-key.pem -sha256 -days 3650 -subj "/CN/LocalTestRootCA" -out ca/ca.pem

echo "[*] Generating server key + CSR..."
openssl genrsa -out server/server-key.pem 2048
openssl req -new -key server/server-key.pem -subj "/CN=tls_server" -out server/server.csr

echo "[*] Signing server CSR with CA..."
openssl x509 -req -in server/server.csr -CA ca/ca.pem -CAkey ca/ca-key.pem -CAcreateserial \
  -out server/server.pem -days 825 -sha256 -extfile <(printf "subjectAltName=DNS:tls_server,DNS:localhost,IP:127.0.0.1")

echo "[*] Generating self-signed server cert..."
openssl req -x509 -nodes -newkey rsa:2048 -keyout selfsigned/selfsigned-key.pem \
  -out selfsigned/selfsigned.pem -days 365 -subj "/CN=tls_server" \
  -addext "subjectAltName=DNS:tls_server,DNS:localhost,IP:127.0.0.1"

echo "[*] Generating attacker cert (self-signed), using same CN to emulate attacker spoof..."
openssl genrsa -out attacker/attacker-key.pem 2048
openssl req -x509 -new -nodes -key attacker/attacker-key.pem -sha256 -days 365 \
  -subj "/CN=tls_server" -out attacker/attacker.pem -addext "subjectAltName=DNS:tls_server,DNS:attacker,IP:127.0.0.1"

echo "[*] Certificates generated under /certs:"
ls -R

# Keep container alive briefly so docker compose doesn't treat it as crashed (a one-shot run is fine too).
sleep 1
echo "[*] Done."