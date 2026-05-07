"""
Templates for Verhältniswahl with result data available.
(All result types containing "Zwischnergebnis")
"""

TEMPLATES = {
    # === TITEL ===
    "titel_gleichauf": {
        "topic": "ergebnis",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "{wahlorgan}swahl: In {name} sind {gewinner_partei} und {zweite_partei} derzeit gleichauf"
    },

    "titel_gewinner_vorn": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent != zweite_prozent"],
        "text": "{wahlorgan}swahl: {gewinner_partei} führt derzeit in {name}"
    },

    # === ABSATZ1 ===
    "absatz1_gleichauf": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "Bei der {wahlorgan}swahl in {name} liegen {gewinner_partei} und {zweite_partei} nach Auszählung von {gez_wahlbereiche} von {anz_wahlbereiche} Wahlbereichen bei den Zweitstimmen nach bisherigem Auszählungsstand gleichauf. Für sie stimmten bisher jeweils {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent"],
        "text": "Bei der {wahlorgan}swahl in {name} führt nach Auszählung von {gez_wahlbereiche} von {anz_wahlbereiche} Wahlbereichen derzeit {gewinner_partei}. Für {gewinner_partei} stimmten nach aktuellem Stand {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner_allein": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1"],
        "text": "Bei der {wahlorgan}swahl in {name} gingen nach Auszählung von {gez_wahlbereiche} von {anz_wahlbereiche} Wahlbereichen die meisten Zweitstimmen an {gewinner_partei}. Für {gewinner_partei} stimmten nach aktuellem Stand {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_keine_weiteren": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1"],
        "text": "In {name} traten keine weiteren Parteien an."
    },

    "absatz1_abstand_dativ_plural": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei == 'Grüne'"],
        "text": "{gewinner_pronomen} liegen damit Stand vor {zweite_partei}. Für {zweite_partei} stimmten bisher {zweite_prozent} Prozent."
    },

    "absatz1_abstand_dativ_singular": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei != 'Grüne'"],
        "text": "{gewinner_pronomen} liegt damit vor {zweite_partei}. Für {zweite_partei} stimmten bisher {zweite_prozent} Prozent."
    },

    # === WEITERE PARTEIEN ===
    "absatz1_weitere_5": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 5"],
        "text": "Danach folgen derzeit {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei, {vierte_partei} ({vierte_prozent} Prozent) und {fuenfte_partei} ({fuenfte_prozent} Prozent)."
    },

    "absatz1_weitere_4": {
        "topic": "absatz1",
        "conditions": ["num_parties == 4"],
        "text": "Danach folgen derzeit {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei und {vierte_partei} mit {vierte_prozent} Prozent."
    },

    "absatz1_weitere_3": {
        "topic": "absatz1",
        "conditions": ["num_parties == 3"],
        "text": "Auf dem dritten Platz folgt derzeit {dritte_partei} mit {dritte_prozent} Prozent."
    },

    # === WAHLBETEILIGUNG ===
    "absatz1_wahlberechtigte": {
        "topic": "absatz1",
        "conditions": [],
        "text": "In {name} leben {wahlberechtigte} Wahlberechtigte."
    },

    # === NOCH OFFEN ===
    "absatz1_noch_offen": {
        "topic": "absatz1",
        "conditions": [],
        "text": "Das endgültige Ergebnis der {wahlorgan}swahl in {name} steht noch aus."
    }
}

# Optional: Template-specific corrections (rarely needed)
# These only apply to templates in THIS file
LOCAL_CORRECTIONS = {
    # Example: Fix a specific typo only in these templates
    # r'Zweitstimme\b': {
    #     "replacement": "Zweitstimmen",
    #     "applies_to": ["absatz1_gleichauf"]
    # }
}