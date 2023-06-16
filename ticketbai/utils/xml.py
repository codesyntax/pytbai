import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import os
import ticketbai
from string import Template


def build_xml(tbai):
    path = os.path.dirname(ticketbai.__file__)
    structure_file = os.path.join(path, "templates/XML/tbai_structure.xml")
    with open(structure_file, "r") as file:
        template = file.read()
    temp = Template(template)
    xml = temp.substitute(
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
    root = ET.fromstring(xml)
    lines = tbai.invoice.get_lines()
    lines_root = root.find(".//DetallesFactura")
    for line in lines:
        line_xml = ET.SubElement(lines_root, "IDDetalleFactura")
        desc_xml = ET.SubElement(line_xml, "DescripcionDetalle")
        desc_xml.text = line.description
        quantity_xml = ET.SubElement(line_xml, "Cantidad")
        quantity_xml.text = str(line.quantity)
        unit_amount_xml = ET.SubElement(line_xml, "ImporteUnitario")
        unit_amount_xml.text = str(line.unit_amount)
        if line.discount:
            discount_xml = ET.SubElement(line_xml, "Descuento")
            discount_xml.text = str(line.discount)
        total_xml = ET.SubElement(line_xml, "ImporteTotal")
        total_xml.text = str(line.total)
    total_root = root.find(".//ImporteTotalFactura")
    total_root.text = str(tbai.invoice.get_total_amount())

    data = ET.tostring(root)
    return "\n".join(
        [
            line
            for line in parseString(data)
            .toprettyxml(indent=" " * 2)
            .split("\n")
            if line.strip()
        ]
    )
