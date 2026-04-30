########################
#
# Election Data Parser
# Functions for parsing and extracting election data
# -> l.sander.fm@ndr.de
#
#########################

import pandas as pd
import sys
from typing import Dict, Any, Optional, Tuple
from .templates.parties import PARTEI_PRONOMEN
from .utils import write_error


def parse_election_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse raw election JSON and return template variables.

    Args:
        raw_data: Dictionary containing 'wahl' key with election data

    Returns:
        dict: All variables needed for templates
    """
    try:
        wahl = raw_data.get('wahl', {})

        # Extract election metadata (without nested structures)
        election_data = {k: v for k, v in wahl.items()
                         if k not in ['ergebnis', 'kandidaten']}

        # Extract results data
        results_data = wahl.get('ergebnis', {})

        # Build candidate dataframe
        candidate_data = results_data.get('kandidaten', [])
        candidate_ref = wahl.get('kandidaten', [])

        candidate_df = pd.DataFrame(candidate_data).merge(
            pd.DataFrame(candidate_ref),
            on=['kandidatur_id', 'pos'],
            how='left'
        )
        candidate_df = candidate_df.sort_values(
            'prozent', ascending=False
        ).reset_index(drop=True)

    except Exception as e:
        write_error(e)
        sys.exit(1)

    # Extract party data
    gewinner_partei, gewinner_prozent = _get_party_at(candidate_df, 0)
    zweite_partei, zweite_prozent = _get_party_at(candidate_df, 1)
    dritte_partei, dritte_prozent = _get_party_at(candidate_df, 2)
    vierte_partei, vierte_prozent = _get_party_at(candidate_df, 3)
    fuenfte_partei, fuenfte_prozent = _get_party_at(candidate_df, 4)

    # Extract basic metadata
    name = election_data.get('gks_name', '').split(',')[0]

    # Build variables dict - single source of truth
    return {
        'ortsname': name,
        'name': name,
        'wahlart': election_data.get('wahlart'),
        'wahlorgan': election_data.get('organ'),
        'ergebnis_art': results_data.get('ergebnis_art'),
        'anz_wahlbereiche': election_data.get('anz_wahlbereiche'),
        'gez_wahlbereiche': results_data.get('gez_wahlbereiche'),
        'num_parties': len(candidate_df),
        'wahlberechtigte': election_data.get('anz_wahlberechtigte'),
        'wahlbeteiligung': results_data.get('wahlbeteil'),
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


def _get_party_at(df: pd.DataFrame, index: int) -> Tuple[Optional[str], Optional[float]]:
    """
    Safely extract party and percentage from dataframe at given index.

    Args:
        df: Candidate dataframe sorted by percentage
        index: Row index

    Returns:
        tuple: (partei, prozent) or (None, None) if index doesn't exist
    """
    if index < len(df):
        return df.at[index, 'partei'], float(df.at[index, 'prozent'])
    return None, None