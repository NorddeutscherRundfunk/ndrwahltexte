"""
Corrections specific to Verhältniswahl templates.
Handles German party name grammar (articles, cases).
"""

from ..parties import PARTEIEN, PARTEI_NAMEN


def build_verhaeltniswahl_corrections(template_keys):
    """
    Build corrections specific to Verhältniswahl templates.

    Args:
        template_keys: List of template keys to determine applies_to scope

    Returns:
        dict: Correction patterns specific to Verhältniswahl
    """
    corrections = {}

    # Determine which templates need which corrections
    absatz_templates = [k for k in template_keys if 'absatz' in k]
    dativ_templates = [k for k in template_keys if 'dativ' in k]
    all_templates = list(template_keys)

    # === AKKUSATIV & DATIV: Orte (in → im) ===
    corrections[r'\b([iI])n Kreis\b'] = {
        "replacement": r"\1m Kreis",
        "applies_to": all_templates
    }

    # === NOMINATIV & AKKUSATIV: Feminine Parteien (die → die) ===
    feminin_pattern = r'\b(' + '|'.join(PARTEIEN['feminin']) + r')\b'
    corrections[feminin_pattern] = {
        "replacement": r"die \1",
        "applies_to": absatz_templates
    }

    # === NOMINATIV & AKKUSATIV: Neutrum Parteien (das → das) ===
    neutrum_pattern = r'\b(' + '|'.join(PARTEIEN['neutrum']) + r')\b'
    corrections[neutrum_pattern] = {
        "replacement": r"das \1",
        "applies_to": absatz_templates
    }

    # === NOMINATIV & AKKUSATIV: Parteien mit "Partei" davor ===
    for partei_key in PARTEIEN['mit_partei_davor']:
        partei_name = PARTEI_NAMEN[partei_key]
        corrections[rf'\b{partei_key}\b'] = {
            "replacement": f"die Partei {partei_name}",
            "applies_to": absatz_templates
        }

    # === NOMINATIV & AKKUSATIV: Pluralformen (die Grünen, Die Linke) ===
    corrections[r'\bGrüne\b'] = {
        "replacement": "die Grünen",
        "applies_to": absatz_templates
    }
    corrections[r'\bLinke\b'] = {
        "replacement": "Die Linke",
        "applies_to": absatz_templates
    }

    # === DATIV: Feminine Parteien (der) ===
    feminin_dativ_pattern = r'\bvor die (' + '|'.join(PARTEIEN['feminin'])+ '|Partei' + r')\b'
    corrections[feminin_dativ_pattern] = {
        "replacement": r"vor der \1",
        "applies_to": dativ_templates
    }

    # === DATIV: Neutrum Parteien (dem) ===
    neutrum_dativ_pattern = r'\bvor das (' + '|'.join(PARTEIEN['neutrum']) + r')\b'
    corrections[neutrum_dativ_pattern] = {
        "replacement": r"vor dem \1",
        "applies_to": dativ_templates
    }

    # === DATIV: Parteien mit "Partei" davor (der Partei) ===
    for partei_key in PARTEIEN['mit_partei_davor']:
        partei_name = PARTEI_NAMEN[partei_key]
        corrections[rf'\bvor die Partei {partei_key}\b'] = {
            "replacement": f"vor der Partei {partei_name}",
            "applies_to": dativ_templates
        }

    # === DATIV: Pluralformen (den Grünen, Der Linken) ===
    corrections[r'\bvor die Grünen\b'] = {
        "replacement": "vor den Grünen",
        "applies_to": dativ_templates
    }
    corrections[r'\bvor Die Linke\b'] = {
        "replacement": "vor Der Linken",
        "applies_to": dativ_templates
    }

    # === AUSZÄHLUNG einem Wahlbereich ===
    corrections[r'Auszählung von 1 von'] = {
        "replacement": "Auszählung von einem von",
        "applies_to": dativ_templates
    }

    return corrections