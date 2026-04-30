"""
Template loader with convention-based auto-loading.
Automatically merges corrections from three layers:
  1. Shared corrections (all elections)
  2. Wahlart-level corrections (e.g., Verhältniswahl)
  3. Template-level corrections (specific template file)
"""

import importlib
import sys
from .shared_corrections import build_shared_corrections
from ..utils import write_error


def load_for(wahlart, ergebnis_art):
    """
    Auto-load templates and corrections by convention.

    Args:
        wahlart: Election type (e.g., 'Verhältniswahl', 'Mehrheitswahl')
        ergebnis_art: Result type (e.g., 'Kein Ergebnis', 'Vorläufiges Endergebnis')

    Returns:
        dict: {'templates': dict, 'corrections': dict}

    Raises:
        Writes error to stderr and exits on failure
    """
    # Normalize names to module names
    wahlart_module = wahlart.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')

    # Convention: "Kein Ergebnis" → kein_ergebnis, others → mit_ergebnis
    if ergebnis_art == 'Kein Ergebnis':
        ergebnis_module = 'kein_ergebnis'
    elif 'Endergebnis' in ergebnis_art:
        ergebnis_module = 'endergebnis'
    elif 'Zwischenergebnis' in ergebnis_art:
        ergebnis_module = 'zwischenergebnis'

    module_path = f'ndrwahltexte.templates.{wahlart_module}.{ergebnis_module}'
    corrections_path = f'ndrwahltexte.templates.{wahlart_module}.corrections'

    try:
        # Load templates
        templates_mod = importlib.import_module(module_path)
        templates = templates_mod.TEMPLATES

        # Layer 1: Shared corrections (apply to all)
        corrections = build_shared_corrections()

        # Layer 2: Wahlart-level corrections
        try:
            corrections_mod = importlib.import_module(corrections_path)
            wahlart_corrections = corrections_mod.build_verhaeltniswahl_corrections(templates.keys())
            corrections.update(wahlart_corrections)
        except (ImportError, AttributeError) as e:
            # No wahlart-level corrections defined - that's okay, continue
            pass

        # Layer 3: Template-level corrections (optional)
        if hasattr(templates_mod, 'LOCAL_CORRECTIONS'):
            corrections.update(templates_mod.LOCAL_CORRECTIONS)

        return {
            'templates': templates,
            'corrections': corrections,
        }

    except ImportError as e:
        error = ValueError(
            f"Missing templates for {wahlart}/{ergebnis_art}.\n"
            f"Expected file: templates/{wahlart_module}/{ergebnis_module}.py\n"
            f"Error: {e}"
        )
        write_error(error)
        sys.exit(1)
    except Exception as e:
        write_error(e)
        sys.exit(1)