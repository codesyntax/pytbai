from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    pkcs12,
)


def get_keycert_from_p12(path, password):
    """Return the PEM private key and certificate stored in a PKCS#12 file.

    Uses ``cryptography`` directly: the ``OpenSSL.crypto`` PKCS#12 helpers were
    deprecated in pyOpenSSL 23 and removed in pyOpenSSL 24.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    with open(path, "rb") as file:
        key, cert, _ = pkcs12.load_key_and_certificates(file.read(), password)
    key_pem = key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    cert_pem = cert.public_bytes(Encoding.PEM)
    return key_pem, cert_pem
