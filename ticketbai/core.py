from datetime import datetime
import json
from ticketbai.definitions import (
    TICKETBAI_ACTUAL_VERSION,
    DOCUMENTATION_URL,
    L3,
    L4,
    L5,
    L6,
    L9,
    L11,
)
from ticketbai.utils.xml import build_xml, sign_xml, validate_xml
from ticketbai.utils.crypto import get_keycert_from_p12


class Subject:
    def __init__(
        self,
        entity_id,
        name,
        multi_recipient="N",
        external_invoice="N",
    ):
        self.entity_id = entity_id
        self.name = name
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
        vat_rate=21,
        vat_type=None,
    ):
        self.description = description
        self.quantity = quantity
        self.unit_amount = unit_amount
        self.discount = discount
        self.vat_rate = vat_rate
        if not vat_type:
            self.vat_type = L11[0]  # 'S1'
        elif vat_type in L11:
            self.vat_type = vat_type
        else:
            raise ValueError(
                "Value not found in L11 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        self.set_base()
        self.set_total()

    def set_base(self):
        line_base = round(self.quantity * self.unit_amount, 2)
        if self.discount:
            self.vat_base = round(
                line_base - (line_base * (self.discount / 100)), 2
            )
        else:
            self.vat_base = line_base

    def set_total(self):
        self.total = round(
            self.vat_base + (self.vat_base * (self.vat_rate / 100)), 2
        )


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
            self.simplified = L5[1]  # 'N'
        elif simplified in L5:
            self.simplified = simplified
        else:
            raise ValueError(
                "Value not found in L5 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        if not substitution:
            self.substitution = L6[1]  # 'N'
        elif substitution in L6:
            self.substitution = substitution
        else:
            raise ValueError(
                "Value not found in L6 options, see documentation: %s"
                % DOCUMENTATION_URL
            )

        if not vat_regime:
            self.vat_regime = L9[0]  # 'N'
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
            line_types = {"type": vat_type, "rates": {}}
            lines = [
                line for line in self.get_lines() if line.vat_type == vat_type
            ]
            for line in lines:
                if line.vat_rate in line_types["rates"]:
                    line_types["rates"][line.vat_rate] = {
                        "base": line_types["rates"][line.vat_rate]["base"]
                        + line.vat_base,
                        "total": line_types["rates"][line.vat_rate]["total"]
                        + line.total,
                    }
                else:
                    line_types["rates"].update(
                        {
                            line.vat_rate: {
                                "base": line.vat_base,
                                "total": line.total,
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
        vat_rate=21,
        vat_type=None,
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
        self.invoice = None
        self.signature = None

    def create_invoice(self, serial_code, num, description, simplified=None):
        self.invoice = Invoice(
            serial_code,
            num,
            description,
            simplified,
        )
        return self.invoice

    def sign_and_send(self, p12_path, password):
        xml = build_xml(self)
        key, cert = get_keycert_from_p12(p12_path, password.encode("utf-8"))
        signed_xml = sign_xml(xml, key, cert)
        validate_xml(signed_xml)
        print("Invoice XML created, validated and sent!")
