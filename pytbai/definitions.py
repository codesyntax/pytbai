from decimal import Decimal

TICKETBAI_ACTUAL_VERSION = "1.2"
DOCUMENTATION_URL = "https://www.gipuzkoa.eus/eu/web/ogasuna/ticketbai/dokumentazioa-eta-araudia"

DEFAULT_VAT_RATE = Decimal("21")

GIPUZKOA = "Gipuzkoa"
AUTHORITY_APIS = {
    "Araba": "",
    "Bizkaia": "",
    GIPUZKOA: {
        "DEV": {
            "invoice": "https://tbai-z.prep.gipuzkoa.eus/sarrerak/alta",
            "qr": "https://tbai.prep.gipuzkoa.eus/qr",
        },
        "PROD": {
            "invoice": "https://tbai.egoitza.gipuzkoa.eus/sarrerak/alta",
            "qr": "https://tbai.egoitza.gipuzkoa.eus/qr",
        },
    },
}

S = "S"  # Bai
N = "N"  # Ez

# Hainbat hartzaile
L3 = [
    S,
    N,
]

L4 = [
    "N",  # Jaulkitzaileak berak egindako faktura
    "T",  # Hirugarrenak egindako faktura
    "D",  # Eragiketaren hartzaileak egindako faktura
]

# Faktura sinplifikatua
L5 = [
    S,
    N,
]

# Faktura sinplifikatuaren ordez egindako faktura
L6 = [
    S,
    N,
]

DEFAULT_VAT = "01"
# BEZaren eta zerga garrantzia duten eragiketen erregimen bereziko gakoa
L9 = [
    DEFAULT_VAT,  # Erregimen orokorreko eragiketa eta hurrengo balioetan jaso gabe dagoen beste edozein kasu
    "02",  # Esportazioa
    "03",  # Erabilitako ondasunen, arte objektuen, zaharkinen eta bilduma objektuen araudi berezia aplikatzen zaien eragiketak
    "04",  # Inbertsio urrearen erregimen berezia
    "05",  # Bidaia agentzien erregimen berezia
    "06",  # BEZeko entitateen multzoaren erregimen berezia (maila aurreratua)
    "07",  # Kutxa irizpidearen erregimen berezia
    "08",  # Ekoizpen, zerbitzu eta inportazioaren gaineko zergari edo kanarietako zeharkako zerga orokorrari lotutako eragiketak
    "09",  # Besteren izenean eta kontura ari diren bidai agentziek egindako zerbitzuen fakturazioa (Fakturazio Erregelamenduko 3. xedapen gehigarria)
    "10",  # Hirugarrenen kontura kobratzea ordainsari profesionalak edo jabetza industrialetik eratorritako eskubideak, egilearenak edo bazkideen, elkartekideen edo elkargokideen kontura kobratzeko eginkizun horiek betetzen dituzten sozietate, elkarte, elkargo profesional edo bestelako entitateek egindakoak
    "11",  # Negozio lokala errentatzeko eragiketak, atxikipenari lotuak
    "12",  # Negozio lokala errentatzeko eragiketak, atxikipenari lotu gabeak
    "13",  # Negozio lokala errentatzeko eragiketak, atxikipenari lotuak eta lotu gabeak
    "14",  # Hartzailea administrazio publiko bat denean ordaintzeke dauden BEZdun fakturak, obra Ziurtagirietakoak
    "15",  # Segidako traktuko eragiketetan ordaintzeke dagoen BEZdun faktura
    "17",  # IX. tituluko XI. kapituluan aurreikusitako araubideetako batera (OSS edo IOSS) bildutako eragiketa
    "19",  # Nezakaritza, abeltzaintza eta arrantzako araubide berezian (NAAAB) dauden jardueren eragiketak
    "51",  # Baliokidetasun errekarguko eragiketak
    "52",  # Erregimen sinplifikatuko eragiketak
    "53",  # BEZaren ondorioetarako enpresari edo profesionaltzat jotzen ez diren pertsona edo entitateek egindako eragiketak
]


# Salbuetsi gabeko eragiketaren mota
S1 = "S1"
L11 = [
    S1,  # Subjektu pasiboaren inbertsiorik gabe
    "S2",  # Subjektu pasiboaren inbertsioarekin
]
