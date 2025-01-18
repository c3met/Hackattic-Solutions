import requests
import json 
import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
import country_converter as coco

get_challenge_url = "https://hackattic.com/challenges/tales_of_ssl/problem?access_token="
submit_solution_url = "https://hackattic.com/challenges/tales_of_ssl/solve?access_token="


chall = requests.get(get_challenge_url).text
load = json.loads(chall)

decode_key = base64.b64decode(load['private_key'])
required_data = load['required_data']

print("Data: " + str(required_data))

country = coco.convert(names=[required_data["country"]], to='ISO2')
key = load_der_private_key(decode_key, password=None)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
    x509.NameAttribute(NameOID.COMMON_NAME, required_data["domain"]), 
])


certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(int(required_data["serial_number"], 16))
    .not_valid_before(datetime.now(timezone.utc))
    .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName(required_data["domain"])]),
        critical=False,
    )
    .sign(private_key=key, algorithm=hashes.SHA256())
)

cert_der = certificate.public_bytes(encoding=serialization.Encoding.DER)
cert_base64 = base64.b64encode(cert_der).decode('utf-8')

payload = {
    "certificate": cert_base64
}

result = requests.post(submit_solution_url, json=payload)
print(result.text)