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

## TODO

- [ ] Recipient data
- [ ] Multiple recipient data
- [ ] Third party / Recipient's invoices
- [ ] Corrective invoices
- [ ] Corrected or replaced invoices
- [ ] Tax free invoices
- [ ] Invoices without national counterparty
- [x] Chaining of previous invoice

## How to contribute

Please read the [Code of Conduct documentation](CODE_OF_CONDUCT.md) first, then all contributions are done via Pull Requests on GitHub but don´t hesitate to open a new issue.

## Credits

This project is made by [CodeSyntax](https://codesyntax.com).
