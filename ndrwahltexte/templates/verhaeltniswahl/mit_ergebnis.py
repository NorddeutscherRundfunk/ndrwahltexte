"""
Templates for Verhältniswahl with result data available.
(All result types except "Kein Ergebnis")
"""

TEMPLATES = {
    # === TITEL ===
    "titel_gleichauf": {
        "topic": "ergebnis",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "Wahl: In {name} sind {gewinner_partei} und {zweite_partei} gleichauf"
    },

    "titel_absolute_mehrheit": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent >= 50", "gewinner_prozent != zweite_prozent"],
        "text": "Wahl: Absolute Mehrheit für {gewinner_partei} in {name}"
    },

    "titel_gewinner_vorn": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent < 50", "gewinner_prozent != zweite_prozent"],
        "text": "Wahl: {gewinner_partei} stärkste Kraft in {name}"
    },

    # === ABSATZ1 ===
    "absatz1_gleichauf": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "Bei der Wahl in {name} sind {gewinner_partei} und {zweite_partei} bei den Zweitstimmen gleichauf. Für sie stimmten jeweils {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent"],
        "text": "Bei der Wahl in {name} gingen die meisten Zweitstimmen an {gewinner_partei}. Für {gewinner_partei} stimmten {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner_allein": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1"],
        "text": "Bei der Wahl in {name} gingen die meisten Zweitstimmen an {gewinner_partei}. Für {gewinner_partei} stimmten {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_keine_weiteren": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1"],
        "text": "In {name} traten keine weiteren Parteien an."
    },

    "absatz1_abstand_dativ_plural": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei == 'Grüne'"],
        "text": "{gewinner_pronomen} liegen damit in {name} vor {zweite_partei}. Für {zweite_partei} stimmten in {name} {zweite_prozent} Prozent."
    },

    "absatz1_abstand_dativ_singular": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei != 'Grüne'"],
        "text": "{gewinner_pronomen} liegt damit in {name} vor {zweite_partei}. Für {zweite_partei} stimmten in {name} {zweite_prozent} Prozent."
    },

    # === WEITERE PARTEIEN ===
    "absatz1_weitere_5": {
        "topic": "absatz1",
        "conditions": ["num_parties >= 5"],
        "text": "Danach folgen {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei, {vierte_partei} ({vierte_prozent} Prozent) und {fuenfte_partei} ({fuenfte_prozent} Prozent)."
    },

    "absatz1_weitere_4": {
        "topic": "absatz1",
        "conditions": ["num_parties == 4"],
        "text": "Danach folgen {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei und {vierte_partei} mit {vierte_prozent} Prozent."
    },

    "absatz1_weitere_3": {
        "topic": "absatz1",
        "conditions": ["num_parties == 3"],
        "text": "Auf dem dritten Platz folgt {dritte_partei} mit {dritte_prozent} Prozent."
    },

    # === WAHLBETEILIGUNG ===
    "absatz1_wahlbeteiligung": {
        "topic": "absatz1",
        "conditions": [],
        "text": "In {name} leben {wahlberechtigte} Wahlberechtigte, die Wahlbeteiligung lag bei {wahlbeteiligung} Prozent."
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