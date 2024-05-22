import xml.etree.ElementTree as ET
from lxml import etree
import os
import logging
from datetime import datetime
import pytbai
from string import Template
from signxml import DigestAlgorithm
from signxml.xades import (
    XAdESSigner,
    XAdESVerifier,
    XAdESVerifyResult,
    XAdESSignaturePolicy,
    XAdESDataObjectFormat,
)

logger = logging.getLogger("pytbai")


def build_xml(tbai, invoice, pre_invoice=None):
    path = os.path.dirname(pytbai.__file__)
    structure_file = os.path.join(path, "templates/XML/tbai_structure.xml")
    with open(structure_file, "r") as file:
        template = file.read()
    temp = Template(template)

    expedition_date = datetime.strptime(invoice.expedition_date, "%Y-%m-%d").strftime(
        "%d-%m-%Y"
    )
    transaction_date = datetime.strptime(invoice.transaction_date, "%Y-%m-%d").strftime(
        "%d-%m-%Y"
    )

    xml = temp.substitute(
        version=tbai.version,
        entity_id=tbai.subject.entity_id,
        name=tbai.subject.name,
        multi_recipient=tbai.subject.multi_recipient,
        external_invoice=tbai.subject.external_invoice,
        serial_code=invoice.serial_code,
        num=invoice.num,
        description=invoice.description,
        simplified=invoice.simplified,
        substitution=invoice.substitution,
        vat_regime=invoice.vat_regime,
        expedition_date=expedition_date,
        expedition_time=invoice.expedition_time,
        transaction_date=transaction_date,
        license=tbai.software.license,
        dev_entity=tbai.software.dev_entity,
        soft_name=tbai.software.soft_name,
        soft_version=tbai.software.soft_version,
    )
    root = ET.fromstring(xml)
    lines = invoice.get_lines()
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
            line_base = line.get_line_base()
            discount_xml = ET.SubElement(line_xml, "Descuento")
            discount_xml.text = str(line.get_discount_qty(line_base))
        total_xml = ET.SubElement(line_xml, "ImporteTotal")
        total_xml.text = str(line.total)
    total_root = root.find(".//ImporteTotalFactura")
    total_root.text = str(invoice.get_total_amount())
    vat_type = root.find(".//NoExenta")
    breakdown = invoice.get_vat_breakdown()
    for vtype in breakdown:
        vtype_line = ET.SubElement(vat_type, "DetalleNoExenta")
        vbreakdown = ET.SubElement(vtype_line, "TipoNoExenta")
        vbreakdown.text = vtype["type"]
        vtbreak = ET.SubElement(vtype_line, "DesgloseIVA")
        for rate in vtype["rates"].items():
            rate_detail = ET.SubElement(vtbreak, "DetalleIVA")
            vat_base = ET.SubElement(rate_detail, "BaseImponible")
            vat_base.text = str(rate[1]["base"])
            vat_rate = ET.SubElement(rate_detail, "TipoImpositivo")
            vat_rate.text = str(float(rate[0]))
            vat_fee = ET.SubElement(rate_detail, "CuotaImpuesto")
            vat_fee.text = str(rate[1]["fee"])

    if pre_invoice:
        fp_root = root.find(".//HuellaTBAI")
        p_inv = ET.Element("EncadenamientoFacturaAnterior")
        fp_root.insert(0, p_inv)
        serial_code = ET.SubElement(p_inv, "SerieFacturaAnterior")
        serial_code.text = pre_invoice["serial_code"]
        num = ET.SubElement(p_inv, "NumFacturaAnterior")
        num.text = pre_invoice["num"]
        expedition_date = ET.SubElement(p_inv, "FechaExpedicionFacturaAnterior")
        expedition_date.text = pre_invoice["expedition_date"]
        signature_value = ET.SubElement(p_inv, "SignatureValueFirmaFacturaAnterior")
        signature_value.text = pre_invoice["signature_value"]

    return root


def validate_xml(xml):
    path = os.path.dirname(pytbai.__file__)
    xsd_file = os.path.join(path, "templates/XSD/ticketBaiV1-2-1.xsd")
    with open(xsd_file, "r") as file:
        xmlschema_doc = etree.parse(file)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        try:
            xmlschema.assert_(xml)
        except AssertionError as msg:
            logger.error(msg)
            return False
        return True


def sign_xml(xml, key, cert):
    signature_policy = XAdESSignaturePolicy(
        Identifier="https://www.gipuzkoa.eus/ticketbai/sinadura",
        Description="",
        DigestMethod=DigestAlgorithm.SHA256,
        DigestValue="vSe1CH7eAFVkGN0X2Y7Nl9XGUoBnziDA5BGUSsyt8mg=",
    )
    data_object_format = XAdESDataObjectFormat(
        Description="",
        MimeType="text/xml",
    )
    signer = XAdESSigner(
        signature_policy=signature_policy,
        claimed_roles=["signer"],
        data_object_format=data_object_format,
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
    )
    signed_doc = signer.sign(xml, key=key, cert=cert)
    return signed_doc
