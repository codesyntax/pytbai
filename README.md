![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/codesyntax/pytbai/python-package.yml)

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

tbai = TBai(json)
invoice = tbai.create_invoice("TB-2021-S", 1, "First invoice", "S")

invoice.create_line("First product", 1, 200, 20)
invoice.create_line("Second product", 2, 350)
```

The `json` parameter is a previous JSON file you've created.

Finally sign and send the invoice:

```python
tbai_kode = tbai.sign_and_send(cert_file.p12, "password")
```

## TODO

- [ ] Recipient data
- [ ] Multiple recipient data
- [ ] Third party / Recipient's invoices
- [ ] Corrective invoices
- [ ] Corrected or replaced invoices
- [ ] Tax free invoices
- [ ] Invoices without national counterparty
- [ ] Chaining of previous invoice

## How to contribute

Please read the [Code of Conduct documentation](CODE_OF_CONDUCT.md) first, then all contributions are done via Pull Requests on GitHub but don´t hesitate to open a new issue.

## Credits

This project is made by [CodeSyntax](https://codesyntax.com).
