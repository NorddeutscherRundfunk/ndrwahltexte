"""
Templates for Verhältniswahl with result data available.
(All result types containing "Endergebnis")
"""

TEMPLATES = {
    # === TITEL ===
    "titel_gleichauf": {
        "topic": "ergebnis",
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "{wahlorgan}swahl: In {name} sind {gewinner_partei} und {zweite_partei} gleichauf"
    },

    "titel_absolute_mehrheit": {
        "topic": "ergebnis",
        "grammar": ["akkusativ"],
        "conditions": ["gewinner_prozent > 50", "gewinner_prozent != zweite_prozent"],
        "text": "{wahlorgan}swahl: Absolute Mehrheit für {gewinner_partei} in {name}"
    },

    "titel_gewinner_vorn": {
        "topic": "ergebnis",
        "conditions": ["gewinner_prozent <= 50", "gewinner_prozent != zweite_prozent"],
        "text": "{wahlorgan}swahl: {gewinner_partei} stärkste Kraft in {name}"
    },

    # === ABSATZ1 ===
    "absatz1_gleichauf": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties >= 2", "gewinner_prozent == zweite_prozent"],
        "text": "Bei der {wahlorgan}swahl in {name} sind {gewinner_partei} und {zweite_partei} gleichauf. Für sie stimmten jeweils {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent"],
        "text": "Bei der {wahlorgan}swahl in {name} gingen die meisten Stimmen an {gewinner_partei}. Für {gewinner_partei} stimmten {gewinner_prozent} Prozent der Wählerinnen und Wähler."
    },

    "absatz1_gewinner_allein": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties == 1"],
        "text": "Bei der {wahlorgan}swahl in {name} gingen {gewinner_prozent} Prozent der Stimmen an {gewinner_partei}."
    },

    "absatz1_keine_weiteren": {
        "topic": "absatz1",
        "conditions": ["num_parties == 1"],
        "text": "In {name} traten keine weiteren Parteien an."
    },

    "absatz1_abstand_plural": {
        "topic": "absatz1",
        "grammar": ["akkusativ", "dativ", "plural"],
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei == 'Grüne'"],
        "text": "{gewinner_pronomen} liegen damit vor {zweite_partei}. Für {zweite_partei} stimmten {zweite_prozent} Prozent."
    },

    "absatz1_abstand_singular": {
        "topic": "absatz1",
        "grammar": ["akkusativ", "dativ", "singular"],
        "conditions": ["num_parties >= 2", "gewinner_prozent != zweite_prozent", "gewinner_partei != 'Grüne'"],
        "text": "{gewinner_pronomen} liegt damit vor {zweite_partei}. Für {zweite_partei} stimmten {zweite_prozent} Prozent."
    },

    # === WEITERE PARTEIEN ===
    "absatz1_weitere_5": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties >= 5"],
        "text": "Danach folgen {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei, {vierte_partei} ({vierte_prozent} Prozent) und {fuenfte_partei} ({fuenfte_prozent} Prozent)."
    },

    "absatz1_weitere_4": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties == 4"],
        "text": "Danach folgen {dritte_partei} mit {dritte_prozent} Prozent auf Platz drei und {vierte_partei} mit {vierte_prozent} Prozent."
    },

    "absatz1_weitere_3": {
        "topic": "absatz1",
        "grammar": ["nominativ"],
        "conditions": ["num_parties == 3"],
        "text": "Auf dem dritten Platz folgt {dritte_partei} mit {dritte_prozent} Prozent."
    },

    # === WAHLBETEILIGUNG ===
    "absatz1_wahlberechtigte": {
        "topic": "absatz1",
        "conditions": [],
        "text": "In {name} leben {wahlberechtigte} Wahlberechtigte."
    },

    "absatz1_wahlbeteiligung": {
        "topic": "absatz1",
        "conditions": [],
        "text": "Die Wahlbeteiligung lag bei {wahlbeteiligung} Prozent."
    },

    # --- Kein Vorwahlergebnis vorhanden ---
    "absatz2_kein_vorwahlergebnis": {
        "topic": "absatz2",
        "conditions": ["hat_vorwahlergebnis == False"],
        "text": "Für {name} liegt kein Ergebnis der vorherigen {wahlorgan}swahl vor. Entweder es gab diese Gemeinde damals noch nicht oder sie wurde für die Wahl mit einer anderen zusammengelegt, weil sie zu klein war, oder es liegt ein anderer Fehler vor."
    },

    # --- Neue stärkste Kraft: Gewinner vorher nicht angetreten ---
    "absatz2_neue_kraft_nicht_angetreten": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei != gewinner_partei_alt",
            "gewinner_prozent != zweite_prozent",
            "gewinner_rang_vorher == 'nicht angetreten'",
        ],
        "grammar": ["nominativ"],
        "text": "{gewinner_partei} ist damit bei der {wahlorgan}swahl neue stärkste Kraft in {name}. Bei der vorherigen {wahlorgan}swahl ist {gewinner_partei} nicht angetreten. Bei der vorherigen {wahlorgan}swahl hatte {gewinner_partei_alt} hier die meisten Stimmen bekommen ({gewinner_prozent_alt} Prozent), das ist eine Veränderung von {gewinner_alt_differenz} Prozentpunkten."
    },

    # --- Neue stärkste Kraft: Gewinner vorher auf Platz X ---
    "absatz2_neue_kraft_mit_rang": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei != gewinner_partei_alt",
            "gewinner_prozent != zweite_prozent",
            "gewinner_rang_vorher != 'nicht angetreten'",
        ],
        "grammar": ["nominativ"],
        "text": "{gewinner_partei} ist damit bei der {wahlorgan}swahl neue stärkste Kraft in {name}. Bei der vorherigen Wahl lag {gewinner_pronomen} mit {gewinner_ergebnis_alt} Prozent der Stimmen auf Platz {gewinner_rang_vorher}. Bei der letzten {wahlorgan}swahl hatte {gewinner_partei_alt} hier die meisten Stimmen bekommen ({gewinner_prozent_alt} Prozent), das ist eine Veränderung von {gewinner_alt_differenz} Prozentpunkten."
    },

    # --- Gleiche stärkste Kraft: Gewinner war 2021 nicht angetreten ---
    "absatz2_gleiche_kraft_nicht_angetreten": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_rang_vorher == 'nicht angetreten'",
        ],
        "grammar": ["nominativ"],
        "text": "{gewinner_partei} war vorherigen {wahlorgan}swahl nicht angetreten, erhielt aber aus dem Stand die meisten Stimmen."
    },

    # --- Gleiche stärkste Kraft: Ergebnisvergleich ---
    "absatz2_gleiche_kraft_vergleich": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei == gewinner_partei_alt",
            "gewinner_rang_vorher != 'nicht angetreten'",
            "gewinner_prozent != gewinner_prozent_alt",
        ],
        "grammar": ["nominativ"],
        "text": "{gewinner_partei} hat damit im Vergleich zur vorherigen {wahlorgan}swahl in {name} das Ergebnis {change_phrase}. Die Veränderung bei den Stimmen beträgt {gewinner_differenz} Prozentpunkte."
    },

    # --- Gleiche stärkste Kraft: Ergebnis unverändert ---
    "absatz2_gleiche_kraft_unveraendert": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei == gewinner_partei_alt",
            "gewinner_rang_vorher != 'nicht angetreten'",
            "gewinner_prozent == gewinner_prozent_alt",
        ],
        "grammar": ["nominativ"],
        "text": "Das Ergebnis von {gewinner_partei} ist im Vergleich zur vorherigen {wahlorgan}swahl in {name} unverändert geblieben."
    },

    # --- Größter Stimmenzuwachs (nur wenn Zuwachspartei != Gewinner und Gewinner vorher angetreten) ---
    "absatz2_meist_zugewinn": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei != meist_zugewinn_partei",
        ],
        "grammar": ["nominativ"],
        "text": "{meist_zugewinn_partei} verzeichnet den größten Stimmenzuwachs ({meist_zugewinn_prozent} Prozentpunkte) in {name}."
    },

    # --- Größte Verluste (nur wenn Verlustpartei != Gewinner) ---
    "absatz2_meist_verlust": {
        "topic": "absatz2",
        "conditions": [
            "hat_vorwahlergebnis == True",
            "gewinner_partei != meist_verlust_partei",
        ],
        "grammar": ["nominativ"],
        "text": "{meist_verlust_partei} hat dort mit {meist_verlust_prozent} Prozentpunkten die größten Verluste zu verzeichnen."
    },
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