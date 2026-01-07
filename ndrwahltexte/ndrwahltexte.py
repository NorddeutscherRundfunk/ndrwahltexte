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


def safe_get_party_data(df, index):
    """Safely extract party and percentage from dataframe row.

    Returns:
        tuple: (partei, prozent) or (None, None) if index doesn't exist
    """
    if index < len(df):
        return df.at[index, 'partei'], float(df.at[index, 'prozent'])
    return None, None

def analyse_election_data(data):
    """Analysiert Wahldaten und erstellt ein Dictionary mit Variablen für Templates."""
    election_data, results_data, candidate_df = load_election_data(data)

    # Basis-Variablen
    name = election_data['gks_name'].split(',')[0]
    num_parties = len(candidate_df)

    # Extract party data safely
    gewinner_partei, gewinner_prozent = safe_get_party_data(candidate_df, 0)
    zweite_partei, zweite_prozent = safe_get_party_data(candidate_df, 1)
    dritte_partei, dritte_prozent = safe_get_party_data(candidate_df, 2)
    vierte_partei, vierte_prozent = safe_get_party_data(candidate_df, 3)
    fuenfte_partei, fuenfte_prozent = safe_get_party_data(candidate_df, 4)

    variables = {
        'ortsname': name,
        'name': name,
        'num_parties': num_parties,
        'gewinner_partei': gewinner_partei,
        'gewinner_prozent': gewinner_prozent,
        'gewinner_pronomen': PARTEI_PRONOMEN.get(gewinner_partei, 'Sie') if gewinner_partei else None,
        'zweite_partei': zweite_partei,
        'zweite_prozent': zweite_prozent,
        'dritte_partei': dritte_partei,
        'dritte_prozent': dritte_prozent,
        'vierte_partei': vierte_partei,
        'vierte_prozent': vierte_prozent,
        'fuenfte_partei': fuenfte_partei,
        'fuenfte_prozent': fuenfte_prozent,
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