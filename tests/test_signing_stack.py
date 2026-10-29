import os
from decimal import Decimal

import pytbai
from lxml import etree
from signxml.xades import XAdESVerifier

from pytbai import TBai
from pytbai.utils.crypto import get_keycert_from_p12
from pytbai.utils.xml import build_xml, sign_xml, validate_xml

CONFIG = {
    "subject": {
        "entity_id": "99999974E",
        "name": "REPRESENTANTESPJ FICTICIO",
        "address": "Some address",
    },
    "software": {
        "license": "TBAIGIPRE00000000501",
        "dev_entity": "P2000000F",
        "soft_name": "FAKTURABAI",
        "soft_version": "1.0",
    },
}


def signed_invoice():
    tbai = TBai(CONFIG)
    invoice = tbai.create_invoice("TB-2026-S", 1, "Test invoice")
    invoice.create_line("Product", Decimal("1"), Decimal("200"), Decimal("20"))
    xml = build_xml(tbai, invoice)
    cert_path = os.path.join(
        os.path.dirname(pytbai.__file__), "../tests/certs/cert_for_tests.p12"
    )
    key, cert = get_keycert_from_p12(cert_path, b"testpassword")
    return sign_xml(xml, key, cert), cert


def test_signed_xml_uses_the_ticketbai_signature_profile():
    signed, _ = signed_invoice()

    algorithms = {}
    for element in signed.iter():
        tag = etree.QName(element).localname
        if tag in {"SignatureMethod", "DigestMethod", "CanonicalizationMethod"}:
            algorithms.setdefault(tag, []).append(element.get("Algorithm"))

    assert algorithms["SignatureMethod"] == [
        "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
    ]
    assert set(algorithms["DigestMethod"]) == {
        "http://www.w3.org/2001/04/xmlenc#sha256"
    }
    assert algorithms["CanonicalizationMethod"] == [
        "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    ]

    tags = {etree.QName(element).localname for element in signed.iter()}
    assert {
        "SigningCertificateV2",
        "SignaturePolicyIdentifier",
        "SignerRole",
        "DataObjectFormat",
    } <= tags


def test_signed_xml_validates_against_the_bundled_schema():
    signed, _ = signed_invoice()

    assert validate_xml(signed) is True


def test_signature_verifies_with_the_test_certificate():
    signed, cert = signed_invoice()

    result = XAdESVerifier().verify(signed, require_x509=True, x509_cert=cert)

    assert result


def test_xmldsig_schema_is_packaged():
    schema_path = os.path.join(
        os.path.dirname(pytbai.__file__),
        "templates/XSD/xmldsig-core-schema.xsd",
    )

    assert os.path.exists(schema_path)
