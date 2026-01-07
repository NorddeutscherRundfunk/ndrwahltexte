########################
#
# Dieses Script konvertiert Wahlergebnis-Daten in Fließtext
# Verwendet robotext.TemplateEngine für Textgenerierung
# -> l.sander.fm@ndr.de 
# 
#########################

import json
import sys
import traceback
import pandas as pd

from .robotext import TemplateEngine
from .params import TEMPLATES, CORRECTIONS, PARTEI_PRONOMEN

def write_error(e):
    """Gibt Fehler als JSON auf stderr aus."""
    error_obj = {
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
    }
    print(json.dumps(error_obj, indent=2), file=sys.stderr)


def removekey(d, key):
    """Entfernt einen Schlüssel aus einem Dictionary und gibt eine Kopie zurück."""
    r = dict(d)
    del r[key]
    return r

def load_election_data(data):
    """Lädt und verarbeitet Wahldaten aus dem JSON-Input."""
    try:
        election_data = data.get('wahl').copy()
        election_data = removekey(election_data, 'ergebnis').copy()
        election_data = removekey(election_data, 'kandidaten').copy()

        results_data = data.get('wahl').get('ergebnis').copy()

        candidate_data = data.get('wahl').get('ergebnis').get('kandidaten').copy()
        candidate_ref = data.get('wahl').get('kandidaten').copy()
        candidate_df = pd.DataFrame(candidate_data).merge(
            pd.DataFrame(candidate_ref),
            on=['kandidatur_id', 'pos'],
            how='left'
        )
        candidate_df = candidate_df.sort_values('prozent', ascending=False).reset_index(drop=True)

        return election_data, results_data, candidate_df
    except Exception as e:
        write_error(e)
        sys.exit(1)


def to_decimal_comma(value):
    """Konvertiert Dezimalpunkt zu Komma und entfernt trailing .0"""
    str_value = str(value).replace('.', ',')
    if str_value.endswith(',0'):
        str_value = str_value[:-2]
    return str_value


def format_wahlberechtigte(value):
    """Formatiert Wahlberechtigte mit Tausenderpunkt"""
    return f"{int(value):,}".replace(',', '.')


def analyse_election_data(data):
    """Analysiert Wahldaten und erstellt ein Dictionary mit Variablen für Templates."""
    election_data, results_data, candidate_df = load_election_data(data)
    print(candidate_df)
    # Basis-Variablen
    name = election_data['gks_name'].split(',')[0]

    # Top 5 Parteien
    gewinner_partei = candidate_df.at[0, 'partei']
    zweite_partei = candidate_df.at[1, 'partei']
    dritte_partei = candidate_df.at[2, 'partei']
    vierte_partei = candidate_df.at[3, 'partei']
    fuenfte_partei = candidate_df.at[4, 'partei']

    variables = {
        'ortsname': name,
        'name': name,
        'gewinner_partei': gewinner_partei,
        'gewinner_prozent': to_decimal_comma(candidate_df.at[0, 'prozent']),
        'gewinner_pronomen': PARTEI_PRONOMEN.get(gewinner_partei, 'Sie'),
        'zweite_partei': zweite_partei,
        'zweite_prozent': to_decimal_comma(candidate_df.at[1, 'prozent']),
        'dritte_partei': dritte_partei,
        'dritte_prozent': to_decimal_comma(candidate_df.at[2, 'prozent']),
        'vierte_partei': vierte_partei,
        'vierte_prozent': to_decimal_comma(candidate_df.at[3, 'prozent']),
        'fuenfte_partei': fuenfte_partei,
        'fuenfte_prozent': to_decimal_comma(candidate_df.at[4, 'prozent']),
    }
    return variables


def write_election_text(data):
    """Generiert Wahltext mit TemplateEngine und fügt ihn den Daten hinzu."""
    variables = analyse_election_data(data)

    # TemplateEngine initialisieren
    engine = TemplateEngine(
        templates=TEMPLATES,
        variables=variables,
        corrections=CORRECTIONS
    )

    # Titel generieren
    titel_selected = engine.select_templates(filter_topic="ergebnis")
    titel = engine.build_text(titel_selected)

    # Absatz1 generieren
    absatz1_selected = engine.select_templates(filter_topic="absatz1")
    absatz1 = engine.build_text(absatz1_selected)

    return {
        'Titel': titel,
        'Absatz1': absatz1
    }


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        write_error(e)
        sys.exit(1)

    new_data = write_election_text(data)
    json.dump(new_data, sys.stdout, indent=2)


if __name__ == "__main__":
    main()