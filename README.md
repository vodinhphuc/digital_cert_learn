# 🔐 TLS & Digital Certificates Lab (Docker Edition)

This project is a hands-on lab to **learn digital certificates, TLS encryption, and man-in-the-middle (MITM) attacks** using only Docker containers.

It simulates:

1. **No encryption** – exposed to MITM.
2. **TLS with attacker’s own key** – still MITM-vulnerable.
3. **TLS with self-signed cert** – can be spoofed.
4. **TLS with trusted CA** – secure against MITM (if CA is trusted).

The lab lets you play both roles: **user (client)**, **legitimate server**, and **attacker proxy**.

---

## 🧩 Architecture

```
client  --->  mitm_proxy (attacker)  --->  tls_server
```

* **client**: Python script that tries to connect over HTTPS/TLS.
* **tls\_server**: Simple TLS echo server using Python + certificates.
* **mitm\_proxy**: Fake TLS proxy that can decrypt & re-encrypt traffic if the client accepts its certificate.

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/tls-mitm-lab.git
cd tls-mitm-lab
```

### 2. Generate certificates

Run helper script to create:

* attacker cert (self-signed),
* legitimate server cert,
* root CA cert (to sign the server cert).

```bash
./generate-certs.sh
```

Certificates will be placed under `./certs`.

### 3. Build and start containers

```bash
docker compose build
docker compose up -d
```

Check logs:

```bash
docker compose logs -f
```

---

## ▶️ Usage

### Run the client

Enter the client container:

```bash
docker compose exec client bash
```

Run the test script:

```bash
python /app/clients.py
```

### Switch scenarios

Edit `clients.py` to switch between:

* No encryption (plain socket)
* TLS without verification
* TLS with self-signed cert
* TLS with trusted CA cert

Each mode demonstrates different vulnerability levels.

---

## 📂 Project structure

```
.
├── Dockerfile.client       # client image
├── Dockerfile.server       # TLS server image
├── Dockerfile.mitm         # attacker proxy image
├── docker-compose.yml      # orchestrates the lab
├── mitm_proxy.py           # attacker proxy implementation
├── tls_server.py           # simple TLS echo server
├── clients.py              # client test scenarios
├── generate-certs.sh       # helper script to create CA + certs
└── certs/                  # generated certificates
```

---

## 🔬 Learning Objectives

* Understand **how TLS works** in practice.
* See why **certificates must be signed by trusted CAs**.
* Observe how MITM can succeed or fail depending on trust.
* Practice using **Python’s `ssl` library** in client/server code.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Do **not** deploy the MITM proxy outside of a controlled lab environment.

---

## 🚀 Next Steps

* Add **Wireshark/tcpdump** to inspect encrypted vs. unencrypted traffic.
* Extend to **mutual TLS (mTLS)**.
* Implement **certificate pinning** in the client.
