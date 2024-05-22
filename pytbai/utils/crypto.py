from OpenSSL import crypto


def get_keycert_from_p12(path, password):
    with open(path, "rb") as file:
        p12 = crypto.load_pkcs12(file.read(), password)
        # PEM formatted private key
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
        # PEM formatted certificate
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
        return key, cert
