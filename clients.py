import requests, urllib3, sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scenario1_plain_http():
    r = requests.get("http://plain_server:8000/")
    print("Scenario 1 (plain HTTP):", r.status_code, r.text.strip())

def scenario2_tls_no_verify_to_attacker():
    # Connect to attacker proxy on port 9443 (attacker presents its cert)
    r = requests.get("https://mitm_proxy:9443/", verify=False)
    print("Scenario 2 (TLS but client does not verify):", r.status_code, r.text.strip())

def scenario3_selfsigned_but_client_trusts_it_wrongly():
    # If server were started with self-signed cert, client can explicitly trust that cert file
    # Here we read cert from /certs/selfsigned/selfsigned.pem (mounted read-only)
    r = requests.get("https://tls_server:8443/", verify="/certs/selfsigned/selfsigned.pem")
    print("Scenario 3 (self-signed + client trusts that cert):", r.status_code, r.text.strip())

def scenario4_ca_signed_and_client_verifies():
    # Client trusts the CA that signed the server cert (ca/ca.pem). MITM using attacker.pem should fail.
    try:
        r = requests.get("https://tls_server:8443/", verify="/certs/ca/ca.pem", timeout=5)
        print("Scenario 4 (CA-signed + verify):", r.status_code, r.text.strip())
    except Exception as e:
        print("Scenario 4 (CA-signed + verify) failed:", e)

if __name__ == "__main__":
    scenario1_plain_http()
    scenario2_tls_no_verify_to_attacker()
    scenario3_selfsigned_but_client_trusts_it_wrongly()
    scenario4_ca_signed_and_client_verifies()
