# -*- coding: utf-8 -*-

from ticketbai import TBai
from ticketbai.utils.xml import build_xml
import unittest

CONFIG = {
    "subject": {"entity_id": "99999974E", "name": "REPRESENTANTESPJ FICTICIO"},
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
        invoice.create_line("Primer producto", 1, 200, 20)
        invoice.create_line("Segundo producto", 2, 350)
        self.assertTrue(invoice.get_lines())
        lines = invoice.get_lines()
        self.assertEqual(lines[0].vat_base, 160)
        self.assertEqual(lines[0].total, 193.6)
        self.assertEqual(lines[1].vat_base, 700)
        self.assertEqual(lines[1].total, 847)

    def test_build_xml(self):
        tbai = TBai(CONFIG)
        invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        invoice.create_line("Primer producto", 1, 200, 20)
        invoice.create_line("Segundo producto", 2, 350)
        xml = build_xml(tbai, invoice)
        self.assertIsNotNone(xml)


if __name__ == "__main__":
    unittest.main()
