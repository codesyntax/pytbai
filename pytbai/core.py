from datetime import datetime
import tempfile
import json
import requests
import logging
from lxml import etree
from pytbai.definitions import (
    TICKETBAI_ACTUAL_VERSION,
    DOCUMENTATION_URL,
    AUTHORITY_APIS,
    GIPUZKOA,
    DEFAULT_VAT_RATE,
    DEFAULT_VAT,
    N,
    L3,
    L4,
    L5,
    L6,
    L9,
    S1,
    L11,
)
from pytbai.utils.xml import build_xml, sign_xml, validate_xml
from pytbai.utils.crypto import get_keycert_from_p12
from pytbai.utils.pdf import build_pdf

logger = logging.getLogger("pytbai")


class Subject:
    def __init__(
        self,
        entity_id,
        name,
        territory=GIPUZKOA,
        multi_recipient=N,
        external_invoice=N,
    ):
        self.entity_id = entity_id
        self.name = name
        if not territory:
            self.authority_api = GIPUZKOA["invoice"]
            self.qr_api = GIPUZKOA["qr"]
        elif territory in AUTHORITY_APIS:
            self.authority_api = AUTHORITY_APIS[territory]["invoice"]
            self.qr_api = AUTHORITY_APIS[territory]["qr"]
        else:
            raise ValueError(
                "Not a valid territory. Options are: Araba, Bizkaia, Gipuzkoa."
            )
        if multi_recipient in L3:
            self.multi_recipient = multi_recipient
        else:
            raise ValueError(
                "Value not found in L3 options, see documentation: %s"
                % DOCUMENTATION_URL
            )
        if external_invoice in L4:
            self.external_invoice = external_invoice
        else:
            raise ValueError(
                "Value not found in L4 options, see documentation: %s"
                % DOCUMENTATION_URL
            )


class InvoiceLine:
    def __init__(
        self,
        description,
        quantity=0,
        unit_amount=0,
        discount=0,
        vat_rate=DEFAULT_VAT_RATE,
        vat_type=None,
    ):
        self.description = description
        self.quantity = quantity
        self.unit_amount = unit_amount
        self.discount = discount
        self.vat_rate = vat_rate
        self.vat_fee = None
        if not vat_type:
            self.vat_type = S1
        elif vat_type in L11:
            self.vat_type = vat_type
        else:
            raise ValueError(
                "Value not found in L11 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        self.set_base()
        self.set_vat_fee()
        self.set_total()

    def get_line_base(self):
        return round(self.quantity * self.unit_amount, 2)

    def get_discount_qty(self, line_base):
        return line_base * (self.discount / 100)

    def set_base(self):
        line_base = self.get_line_base()
        if self.discount:
            self.vat_base = round(
                line_base - self.get_discount_qty(line_base), 2
            )
        else:
            self.vat_base = line_base

    def set_vat_fee(self):
        self.vat_fee = round(self.vat_base * (self.vat_rate / 100), 2)

    def set_total(self):
        self.total = round(self.vat_base + self.vat_fee, 2)


class Invoice:
    def __init__(
        self,
        serial_code,
        num,
        description,
        simplified=None,
        substitution=None,
        vat_regime=None,
    ):
        now = datetime.now()
        self.serial_code = serial_code
        self.num = num
        self.description = description
        self.expedition_date = now.date()
        self.expedition_time = now.time()
        self.transaction_date = now.date()

        if not simplified:
            self.simplified = N
        elif simplified in L5:
            self.simplified = simplified
        else:
            raise ValueError(
                "Value not found in L5 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        if not substitution:
            self.substitution = N
        elif substitution in L6:
            self.substitution = substitution
        else:
            raise ValueError(
                "Value not found in L6 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        if not vat_regime:
            self.vat_regime = DEFAULT_VAT
        elif vat_regime in L9:
            self.vat_regime = vat_regime
        else:
            raise ValueError(
                "Value not found in L9 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        self.lines = []

    def get_lines(self):
        return self.lines

    def get_total_amount(self):
        lines = self.get_lines()
        return round(sum([line.total for line in lines]), 2)

    def get_vat_breakdown(self):
        breakdown = []
        for vat_type in L11:
            lines = [
                line for line in self.get_lines() if line.vat_type == vat_type
            ]
            if lines:
                line_types = {"type": vat_type, "rates": {}}
                for line in lines:
                    if line.vat_rate in line_types["rates"]:
                        line_types["rates"][line.vat_rate] = {
                            "base": line_types["rates"][line.vat_rate]["base"]
                            + line.vat_base,
                            "fee": line_types["rates"][line.vat_rate]["fee"]
                            + line.vat_fee,
                        }
                    else:
                        line_types["rates"].update(
                            {
                                line.vat_rate: {
                                    "base": line.vat_base,
                                    "fee": line.vat_fee,
                                }
                            }
                        )
                breakdown.append(line_types)
        return breakdown

    def create_line(
        self,
        description,
        quantity=0,
        unit_import=0,
        discount=0,
        vat_rate=DEFAULT_VAT_RATE,
        vat_type=S1,
    ):
        line = InvoiceLine(
            description, quantity, unit_import, discount, vat_rate, vat_type
        )
        self.lines.append(line)

    def delete_lines(self, lines):
        curr_lines = self.lines
        for line in lines:
            curr_lines.remove(line)
        self.lines = curr_lines


class Software:
    def __init__(
        self,
        license,
        dev_entity,
        soft_name,
        soft_version,
    ):
        self.license = license
        self.dev_entity = dev_entity
        self.soft_name = soft_name
        self.soft_version = soft_version


class TBai:
    def __init__(self, config, version=TICKETBAI_ACTUAL_VERSION):
        self.version = version
        self.subject = Subject(**config["subject"])
        self.software = Software(**config["software"])

    def create_invoice(self, serial_code, num, description, simplified=None):
        invoice = Invoice(
            serial_code,
            num,
            description,
            simplified,
        )
        return invoice

    def sign_and_send(self, invoice, p12_path, password):
        xml = build_xml(self, invoice)
        key, cert = get_keycert_from_p12(p12_path, password.encode("utf-8"))
        signed_xml = sign_xml(xml, key, cert)
        if not validate_xml(signed_xml):
            return (None, None)

        key_file = tempfile.NamedTemporaryFile()
        key_file.write(key)
        cert_file = tempfile.NamedTemporaryFile()
        cert_file.write(cert)

        headers = {"Content-Type": "application/xml"}

        # TODO: Error handling for timeout
        response = requests.post(
            url=self.subject.authority_api,
            headers=headers,
            data=etree.tostring(signed_xml),
            cert=(cert_file.name, key_file.name),
            timeout=5,
        )
        key_file.close()
        cert_file.close()

        if response.ok:
            response_xml = etree.fromstring(response.content)
            state = response_xml.find(".//Estado").text
            if state == "01":
                logger.error("XML not accepted")
                return (None, response_xml)
            tbai_ID = response_xml.find(".//IdentificadorTBAI").text
            return (tbai_ID, signed_xml)
        logger.error("API connection error")
        return (None, None)

    def create_tbai_pdf(self, invoice, tbai_id):
        return build_pdf(invoice, tbai_id, self.subject)
