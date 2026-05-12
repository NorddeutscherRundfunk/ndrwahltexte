"""
Corrections specific to German party name grammar (articles, cases).
"""

from .parties import PARTEIEN, PARTEI_NAMEN, DATIV_FORMS, PLURAL_PARTEIEN

# === Article Mapping ===
ARTICLES = {
    'nominativ': {
        'maskulin': 'der',
        'feminin': 'die',
        'neutrum': 'das',
        'plural': 'die'
    },
    'akkusativ': {
        'maskulin': 'den',
        'feminin': 'die',
        'neutrum': 'das',
        'plural': 'die'
    },
    'dativ': {
        'maskulin': 'dem',
        'feminin': 'der',
        'neutrum': 'dem',
        'plural': 'den'
    }
}

# === Prepositions that trigger specific cases ===
PREPOSITIONS = {
    'akkusativ': ['für', 'durch', 'gegen', 'ohne', 'um', 'an'],
    'dativ': ['vor', 'mit', 'bei', 'nach', 'zu', 'von', 'aus', 'seit']
}


def get_templates_by_case(templates, case):
    """
    Extract template keys that contain a specific grammatical case.

    Args:
        templates: Dict of templates with their metadata
        case: 'nominativ', 'akkusativ', or 'dativ'

    Returns:
        list: Template keys containing the specified case
    """
    return [
        key for key, template in templates.items()
        if case in template.get('grammar', [])
    ]


def build_nominative_corrections(scoped_templates):
    """
    Build nominative case corrections (standalone patterns only).

    Args:
        scoped_templates: List of template keys for nominative scope

    Returns:
        dict: Nominative correction patterns
    """
    corrections = {}

    if not scoped_templates:
        return corrections

    article = ARTICLES['nominativ']

    # Handle regular genders
    for gender in ['maskulin', 'feminin', 'neutrum']:
        if gender not in PARTEIEN or not PARTEIEN[gender]:
            continue

        parties = PARTEIEN[gender]
        gender_article = article[gender]
        party_pattern = '|'.join(parties)

        corrections[rf'\b({party_pattern})\b'] = {
            "replacement": rf"{gender_article} \1",
            "applies_to": scoped_templates
        }

    # Handle plural gender with special declension
    if 'plural' in PARTEIEN and PARTEIEN['plural']:
        parties = PARTEIEN['plural']
        gender_article = article['plural']

        for party in parties:
            declined_form = PLURAL_PARTEIEN[party]
            corrections[rf'\b{party}\b'] = {
                "replacement": f"{gender_article} {declined_form}",
                "applies_to": scoped_templates
            }

    # Handle "mit Partei davor" category
    if 'mit_partei_davor' in PARTEIEN and PARTEIEN['mit_partei_davor']:
        for partei_key in PARTEIEN['mit_partei_davor']:
            partei_name = PARTEI_NAMEN[partei_key]

            corrections[rf'\b{partei_key}\b'] = {
                "replacement": f"die Partei {partei_name}",
                "applies_to": scoped_templates
            }

    return corrections


def build_preposition_corrections(case, scoped_templates):
    """
    Build preposition-based corrections for accusative and dative.

    Args:
        case: 'akkusativ' or 'dativ'
        scoped_templates: List of template keys for this case's scope

    Returns:
        dict: Preposition-based correction patterns
    """
    corrections = {}

    if not scoped_templates:
        return corrections

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
                "applies_to": scoped_templates
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
                    "applies_to": scoped_templates
                }

    # Handle "mit Partei davor" category
    if 'mit_partei_davor' in PARTEIEN and PARTEIEN['mit_partei_davor']:
        for partei_key in PARTEIEN['mit_partei_davor']:
            partei_name = PARTEI_NAMEN[partei_key]

            if case == 'akkusativ':
                gender_article = 'die'
            else:  # dativ
                gender_article = 'der'

            for prep in prepositions:
                corrections[rf'(?i)\b{prep} {partei_key}\b'] = {
                    "replacement": f"{prep} {gender_article} Partei {partei_name}",
                    "applies_to": scoped_templates
                }

    return corrections


def build_party_corrections(templates):
    """
    Build all party grammar corrections.

    Strategy:
    1. Extract template scopes for each case from grammar metadata
    2. Nominative: Standalone patterns (scoped)
    3. Akkusativ/Dativ: Preposition-based patterns (scoped)

    Args:
        templates: Dict of all templates with their metadata

    Returns:
        dict: All party grammar correction patterns
    """
    corrections = {}

    # Extract scopes once for all cases
    nominativ_templates = get_templates_by_case(templates, 'nominativ')
    akkusativ_templates = get_templates_by_case(templates, 'akkusativ')
    dativ_templates = get_templates_by_case(templates, 'dativ')

    # Build corrections
    corrections.update(build_nominative_corrections(nominativ_templates))
    corrections.update(build_preposition_corrections('akkusativ', akkusativ_templates))
    corrections.update(build_preposition_corrections('dativ', dativ_templates))

    # === CAPITALIZATION: Die Linke ===
    corrections[r'\bdie Linke\b'] = {
        "replacement": "Die Linke",
        "applies_to": None
    }

    corrections[r'\bder Linken\b'] = {
        "replacement": "Der Linken",
        "applies_to": None
    }

    return corrections