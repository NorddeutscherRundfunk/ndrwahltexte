########################
#
# Dieses Script enthält Projekt-Variablen für ndrwahltexte
# Ersetzt parteigrammatik.csv durch regex-basierte Korrekturen
# -> l.sander.fm@ndr.de 
# 
#########################
import re

# Parteien nach grammatischem Geschlecht gruppiert
PARTEIEN = {
    'feminin': ['SPD', 'CDU', 'AfD', 'FDP', 'CSU', 'MLPD', 'Tierschutzpartei'],
    'neutrum': ['BSW', 'Bündnis Deutschland'],
    'mit_partei_davor': ['Volt', 'dieBasis LV', 'FW-PB'],  # FW-PB = "die Partei Freie Wähler"
}

# Spezielle Pluralformen
PLURAL_PARTEIEN = {
    'Grüne': 'Grünen',
    'Linke': 'Linken',
}

# Partei-Namen für "mit Partei davor" Kategorie
PARTEI_NAMEN = {
    'Volt': 'Volt',
    'dieBasis LV': 'dieBasis',
    'FW-PB': 'Freie Wähler',
}

# Pronomen für Parteien (Sie/Er/Es)
PARTEI_PRONOMEN = {
    'SPD': 'Sie',
    'CDU': 'Sie',
    'AfD': 'Sie',
    'FDP': 'Sie',
    'Grüne': 'Sie',
    'Linke': 'Sie',
    'BSW': 'Es',
    'CSU': 'Sie',
    'FW-PB': 'Sie',
    'Volt': 'Sie',
    'dieBasis LV': 'Sie',
    'MLPD': 'Sie',
    'Tierschutzpartei': 'Sie',
    'Bündnis Deutschland': 'Es',
}

# Templates für Wahltexte
TEMPLATES = {
    # === TITEL ===
    "titel_gleichauf": {
        "topic": "ergebnis",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "{wahlorgan}swahl: In {name} sind {gewinner_partei} und {zweite_partei} gleichauf"
    },

    "titel_absolute_mehrheit": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent >= 50", "gewinner_prozent != zweite_prozent", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "{wahlorgan}swahl: Absolute Mehrheit für {gewinner_partei} in {name}"
    },

    "titel_gewinner_vorn": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent < 50", "gewinner_prozent != zweite_prozent", "wahlart == 'Verhältniswahl'","ergebnis_art != 'Kein Ergebnis'"],
        "text": "{wahlorgan}swahl: {gewinner_partei} stärkste Kraft in {name}"
    },

    # === ABSATZ1 ===
    "absatz1_gleichauf": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Bei der {wahlorgan}swahl in {name} sind {gewinner_partei} und {zweite_partei} bei den Zweitstimmen gleichauf. Für sie stimmten jeweils {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Bei der {wahlorgan}swahl in {name} gingen die meisten Zweitstimmen an {gewinner_partei}. Für {gewinner_partei} stimmten {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner_allein": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Bei der {wahlorgan}swahl in {name} gingen die meisten Zweitstimmen an {gewinner_partei}. Für {gewinner_partei} stimmten {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_keine_weiteren": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "In {name} traten keine weiteren Parteien an."
    },

    "absatz1_abstand_plural": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei == 'Grüne'", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "{gewinner_pronomen} liegen damit in {name} vor {zweite_partei}. Für {zweite_partei} stimmten in {name} {zweite_prozent} Prozent."
    },

    "absatz1_abstand_singular": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei != 'Grüne'", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "{gewinner_pronomen} liegt damit in {name} vor {zweite_partei}. Für {zweite_partei} stimmten in {name} {zweite_prozent} Prozent."
    },

    # === WEITERE PARTEIEN ===
    "absatz1_weitere_5": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 5", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Danach folgen {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei, {vierte_partei} ({vierte_prozent} Prozent) und {fuenfte_partei} ({fuenfte_prozent} Prozent)."
    },

    "absatz1_weitere_4": {
        "topic": "absatz1",
        "conditions": ["num_parties == 4", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Danach folgen zufolge {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei und {vierte_partei} mit {vierte_prozent} Prozent."
    },

    "absatz1_weitere_3": {
        "topic": "absatz1",
        "conditions": ["num_parties == 3", "wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "Auf dem dritten Platz folgt {dritte_partei} mit {dritte_prozent} Prozent."
    },

    # === WAHLBETETEILIGUNG ===
    "absatz1_wahlbeteiligung": {
        "topic": "absatz1",
        "conditions": ["wahlart == 'Verhältniswahl'", "ergebnis_art != 'Kein Ergebnis'"],
        "text": "In {name} leben {wahlberechtigte} Wahlberechtigte, die Wahlbeteiligung lag bei {wahlbeteiligung} Prozent."
    }
}

# Alle Templates für Artikelkorrekturen
ALL_TEMPLATES = TEMPLATES.keys()
TITEL_TEMPLATES = [template for template in TEMPLATES.keys() if "titel" in template]
ABSATZ_TEMPLATES = [template for template in TEMPLATES.keys() if "absatz" in template]

DATIV_TEMPLATES = ["absatz1_abstand_plural", "absatz1_abstand_singular"]


# Korrekturen für grammatisch korrekte Parteinamen
# Diese werden dynamisch aus den Parteien-Listen generiert
def _build_corrections():
    corrections = {}

    # === NUMBER FORMATTING: remove trailing .0 ===
    # Matches decimal numbers like "34.5" or "50.0" and converts them
    corrections[r'\b(\d+)\.0\b'] = {
        "replacement": r"\1",
        "applies_to": ALL_TEMPLATES
    }
    # === NUMBER FORMATTING: Decimal point to comma ===
    corrections[r'\b(\d+)\.(\d+)\b'] = {
        "replacement": r"\1,\2",
        "applies_to": ALL_TEMPLATES
    }

    # === NUMBER FORMATTING: Add . between thousands in numbers ===
    def format_german_number(m):
        num = m.group(1)
        return f"{int(num):,}".replace(",", ".")

    corrections[r'\b(\d{5,})\b'] = {
        "replacement": format_german_number,
        "applies_to": ALL_TEMPLATES
    }

    # === AKKUSATIV & DATIV: Orte (in → im) ===
    corrections[r'\b([iI])n Kreis\b'] = {
        "replacement": r"\1m Kreis",
        "applies_to": ALL_TEMPLATES
    }

    # === NOMINATIV & AKKUSATIV: Feminine Parteien (die → die) ===
    feminin_pattern = r'\b(' + '|'.join(PARTEIEN['feminin']) + r')\b'
    corrections[feminin_pattern] = {
        "replacement": r"die \1",
        "applies_to": ABSATZ_TEMPLATES
    }

    # === NOMINATIV & AKKUSATIV: Neutrum Parteien (das → das) ===
    neutrum_pattern = r'\b(' + '|'.join(PARTEIEN['neutrum']) + r')\b'
    corrections[neutrum_pattern] = {
        "replacement": r"das \1",
        "applies_to": ABSATZ_TEMPLATES
    }

    # === NOMINATIV & AKKUSATIV: Parteien mit "Partei" davor ===
    for partei_key in PARTEIEN['mit_partei_davor']:
        partei_name = PARTEI_NAMEN[partei_key]
        corrections[rf'\b{partei_key}\b'] = {
            "replacement": f"die Partei {partei_name}",
            "applies_to": ABSATZ_TEMPLATES
        }

    # === NOMINATIV & AKKUSATIV: Pluralformen (die Grünen, Die Linke) ===
    corrections[r'\bGrüne\b'] = {
        "replacement": "die Grünen",
        "applies_to": ABSATZ_TEMPLATES
    }
    corrections[r'\bLinke\b'] = {
        "replacement": "Die Linke",
        "applies_to": ABSATZ_TEMPLATES
    }

    # === DATIV: Feminine Parteien (der) ===
    feminin_dativ_pattern = r'\bvor die (' + '|'.join(PARTEIEN['feminin']) + r')\b'
    corrections[feminin_dativ_pattern] = {
        "replacement": r"vor der \1",
        "applies_to": DATIV_TEMPLATES
    }

    # === DATIV: Neutrum Parteien (dem) ===
    neutrum_dativ_pattern = r'\bvor das (' + '|'.join(PARTEIEN['neutrum']) + r')\b'
    corrections[neutrum_dativ_pattern] = {
        "replacement": r"vor dem \1",
        "applies_to": DATIV_TEMPLATES
    }

    # === DATIV: Parteien mit "Partei" davor (der Partei) ===
    for partei_key in PARTEIEN['mit_partei_davor']:
        partei_name = PARTEI_NAMEN[partei_key]
        corrections[rf'\bvor die Partei {partei_key}\b'] = {
            "replacement": f"vor der Partei {partei_name}",
            "applies_to": DATIV_TEMPLATES
        }

    # === DATIV: Pluralformen (den Grünen, Der Linken) ===
    corrections[r'\bvor die Grüne\b'] = {
        "replacement": "vor den Grünen",
        "applies_to": DATIV_TEMPLATES
    }
    corrections[r'\bvor Die Linke\b'] = {
        "replacement": "vor Der Linken",
        "applies_to": DATIV_TEMPLATES
    }

    return corrections


CORRECTIONS = _build_corrections()