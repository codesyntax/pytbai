import os
import ticketbai
import qrcode
from string import Template
from weasyprint import HTML, CSS

TEMPLATES_PATH = os.path.join(os.path.dirname(ticketbai.__file__), "templates")


def get_css_string():
    css_file = os.path.join(TEMPLATES_PATH, "PDF/ticketbai.css")
    with open(css_file, "r") as file:
        css_string = file.read()
        return css_string


def get_html_string(invoice, tbai_id):
    html_file = os.path.join(TEMPLATES_PATH, "PDF/ticketbai.html")
    with open(html_file, "r") as file:
        template = file.read()
    temp = Template(template)
    return temp.substitute(tbai_id=tbai_id)


def build_pdf(pdf_path, invoice, tbai_id):
    css = CSS(string=get_css_string())
    html = HTML(string=get_html_string(invoice, tbai_id))
    return html.write_pdf(stylesheets=css)
