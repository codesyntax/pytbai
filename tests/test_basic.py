# -*- coding: utf-8 -*-

from ticketbai import TBai
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


if __name__ == "__main__":
    unittest.main()
