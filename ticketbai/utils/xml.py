import xml.etree.ElementTree as ET
import importlib.resources as pkg_resources
from ticketbai import templates
from string import Template


def build_xml(tbai):
    inp_file = pkg_resources.files(templates) / "XML/tbai_structure.xml"
    with inp_file.open("rt") as f:
        template = f.read()
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
    )
    return xml
