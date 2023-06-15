TICKETBAI_ACTUAL_VERSION = "1.2"


class Subject:
    entity_id = None
    name = None
    multi_recipient = None
    external_invoice = None

    def __init__(self):
        self.multi_recipient = "N"
        self.external_invoice = "N"


class TBai:
    version = None
    subject = Subject()

    def __init__(self):
        self.version = TICKETBAI_ACTUAL_VERSION
