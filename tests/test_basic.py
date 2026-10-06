# -*- coding: utf-8 -*-

import pytbai
from pytbai import TBai
from pytbai.utils.xml import build_xml, validate_xml, sign_xml
import os
import json
import unittest
from datetime import datetime
from decimal import Decimal
from pytbai.utils.crypto import get_keycert_from_p12
from tests.data.tbai_json import (
    TBAI_JSON,
    TBAI_INVOICE_JSON,
    TBAI_INVOICE_LINES_JSON,
)

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


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_tbai_subject_constructor(self):
        tbai = TBai(CONFIG)
        self.assertIsNotNone(tbai.subject)
        self.assertEqual(tbai.subject.entity_id, "99999974E")
        self.assertEqual(tbai.subject.name, "REPRESENTANTESPJ FICTICIO")
        self.assertEqual(tbai.subject.address, "Some address")

    def test_tbai_software_constructor(self):
        tbai = TBai(CONFIG)
        self.assertIsNotNone(tbai.software)
        self.assertEqual(tbai.software.license, "TBAIGIPRE00000000501")
        self.assertEqual(tbai.software.dev_entity, "P2000000F")
        self.assertEqual(tbai.software.soft_name, "FAKTURABAI")
        self.assertEqual(tbai.software.soft_version, "1.0")

    def test_create_invoice(self):
        tbai = TBai(CONFIG)
        invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.serial_code, "TB-2021-S")
        self.assertEqual(invoice.num, 1)
        self.assertEqual(invoice.description, "Primera factura")
        self.assertEqual(invoice.simplified, "N")
        self.assertEqual(invoice.substitution, "N")
        self.assertEqual(invoice.vat_regime, "01")

    def test_create_invoice_line(self):
        tbai = TBai(CONFIG)
        invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        invoice.create_line(
            "Primer producto", Decimal("1"), Decimal("200"), Decimal("20")
        )
        invoice.create_line("Segundo producto", Decimal("2"), Decimal("350"))
        self.assertTrue(invoice.get_lines())
        lines = invoice.get_lines()
        self.assertEqual(lines[0].vat_base, Decimal("160"))
        self.assertEqual(lines[0].total, Decimal("193.6"))
        self.assertEqual(lines[1].vat_base, Decimal("700"))
        self.assertEqual(lines[1].total, Decimal("847"))

    def test_build_xml(self):
        tbai = TBai(CONFIG)
        invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        invoice.create_line(
            "Primer producto", Decimal("1"), Decimal("200"), Decimal("20")
        )
        invoice.create_line("Segundo producto", Decimal("2"), Decimal("350"))
        xml = build_xml(tbai, invoice)
        self.assertIsNotNone(xml)

    def test_sign_validate_xml(self):
        path = os.path.dirname(pytbai.__file__)
        cert_path = os.path.join(path, "../tests/certs/cert_for_tests.p12")
        tbai = TBai(CONFIG)
        invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        invoice.create_line(
            "Primer producto", Decimal("1"), Decimal("200"), Decimal("20")
        )
        invoice.create_line("Segundo producto", Decimal("2"), Decimal("350"))
        xml = build_xml(tbai, invoice)
        key, cert = get_keycert_from_p12(cert_path, b"testpassword")
        signed_xml = sign_xml(xml, key, cert)
        result = validate_xml(signed_xml)
        self.assertEqual(result, True)

    def test_get_json(self):
        tbai = TBai(CONFIG)
        date = datetime(2023, 7, 5, 12, 58, 17, 710211)
        invoice = tbai.create_invoice(
            "TB-2021-S",
            1,
            "Primera factura",
            expedition_date=date.date().isoformat(),
            expedition_time=date.time().strftime("%H:%M:%S"),
            transaction_date=date.date().isoformat(),
        )
        tbai_json = tbai.get_json()
        self.assertDictEqual(json.loads(tbai_json), TBAI_JSON)
        tbai_json = tbai.get_json(invoice)
        self.assertDictEqual(json.loads(tbai_json), TBAI_INVOICE_JSON)
        invoice.create_line(
            "Primer producto", Decimal("1"), Decimal("200"), Decimal("20")
        )
        invoice.create_line("Segundo producto", Decimal("2"), Decimal("350"))
        tbai_json = tbai.get_json(invoice)
        self.assertDictEqual(json.loads(tbai_json), TBAI_INVOICE_LINES_JSON)

    def test_get_keycert_from_p12_returns_pem(self):
        path = os.path.dirname(pytbai.__file__)
        cert_path = os.path.join(path, "../tests/certs/cert_for_tests.p12")
        key, cert = get_keycert_from_p12(cert_path, b"testpassword")
        self.assertIn(b"-----BEGIN", key)
        self.assertIn(b"-----BEGIN CERTIFICATE-----", cert)

    def test_get_keycert_from_p12_accepts_a_string_password(self):
        # django-ticketbai passes Config.password, a str, not bytes.
        path = os.path.dirname(pytbai.__file__)
        cert_path = os.path.join(path, "../tests/certs/cert_for_tests.p12")
        key, cert = get_keycert_from_p12(cert_path, "testpassword")
        self.assertEqual(key, get_keycert_from_p12(cert_path, b"testpassword")[0])
        self.assertIn(b"-----BEGIN CERTIFICATE-----", cert)

    def test_validate_xml_rejects_an_invalid_document(self):
        from lxml import etree

        self.assertFalse(validate_xml(etree.fromstring("<invalid/>")))

    def test_prod_endpoints_match_the_published_1_6_3(self):
        from pytbai.definitions import AUTHORITY_APIS, GIPUZKOA

        prod = AUTHORITY_APIS[GIPUZKOA]["PROD"]
        self.assertEqual(
            prod["invoice"], "https://tbai-z.egoitza.gipuzkoa.eus/sarrerak/alta"
        )
        self.assertEqual(prod["qr"], "https://tbai.egoitza.gipuzkoa.eus/qr/")


if __name__ == "__main__":
    unittest.main()
