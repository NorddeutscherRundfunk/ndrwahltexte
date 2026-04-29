########################
#
# Dieses Script konvertiert Wahlergebnis-Daten in Fließtext
# Verwendet robotext.TemplateEngine für Textgenerierung
# -> l.sander.fm@ndr.de 
# 
#########################

import json
import sys
import pandas as pd

from .robotext import TemplateEngine
from .templates.parties import PARTEI_PRONOMEN
from .templates import load_for  # NEW: use auto-loader
from .utils import write_error

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
    wahlart = election_data['wahlart']
    ergebnis_art = results_data['ergebnis_art']
    wahlberechtigte = election_data['anz_wahlberechtigte']
    wahlbeteiligung = results_data['wahlbeteil']
    wahlorgan = election_data['organ']

    # Extract party data safely
    gewinner_partei, gewinner_prozent = safe_get_party_data(candidate_df, 0)
    zweite_partei, zweite_prozent = safe_get_party_data(candidate_df, 1)
    dritte_partei, dritte_prozent = safe_get_party_data(candidate_df, 2)
    vierte_partei, vierte_prozent = safe_get_party_data(candidate_df, 3)
    fuenfte_partei, fuenfte_prozent = safe_get_party_data(candidate_df, 4)

    variables = {
        'ortsname': name,
        'name': name,
        'wahlart': wahlart,
        'wahlorgan': wahlorgan,
        'ergebnis_art': ergebnis_art,
        'num_parties': num_parties,
        'wahlberechtigte': wahlberechtigte,
        'wahlbeteiligung': wahlbeteiligung,
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

    # Load templates and corrections by convention
    # Note: load_for now handles its own errors and exits
    config = load_for(variables['wahlart'], variables['ergebnis_art'])

    # TemplateEngine initialisieren
    engine = TemplateEngine(
        templates=config['templates'],
        variables=variables,
        corrections=config['corrections']
    )

    # Titel generieren
    titel = engine.build_text(engine.select_templates(filter_topic="ergebnis"))

    # Absatz1 generieren
    absatz1 = engine.build_text(engine.select_templates(filter_topic="absatz1"))

    # Prüfen ob Titel oder Absatz1 leer sind
    if not titel or not titel.strip() or not absatz1 or not absatz1.strip():
        return {
            'error': 'Für diese Daten konnte kein Wahltext geschrieben werden.'
        }

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

    # Prüfen ob ein Fehler zurückgegeben wurde
    if 'error' in new_data:
        error_obj = {
            "error": {
                "type": "ValidationError",
                "message": new_data['error'],
                "traceback": ""
            }
        }
        print(json.dumps(error_obj, indent=2), file=sys.stderr)
        sys.exit(1)

    json.dump(new_data, sys.stdout, indent=2)


if __name__ == "__main__":
    main()