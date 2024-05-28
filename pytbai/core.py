from datetime import datetime
import copy
import tempfile
import json
import requests
import logging
from decimal import Decimal
from lxml import etree
from json import JSONEncoder
from decimal import Decimal
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

logger = logging.getLogger("pytbai")


class Subject:
    def __init__(
        self,
        entity_id,
        name,
        territory=GIPUZKOA,
        multi_recipient=N,
        external_invoice=N,
        env="DEV",
    ):
        self.entity_id = entity_id
        self.name = name
        if not territory:
            self.authority_api = GIPUZKOA[env]["invoice"]
            self.qr_api = GIPUZKOA[env]["qr"]
        elif territory in AUTHORITY_APIS:
            self.authority_api = AUTHORITY_APIS[territory][env]["invoice"]
            self.qr_api = AUTHORITY_APIS[territory][env]["qr"]
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

    def get_dict(self):
        return copy.deepcopy(self.__dict__)


class InvoiceLine:
    def __init__(
        self,
        description,
        quantity=Decimal("0"),
        amount=Decimal("0"),
        discount=Decimal("0"),
        vat_rate=DEFAULT_VAT_RATE,
        vat_type=None,
        vat_included=False,
    ):
        self.description = description
        self.quantity = quantity
        self.discount = discount
        self.vat_rate = vat_rate
        self.vat_fee = Decimal("0")
        if not vat_type:
            self.vat_type = S1
        elif vat_type in L11:
            self.vat_type = vat_type
        else:
            raise ValueError(
                "Value not found in L11 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        if not vat_included:
            self.unit_amount = amount
            line_base = self.quantity * self.unit_amount
            self.vat_base = line_base - self.get_discount_qty(line_base)
            vat_fee = self.vat_base * (self.vat_rate / 100)
            self.vat_fee = vat_fee.quantize(Decimal("0.00"))
            self.total = self.vat_base + self.vat_fee
        else:
            self.total = amount
            line_base = (self.total - self.get_discount_qty(self.total)) / self.quantity
            self.unit_amount = (line_base / (1 + (self.vat_rate / 100))).quantize(
                Decimal("0.00")
            )
            self.vat_fee = line_base.quantize(Decimal("0.00")) - self.unit_amount
            vat_base = self.vat_fee / (self.vat_rate / 100)
            self.vat_base = vat_base.quantize(Decimal("0.00"))

    def get_line_base(self):
        return self.quantity * self.unit_amount

    def get_discount_qty(self, amount):
        discount_qty = Decimal("0")
        if self.discount:
            discount_qty = amount * (self.discount / 100)
        return discount_qty.quantize(Decimal("0.00"))

    def get_dict(self):
        return copy.deepcopy(self.__dict__)


class Invoice:
    def __init__(
        self,
        serial_code,
        num,
        description,
        simplified=None,
        substitution=None,
        vat_regime=None,
        expedition_date=None,
        expedition_time=None,
        transaction_date=None,
    ):

        self.serial_code = serial_code
        self.num = num
        self.description = description
        self.expedition_date = expedition_date or datetime.now().date().isoformat()
        self.expedition_time = expedition_time or datetime.now().time().strftime(
            "%H:%M:%S"
        )
        self.transaction_date = transaction_date or datetime.now().date().isoformat()

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
        total = Decimal(sum([line.total for line in lines]))
        return total.quantize(Decimal("0.00"))

    def get_vat_breakdown(self):
        breakdown = []
        for vat_type in L11:
            lines = [line for line in self.get_lines() if line.vat_type == vat_type]
            if lines:
                line_types = {"type": vat_type, "rates": {}}
                for line in lines:
                    if str(line.vat_rate) in line_types["rates"]:
                        line_types["rates"][str(line.vat_rate)] = {
                            "base": line_types["rates"][str(line.vat_rate)]["base"]
                            + line.vat_base,
                            "fee": line_types["rates"][str(line.vat_rate)]["fee"]
                            + line.vat_fee,
                        }
                    else:
                        line_types["rates"].update(
                            {
                                str(line.vat_rate): {
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
        quantity=Decimal("0"),
        amount=Decimal("0"),
        discount=Decimal("0"),
        vat_rate=DEFAULT_VAT_RATE,
        vat_type=S1,
        vat_included=False,
    ):
        line = InvoiceLine(
            description,
            quantity,
            unit_import,
            discount,
            vat_rate,
            vat_type,
        )
        self.lines.append(line)

    def delete_lines(self, lines):
        curr_lines = self.lines
        for line in lines:
            curr_lines.remove(line)
        self.lines = curr_lines

    def get_dict(self):
        invoice_json = copy.deepcopy(self.__dict__)
        lines_json = []
        for line in invoice_json["lines"]:
            lines_json.append(line.get_dict())
        invoice_json["lines"] = lines_json
        invoice_json["total_amount"] = self.get_total_amount()
        invoice_json["vat_breakdown"] = self.get_vat_breakdown()
        return invoice_json


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

    def get_dict(self):
        return copy.deepcopy(self.__dict__)


class TBaiEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


class TBai:
    def __init__(self, config, version=TICKETBAI_ACTUAL_VERSION, env="DEV"):
        self.version = version
        self.env = env
        config["subject"].update({"env": env})
        self.subject = Subject(**config["subject"])
        self.software = Software(**config["software"])

    def create_invoice(
        self,
        serial_code,
        num,
        description,
        simplified=None,
        expedition_date=None,
        expedition_time=None,
        transaction_date=None,
    ):
        invoice = Invoice(
            serial_code,
            num,
            description,
            simplified=simplified,
            expedition_date=expedition_date or datetime.now().date().isoformat(),
            expedition_time=expedition_time
            or datetime.now().time().strftime("%H:%M:%S"),
            transaction_date=transaction_date or datetime.now().date().isoformat(),
        )
        return invoice

    def sign(self, invoice, p12_path, password, pre_invoice=None):
        xml = build_xml(self, invoice, pre_invoice)
        key, cert = get_keycert_from_p12(p12_path, password.encode("utf-8"))
        signed_xml = sign_xml(xml, key, cert)
        if not validate_xml(signed_xml):
            return None
        return etree.tostring(signed_xml).decode("utf-8")

    def send(self, signed_xml, p12_path, password):
        result_json = {
            "status": 500,
            "TBAI_ID": None,
            "CSV": None,
            "ErrorXML": None,
        }

        key, cert = get_keycert_from_p12(p12_path, password.encode("utf-8"))
        key_file = tempfile.NamedTemporaryFile()
        key_file.write(key)
        key_file.flush()
        cert_file = tempfile.NamedTemporaryFile()
        cert_file.write(cert)
        cert_file.flush()

        headers = {"Content-Type": "application/xml"}

        response = requests.post(
            url=self.subject.authority_api,
            headers=headers,
            data=signed_xml,
            cert=(cert_file.name, key_file.name),
        )

        key_file.close()
        cert_file.close()

        if response.ok:
            result_json["status"] = 200
            response_xml = etree.fromstring(response.content)
            state = response_xml.find(".//Estado").text
            if state == "01":
                logger.error("XML not accepted")
                result_json["ErrorXML"] = response.content
                return result_json
            result_json["TBAI_ID"] = response_xml.find(".//IdentificadorTBAI").text
            result_json["CSV"] = response_xml.find(".//CSV").text
            return result_json
        logger.error("API connection error")
        return result_json

    def get_json(self, invoice=None):
        tbai_json = {"version": self.version, "env": self.env}
        if self.subject:
            tbai_json["subject"] = self.subject.get_dict()
        if invoice:
            tbai_json["invoice"] = invoice.get_dict()
        if self.software:
            tbai_json["software"] = self.software.get_dict()
        return json.dumps(tbai_json, cls=TBaiEncoder)
