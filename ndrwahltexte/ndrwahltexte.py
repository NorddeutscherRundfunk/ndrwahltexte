########################
#
# Dieses Script konvertiert Wahlergebnis-Daten in Fließtext
# -> l.sander.fm@ndr.de 
# 
#########################

#%% load libraries
import json
import pandas as pd
from argparse import ArgumentParser
import logging as log
from pathlib import Path
import sys
import traceback

#%% load global variables
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

cwd = Path.cwd()
mod_path = Path(__file__).parent
partei_rel_path = 'data/raw/parteigrammatik.csv'
partei_src_path = (mod_path / partei_rel_path).resolve()

PARTEI_GRAMMATIK = pd.read_csv(partei_src_path,sep=';').set_index('Kurzname')

def write_error(e):
    error_obj = {
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
    }
    print(json.dumps(error_obj, indent=2), file=sys.stderr)

def load_election_data(data):
    file_data = data
    try:
        election_data = file_data.get('wahl').copy()
        election_data = removekey(election_data,'ergebnis').copy()
        election_data = removekey(election_data,'kandidaten').copy()

        results_data = file_data.get('wahl').get('ergebnis').copy()
        
        candidate_data = file_data.get('wahl').get('ergebnis').get('kandidaten').copy()
        candidate_ref = file_data.get('wahl').get('kandidaten').copy()
        candidate_df = pd.DataFrame(candidate_data).merge(pd.DataFrame(candidate_ref), on=['kandidatur_id','pos'], how='left')
        candidate_df = candidate_df.sort_values('prozent', ascending=False).reset_index(drop=True)
        
        log.info('election data extracted successfully')
        return election_data, results_data, candidate_df
    except Exception as e:
        write_error(e)
        sys.exit(1)

def analyse_election_data(data):
    election_data, results_data, candidate_df = load_election_data(data)
    erg_dict = {'ortsname' : election_data['gks_name'].split(',')[0],
            'gewinner_partei': candidate_df.at[0,'partei'],
           'gewinner_prozent' : candidate_df.at[0,'prozent'],
            'zweite_partei': candidate_df.at[1,'partei'],
           'zweite_prozent' : candidate_df.at[1,'prozent'],
           }
    log.info('election data analysed successfully')
    return erg_dict

def write_election_text(data):
    erg_dict = analyse_election_data(data)
    satz1 = "In {ort} gingen die meisten Zweitstimmen an {gewinner_partei}.".format(ort = erg_dict['ortsname'], gewinner_partei = PARTEI_GRAMMATIK.at[erg_dict['gewinner_partei'],'Artikel NomSin + Parteiname'])
    data['wahl']['ergebnis'].setdefault("texte", {})['Titel']=satz1
    return data

def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        write_error(e)
        sys.exit(1)
        
    new_data = write_election_text(data)
    json.dump(new_data, sys.stdout, indent=2)
    
#%% hier startet das Hauptprogramm
if __name__ == "__main__":
    main()

# %%
