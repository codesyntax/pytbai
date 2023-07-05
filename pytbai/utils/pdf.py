import os
import pytbai
import qrcode
import base64
from io import BytesIO
from string import Template
from requests.models import PreparedRequest
from weasyprint import HTML, CSS

TEMPLATES_PATH = os.path.join(os.path.dirname(pytbai.__file__), "templates")


def create_qr_base64(invoice, tbai_id, subject):
    request = PreparedRequest()
    params = {
        "id": tbai_id,
        "s": invoice.serial_code,
        "nf": invoice.num,
        "i": invoice.get_total_amount(),
        "cr": tbai_id.split("-")[-1],
    }
    request.prepare_url(subject.qr_api, params)

    qr_code = qrcode.QRCode(box_size=3)
    qr_code.add_data("%s" % request.url)
    img = qr_code.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img.close()
    return base64.b64encode(buffered.getvalue())


def get_css_string():
    css_file = os.path.join(TEMPLATES_PATH, "PDF/ticketbai.css")
    with open(css_file, "r") as file:
        css_string = file.read()
        return css_string


def get_html_string(invoice, tbai_id, subject):
    html_file = os.path.join(TEMPLATES_PATH, "PDF/ticketbai.html")
    qr_base64 = create_qr_base64(invoice, tbai_id, subject)
    subject_info = "%s</br>IFZ: %s</br>" % (subject.name, subject.entity_id)
    date = invoice.expedition_date.strftime("%Y-%m-%d")
    hour = invoice.expedition_time.strftime("%H:%M:%S")
    serial_code = invoice.serial_code
    num = invoice.num
    invoice_total = str(invoice.get_total_amount()).replace(".", ",")

    with open(html_file, "r") as file:
        template = file.read()
    temp = Template(template)
    return temp.substitute(
        subject_info=subject_info,
        date=date,
        hour=hour,
        serial_code=serial_code,
        num=num,
        invoice_total=invoice_total,
        tbai_id=tbai_id,
        qrcode=qr_base64.decode("utf-8"),
    )


def build_pdf(invoice, tbai_id, subject):
    css = CSS(string=get_css_string())
    html = HTML(string=get_html_string(invoice, tbai_id, subject))
    return html.write_pdf(stylesheets=[css])
