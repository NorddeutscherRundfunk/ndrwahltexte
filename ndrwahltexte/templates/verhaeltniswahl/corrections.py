"""
Corrections specific to Verhältniswahl templates.
Handles German party name grammar (articles, cases).
"""

from ..parties import PARTEIEN, PARTEI_NAMEN, DATIV_FORMS, PLURAL_PARTEIEN

# === Article Mapping ===
ARTICLES = {
    'nominative': {
        'maskulin': 'der',
        'feminin': 'die',
        'neutrum': 'das',
        'plural': 'die'
    },
    'accusative': {
        'maskulin': 'den',
        'feminin': 'die',
        'neutrum': 'das',
        'plural': 'die'
    },
    'dative': {
        'maskulin': 'dem',
        'feminin': 'der',
        'neutrum': 'dem',
        'plural': 'den'
    }
}

# === Prepositions that trigger specific cases ===
PREPOSITIONS = {
    'accusative': ['für', 'durch', 'gegen', 'ohne', 'um', 'an'],
    'dative': ['vor', 'mit', 'bei', 'nach', 'zu', 'von', 'aus', 'seit']
}


def build_nominative_corrections(template_scope):
    """
    Build nominative case corrections (standalone patterns only).

    Nominative is the only case that appears without a preposition,
    so only nominative gets standalone patterns.

    Args:
        template_scope: List of nominative template keys

    Returns:
        dict: Nominative correction patterns
    """
    corrections = {}
    article = ARTICLES['nominative']

    # Handle regular genders
    for gender in ['maskulin', 'feminin', 'neutrum']:
        if gender not in PARTEIEN or not PARTEIEN[gender]:
            continue

        parties = PARTEIEN[gender]
        gender_article = article[gender]
        party_pattern = '|'.join(parties)

        # Standalone pattern (only for nominative)
        corrections[rf'\b({party_pattern})\b'] = {
            "replacement": rf"{gender_article} \1",
            "applies_to": template_scope
        }

    # Handle plural gender with special declension handling
    if 'plural' in PARTEIEN and PARTEIEN['plural']:
        parties = PARTEIEN['plural']
        gender_article = article['plural']

        for party in parties:
            declined_form = PLURAL_PARTEIEN[party]
            corrections[rf'\b{party}\b'] = {
                    "replacement": f"{gender_article} {declined_form}",
                    "applies_to": template_scope
                }

    # Handle "mit Partei davor" category
    if 'mit_partei_davor' in PARTEIEN and PARTEIEN['mit_partei_davor']:
        for partei_key in PARTEIEN['mit_partei_davor']:
            partei_name = PARTEI_NAMEN[partei_key]

            corrections[rf'\b{partei_key}\b'] = {
                "replacement": f"die Partei {partei_name}",
                "applies_to": template_scope
            }

    return corrections


def build_preposition_corrections(case):
    """
    Build preposition-based corrections for accusative and dative.

    These patterns match "preposition + party" and apply the correct
    case-specific article. They apply to ALL templates as a failsafe.

    Args:
        case: 'accusative' or 'dative'

    Returns:
        dict: Preposition-based correction patterns
    """
    corrections = {}
    prepositions = PREPOSITIONS.get(case, [])
    article = ARTICLES[case]

    # Handle regular genders
    for gender in ['maskulin', 'feminin', 'neutrum']:
        if gender not in PARTEIEN or not PARTEIEN[gender]:
            continue

        parties = PARTEIEN[gender]
        gender_article = article[gender]
        party_pattern = '|'.join(parties)

        for prep in prepositions:
            corrections[rf'(?i)\b{prep} ({party_pattern})\b'] = {
                "replacement": rf"{prep} {gender_article} \1",
                "applies_to": None
            }

    # Handle plural gender with special declension
    if 'plural' in PARTEIEN and PARTEIEN['plural']:
        parties = PARTEIEN['plural']
        gender_article = article['plural']

        for party in parties:
            declined_form = PLURAL_PARTEIEN[party]

            for prep in prepositions:
                corrections[rf'(?i)\b{prep} {party}\b'] = {
                    "replacement": f"{prep} {gender_article} {declined_form}",
                    "applies_to": None
                }

    # Handle "mit Partei davor" category
    if 'mit_partei_davor' in PARTEIEN and PARTEIEN['mit_partei_davor']:
        for partei_key in PARTEIEN['mit_partei_davor']:
            partei_name = PARTEI_NAMEN[partei_key]

            if case == 'accusative':
                gender_article = 'die'
            else:  # dative
                gender_article = 'der'

            for prep in prepositions:
                corrections[rf'(?i)\b{prep} {partei_key}\b'] = {
                    "replacement": f"{prep} {gender_article} Partei {partei_name}",
                    "applies_to": None
                }

    return corrections


def build_verhaeltniswahl_corrections(template_keys):
    """
    Build corrections specific to Verhältniswahl templates.

    Strategy:
    1. Nominative: Standalone patterns (scoped to nominative templates)
       - Uses declined forms for plural parties (Grüne → die Grünen)
    2. Accusative/Dative: ONLY preposition-based patterns (universal)
       - Also uses declined forms for plural parties

    This prevents case conflicts in mixed templates like "akkusativ_dativ".

    Args:
        template_keys: List of template keys to determine applies_to scope

    Returns:
        dict: All correction patterns for Verhältniswahl
    """
    corrections = {}

    # Identify nominative templates
    nominativ_templates = [k for k in template_keys if 'nominativ' in k]

    # Build corrections
    corrections.update(build_nominative_corrections(nominativ_templates))
    corrections.update(build_preposition_corrections('accusative'))
    corrections.update(build_preposition_corrections('dative'))

    return corrections