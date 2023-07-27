TBAI_JSON = {
    "version": "1.2",
    "env": "DEV",
    "subject": {
        "entity_id": "99999974E",
        "name": "REPRESENTANTESPJ FICTICIO",
        "authority_api": "https://tbai-z.prep.gipuzkoa.eus/sarrerak/alta",
        "qr_api": "https://tbai.prep.gipuzkoa.eus/qr/",
        "multi_recipient": "N",
        "external_invoice": "N",
    },
    "software": {
        "license": "TBAIGIPRE00000000501",
        "dev_entity": "P2000000F",
        "soft_name": "FAKTURABAI",
        "soft_version": "1.0",
    },
}

TBAI_INVOICE_JSON = {
    "version": "1.2",
    "env": "DEV",
    "subject": {
        "entity_id": "99999974E",
        "name": "REPRESENTANTESPJ FICTICIO",
        "authority_api": "https://tbai-z.prep.gipuzkoa.eus/sarrerak/alta",
        "qr_api": "https://tbai.prep.gipuzkoa.eus/qr/",
        "multi_recipient": "N",
        "external_invoice": "N",
    },
    "invoice": {
        "serial_code": "TB-2021-S",
        "num": 1,
        "description": "Primera factura",
        "expedition_date": "2023-07-05",
        "expedition_time": "12:58:17",
        "transaction_date": "2023-07-05",
        "simplified": "N",
        "substitution": "N",
        "vat_regime": "01",
        "lines": [],
        "total_amount": 0,
    },
    "software": {
        "license": "TBAIGIPRE00000000501",
        "dev_entity": "P2000000F",
        "soft_name": "FAKTURABAI",
        "soft_version": "1.0",
    },
}

TBAI_INVOICE_LINES_JSON = {
    "version": "1.2",
    "env": "DEV",
    "subject": {
        "entity_id": "99999974E",
        "name": "REPRESENTANTESPJ FICTICIO",
        "authority_api": "https://tbai-z.prep.gipuzkoa.eus/sarrerak/alta",
        "qr_api": "https://tbai.prep.gipuzkoa.eus/qr/",
        "multi_recipient": "N",
        "external_invoice": "N",
    },
    "invoice": {
        "serial_code": "TB-2021-S",
        "num": 1,
        "description": "Primera factura",
        "expedition_date": "2023-07-05",
        "expedition_time": "12:58:17",
        "transaction_date": "2023-07-05",
        "simplified": "N",
        "substitution": "N",
        "vat_regime": "01",
        "lines": [
            {
                "description": "Primer producto",
                "quantity": 1,
                "unit_amount": 200,
                "discount": 20,
                "vat_rate": 21,
                "vat_fee": 33.6,
                "vat_type": "S1",
                "vat_base": 160.0,
                "total": 193.6,
            },
            {
                "description": "Segundo producto",
                "quantity": 2,
                "unit_amount": 350,
                "discount": 0,
                "vat_rate": 21,
                "vat_fee": 147.0,
                "vat_type": "S1",
                "vat_base": 700,
                "total": 847.0,
            },
        ],
        "total_amount": 1040.6,
    },
    "software": {
        "license": "TBAIGIPRE00000000501",
        "dev_entity": "P2000000F",
        "soft_name": "FAKTURABAI",
        "soft_version": "1.0",
    },
}
