"""
Verhältniswahl-specific corrections.

This module provides a hook for Verhältniswahl-specific text corrections
that aren't covered by party grammar or shared corrections.

Use this for corrections that:
- Only apply to Verhältniswahl templates
- Are specific to the election type logic (not party grammar)
- Need to override or supplement the standard correction layers

Example use cases:
- Verhältniswahl-specific terminology corrections
- Special handling for Zweitstimmen vs Erststimmen
- Organ-specific text corrections
"""


def build_verhaeltniswahl_corrections(template_keys):
    """
    Build Verhältniswahl-specific corrections.

    This function is called automatically by the template loader.
    Add corrections here that are specific to Verhältniswahl templates.

    Args:
        template_keys: List of template keys from the current template file

    Returns:
        dict: Correction patterns in the standard format:
        {
            r'pattern': {
                'replacement': 'text' or function,
                'applies_to': list of template keys or None for all
            }
        }

    Examples:
        # Fix Verhältniswahl-specific typo
        corrections[r'Zweitstimme\b'] = {
            'replacement': 'Zweitstimmen',
            'applies_to': ['absatz1_gewinner']
        }

        # Override party grammar for specific context
        corrections[r'Stadtrat\b'] = {
            'replacement': 'im Stadtrat',
            'applies_to': None
        }
    """
    corrections = {}

    # Add your Verhältniswahl-specific corrections here
    # Currently empty - party grammar and shared corrections handle everything

    return corrections