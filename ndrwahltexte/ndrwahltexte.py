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
from pathlib import Path

from .robotext import TemplateEngine
from .params import TEMPLATES, CORRECTIONS


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


def analyse_election_data(data):
    """Analysiert Wahldaten und erstellt ein Dictionary mit Variablen für Templates."""
    election_data, results_data, candidate_df = load_election_data(data)
    
    variables = {
        'ortsname': election_data['gks_name'].split(',')[0],
        'gewinner_partei': candidate_df.at[0, 'partei'],
        'gewinner_prozent': candidate_df.at[0, 'prozent'],
        'zweite_partei': candidate_df.at[1, 'partei'],
        'zweite_prozent': candidate_df.at[1, 'prozent'],
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
    
    # Text generieren (nur "titel" Template)
    selected = engine.select_templates(filter_topic="ergebnis")
    text = engine.build_text(selected)
    
    # Text in Datenstruktur einfügen
    data['wahl']['ergebnis'].setdefault("texte", {})['Titel'] = text
    return data


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