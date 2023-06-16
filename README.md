# TicketBai

TicketBai allows to create, manage and send TicketBai invoices to the Basque tax authorities.

## Usage

You need to configure your bussiness and software info in a JSON file:

```json
{
  "subject": {
    "entity_id": "99999974E",
    "name": "REPRESENTANTESPJ FICTICIO"
  },
  "software": {
    "license": "TBAIGIPRE00000000501",
    "dev_entity": "P2000000F",
    "soft_name": "FAKTURABAI",
    "soft_version": "1.0"
  }
}
```

Then create a invoice:

```python
from ticketbai import TBai

tbai = TBai(json)
invoice = tbai.create_invoice("TB-2021-S", 1, "Primera factura", "S")
```

The `json` parameter is a previous JSON file you've created.

## How to contribute

Please read the [Code of Conduct documentation](CODE_OF_CONDUCT.md) first, then all contributions are done via Pull Requests on GitHub but don´t hesitate to open a new issue.

## Credits

This project is made by [CodeSyntax](https://codesyntax.com).
