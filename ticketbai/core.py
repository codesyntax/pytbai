from datetime import datetime

TICKETBAI_ACTUAL_VERSION = "1.2"


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
        self.multi_recipient = multi_recipient
        self.external_invoice = external_invoice


class InvoiceLine:
    def __init__(
        self,
        description,
        quantity=0,
        unit_amount=0,
        discount=0,
    ):
        self.decription = description
        self.quantity = quantity
        self.unit_amount = unit_amount
        self.discount = discount
        self.set_total()

    def set_total(self):
        line_base = round(self.quantity * self.unit_amount, 2)
        if self.discount:
            self.total = line_base * (self.discount / 100)
        else:
            self.total = line_base


class Invoice:
    def __init__(
        self,
        serial_code,
        num,
        description,
        simplified=None,
        substitution=None,
        vat_regime="01",
    ):
        now = datetime.now()
        self.serial_code = serial_code
        self.num = num
        self.expedition_date = now.date()
        self.expedition_time = now.time()
        self.simplified = simplified
        self.substitution = substitution
        self.transaction_date = now.date()
        self.description = description
        self.vat_regime = vat_regime
        self.lines = []

    def get_lines(self):
        return self.lines

    def get_total_amount(self):
        lines = self.get_lines()
        return sum([line.total for line in lines])

    def create_line(self, description, quantity=0, unit_import=0, discount=0):
        line = InvoiceLine(description, quantity, unit_import, discount)
        self.lines.append(line)

    def delete_lines(self, lines):
        for line in lines:
            self.lines.remove(line)


class TBai:
    def __init__(self, subject, version=TICKETBAI_ACTUAL_VERSION):
        self.version = version
        self.subject = subject
        self.invoice = None
        self.tbai_print = None
        self.signature = None

    def create_invoice(self, serial_code, num, description, simplified=None):
        self.invoice = Invoice(
            serial_code,
            num,
            description,
            simplified,
        )
        return self.invoice
