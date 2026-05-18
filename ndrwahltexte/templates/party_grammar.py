"""
Corrections specific to German party name grammar (articles, cases).
"""
import re
from .parties import PARTEIEN, PARTEI_NAMEN, PLURAL_PARTEIEN

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

# === VERB CONJUGATION: Singular 3rd person → Plural forms ===
VERB_CORRECTIONS = {
    # sein
    'ist': 'sind',
    # haben
    'hat': 'haben',
    # position verbs
    'liegt': 'liegen',
    'steht': 'stehen',
    'kommt': 'kommen',
    'gewinnt': 'gewinnen',
    'verliert': 'verlieren',
    # action verbs
    'führt': 'führen',
    'erreicht': 'erreichen',
    'erhält': 'erhalten',
    'bekommt': 'bekommen',
    'holt': 'holen',
    'geht': 'gehen',
    'bleibt': 'bleiben',
    'zieht': 'ziehen',
    'schneidet': 'schneiden',
    'landet': 'landen',
    'folgt': 'folgen',
    # Add more as needed
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


def build_all_party_names_pattern():
    """
    Build a regex pattern matching all known party names.
    Used for negative lookahead to avoid incorrect verb corrections.

    Returns:
        str: Regex pattern matching any party name
    """
    all_parties = []

    # Collect all party names from all categories
    for gender in ['feminin', 'neutrum', 'maskulin']:
        if gender in PARTEIEN:
            all_parties.extend(PARTEIEN[gender])

    # Add plural parties
    if 'plural' in PARTEIEN:
        all_parties.extend(PARTEIEN['plural'])

    # Add declined forms for plural parties
    all_parties.extend(PLURAL_PARTEIEN.values())

    # Add special parties (mit_partei_davor)
    if 'mit_partei_davor' in PARTEIEN:
        all_parties.extend(PARTEIEN['mit_partei_davor'])
        # Also add their full forms
        all_parties.extend(PARTEI_NAMEN.values())

    # Escape special regex characters and join
    escaped_parties = [re.escape(party) for party in all_parties]
    return '|'.join(escaped_parties)


def build_plural_party_verb_corrections(plural_parties):
    """
    Build verb agreement corrections for plural party names.

    Allows multiple words between verb and party name, but excludes
    patterns where another party name appears in between (which would
    indicate the verb belongs to a different subject).

    Args:
        plural_parties: List of party names requiring plural verbs

    Returns:
        dict: Correction patterns for verb agreement
    """
    corrections = {}

    # Build exclusion pattern for all party names
    party_exclusion = build_all_party_names_pattern()

    for party in plural_parties:
        declined_form = PLURAL_PARTEIEN[party]

        for singular_verb, plural_verb in VERB_CORRECTIONS.items():
            # Direct adjacency: "Grüne liegt"
            corrections[rf'\b{party} {singular_verb}\b'] = {
                "replacement": f"{party} {plural_verb}",
                "applies_to": None
            }

            # Direct adjacency: "liegt Grüne"
            corrections[rf'\b{singular_verb} {party}\b'] = {
                "replacement": f"{plural_verb} {party}",
                "applies_to": None
            }

            # Direct adjacency: "die Grünen liegt"
            corrections[rf'\bdie {declined_form} {singular_verb}\b'] = {
                "replacement": f"die {declined_form} {plural_verb}",
                "applies_to": None
            }

            # Direct adjacency: "liegt die Grünen"
            corrections[rf'\b{singular_verb} die {declined_form}\b'] = {
                "replacement": f"{plural_verb} die {declined_form}",
                "applies_to": None
            }

            # Flexible pattern: "führt nach Auszählung von 29 von 58 Wahlbereichen derzeit die Grünen"
            # Capture the intervening words in group 1
            corrections[
                rf'\b{singular_verb}\s+((?:(?!(?:{party_exclusion})\b)\S+\s+){{1,10}})die {declined_form}\b'] = {
                "replacement": rf"{plural_verb} \1die {declined_form}",
                "applies_to": None
            }

            # Reverse: "die Grünen derzeit liegt"
            # Capture the intervening words in group 1
            corrections[rf'\bdie {declined_form}\s+((?:(?!(?:{party_exclusion})\b)\S+\s+){{1,5}}){singular_verb}\b'] = {
                "replacement": rf"die {declined_form} \1{plural_verb}",
                "applies_to": None
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
    corrections.update(build_plural_party_verb_corrections(PLURAL_PARTEIEN.keys()))

    # === CAPITALIZATION: Die Linke ===
    corrections[r'\bdie Linke\b'] = {
        "replacement": "Die Linke",
        "applies_to": None
    }

    corrections[r'\bder Linke\b'] = {
        "replacement": "Der Linken",
        "applies_to": None
    }

    return corrections