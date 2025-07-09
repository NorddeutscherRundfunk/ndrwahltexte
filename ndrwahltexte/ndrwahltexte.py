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

def load_file(FILENAME):
    with open(FILENAME) as f:
        file_data = json.load(f)
    log.info('file loaded successfully')
    return file_data

def load_election_data(FILENAME):
    file_data = load_file(ELECTION_FILE)
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
    except:
        log.err('there was a problem with the election data')
        return None

def analyse_election_data(FILENAME):
    election_data, results_data, candidate_df = load_election_data(FILENAME)
    erg_dict = {'ortsname' : election_data['gks_name'].split(',')[0],
            'gewinner_partei': candidate_df.at[0,'partei'],
           'gewinner_prozent' : candidate_df.at[0,'prozent'],
            'zweite_partei': candidate_df.at[1,'partei'],
           'zweite_prozent' : candidate_df.at[1,'prozent'],
           }
    log.info('election data analysed successfully')
    return erg_dict

def write_election_text(FILENAME):
    erg_dict = analyse_election_data(FILENAME)
    satz1 = "Bei der niedersächsischen Kommunalwahl 2026 in {ort} gingen die meisten Zweitstimmen an {gewinner_partei}.".format(ort = erg_dict['ortsname'], gewinner_partei = PARTEI_GRAMMATIK.at[erg_dict['gewinner_partei'],'Artikel NomSin + Parteiname'])
    text = satz1
    return text

def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", required = True, dest="filename",
                    help="election file", metavar="FILE")
    
    parser.add_argument("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="print status messages to stdout")
    
    args = parser.parse_args()
    
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")
    
    ELECTION_FILE = args.filename
    print(write_election_text(ELECTION_FILE))
    
    log.info('ndrwahltexte.py done')

#%% hier startet das Hauptprogramm
if __name__ == "__main__":
    main()

# %%
