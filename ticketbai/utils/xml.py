import xml.etree.ElementTree as ET
import os
import ticketbai
from string import Template


def build_xml(tbai):
    path = os.path.dirname(ticketbai.__file__)
    structure_file = os.path.join(path, "templates/XML/tbai_structure.xml")
    with open(structure_file, "r") as file:
        template = file.read()
    t = Template(template)
    xml = t.substitute(
        version=tbai.version,
        entity_id=tbai.subject.entity_id,
        name=tbai.subject.name,
        multi_recipient=tbai.subject.multi_recipient,
        external_invoice=tbai.subject.external_invoice,
        serial_code=tbai.invoice.serial_code,
        num=tbai.invoice.num,
        description=tbai.invoice.description,
        simplified=tbai.invoice.simplified,
        substitution=tbai.invoice.substitution,
        vat_regime=tbai.invoice.vat_regime,
        expedition_date=tbai.invoice.expedition_date.strftime("%Y-%m-%d"),
        expedition_time=tbai.invoice.expedition_time.strftime("%H:%M:%S"),
        transaction_date=tbai.invoice.transaction_date.strftime("%Y-%m-%d"),
        license=tbai.software.license,
        dev_entity=tbai.software.dev_entity,
        soft_name=tbai.software.soft_name,
        soft_version=tbai.software.soft_version,
    )
    return xml
