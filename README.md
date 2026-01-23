![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytbai)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/codesyntax/pytbai/python-package.yml)
![PyPI - Version](https://img.shields.io/pypi/v/pytbai)

# pytbai

pytbai allows to create, manage and send TicketBai invoices to the Basque tax authorities.

## Usage

You need to configure your bussiness and software info in a JSON file:

```json
{
  "subject": {
    "entity_id": "99999974E",
    "name": "BUSSINESS NAME"
  },
  "software": {
    "license": "TBAIGIPRE00000000501",
    "dev_entity": "P2000000F",
    "soft_name": "TBAI",
    "soft_version": "1.0"
  }
}
```

Then create a invoice:

```python
from pytbai import TBai
from decimal import Decimal

tbai = TBai(json)
invoice = tbai.create_invoice("TB-2021-S", 1, "First invoice", "S")

invoice.create_line("First product", Decimal("1"), Decimal("200"), Decimal("20"))
invoice.create_line("Second product", Decimal("2"), Decimal("350"))
```

The `json` parameter is a previous JSON file you've created.

Finally sign and send the invoice:

```python
result = tbai.sign_and_send("/path_to_p12_certificate", "password")
```

You can also get the full structure of TBai invoice:

```python
json_structure = tbai.get_json(invoice)
```

## Invoice Chaining (Encadenamiento)

TicketBAI requires each invoice to reference the `SignatureValue` of the previous invoice in the same series, creating a blockchain-style chain. This prevents invoice manipulation and ensures regulatory compliance.

### Example: Chaining Invoices

```python
from pytbai import TBai
from decimal import Decimal

config = {
    "subject": {
        "entity_id": "B20456794",
        "name": "YOUR COMPANY S.L."
    },
    "software": {
        "license": "TBAIPRUEBA",
        "dev_entity": "A48119820",
        "soft_name": "TicketBAI Software",
        "soft_version": "1.0.0"
    }
}

tbai = TBai(config)

# First invoice (no previous invoice)
invoice1 = tbai.create_invoice("A", 1, "First invoice", "S")
invoice1.create_line("Product", Decimal("1"), Decimal("100"))
signed_xml_1 = tbai.sign(invoice1, "/path/to/cert.p12", "password")
result1 = tbai.send(signed_xml_1, "/path/to/cert.p12", "password")

# Extract SignatureValue from the signed XML or API response
# (In production, you would extract this from result1 or the signed XML)
signature_value_1 = "MEJP9Z/7SbnG+Fb8BzZAbWYRj95wFgY0jwcZhpMMf+Sbhjn1Cc..."

# Second invoice (chained to first)
invoice2 = tbai.create_invoice("A", 2, "Second invoice", "S")
invoice2.set_previous_invoice(
    serial_code="A",
    num="1",
    expedition_date="22-01-2026",  # Format: DD-MM-YYYY
    signature_value=signature_value_1
)
invoice2.create_line("Product", Decimal("1"), Decimal("200"))
signed_xml_2 = tbai.sign(invoice2, "/path/to/cert.p12", "password")
result2 = tbai.send(signed_xml_2, "/path/to/cert.p12", "password")
```

**Important Notes:**

- The **first invoice** of each series should NOT have a previous invoice
- Only **subsequent invoices** should use `set_previous_invoice()`
- The `signature_value` is typically extracted from Hacienda's response after successfully sending the previous invoice
- TicketBAI only uses the first 100 characters of the SignatureValue (this is handled automatically)

## TODO

- [ ] Recipient data
- [ ] Multiple recipient data
- [ ] Third party / Recipient's invoices
- [ ] Corrective invoices
- [ ] Corrected or replaced invoices
- [ ] Tax free invoices
- [ ] Invoices without national counterparty
- [x] ~~Chaining of previous invoice~~ ✅ **IMPLEMENTED**

## How to contribute

Please read the [Code of Conduct documentation](CODE_OF_CONDUCT.md) first, then all contributions are done via Pull Requests on GitHub but don´t hesitate to open a new issue.

## Credits

This project is made by [CodeSyntax](https://codesyntax.com).
