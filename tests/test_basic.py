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
        self.assertIsNotNone(tbai.invoice)
        self.assertEqual(tbai.invoice.serial_code, "TB-2021-S")
        self.assertEqual(tbai.invoice.num, 1)
        self.assertEqual(tbai.invoice.description, "Primera factura")
        self.assertEqual(tbai.invoice.simplified, "N")
        self.assertEqual(tbai.invoice.substitution, "N")
        self.assertEqual(tbai.invoice.vat_regime, "01")

    def test_build_xml(self):
        tbai = TBai(CONFIG)
        tbai.create_invoice("TB-2021-S", 1, "Primera factura")
        xml = build_xml(tbai)
        self.assertIsNotNone(xml)


if __name__ == "__main__":
    unittest.main()
