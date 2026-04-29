########################
#
# Text Generator
# Functions for generating election text from variables
# -> l.sander.fm@ndr.de
#
#########################

from typing import Dict
from .robotext import TemplateEngine
from .templates import load_for


def generate_election_text(variables: Dict) -> Dict[str, str]:
    """
    Generate election text from template variables.

    Args:
        variables: Dictionary of election data variables

    Returns:
        dict: Dictionary with 'Titel' and 'Absatz1' keys, or 'error' key if generation failed
    """
    # Load templates and corrections based on election type
    config = load_for(variables['wahlart'], variables['ergebnis_art'])

    # Initialize template engine
    engine = TemplateEngine(
        templates=config['templates'],
        variables=variables,
        corrections=config['corrections']
    )

    # Generate title
    titel_selected = engine.select_templates(filter_topic="ergebnis")
    titel = engine.build_text(titel_selected)

    # Generate first paragraph
    absatz1_selected = engine.select_templates(filter_topic="absatz1")
    absatz1 = engine.build_text(absatz1_selected)

    # Validate output
    if not titel or not titel.strip() or not absatz1 or not absatz1.strip():
        return {
            'error': 'Für diese Daten konnte kein Wahltext geschrieben werden.'
        }

    return {
        'Titel': titel,
        'Absatz1': absatz1
    }