"""
Shared corrections that apply across all election types.
Mainly number formatting and common German grammar rules.
"""


def build_shared_corrections():
    """Build corrections that apply to all templates across all election types."""
    corrections = {}

    # === NUMBER FORMATTING: remove trailing .0 ===
    corrections[r'\b(\d+)\.0\b'] = {
        "replacement": r"\1",
        "applies_to": None  # None means applies to ALL templates
    }

    # === NUMBER FORMATTING: Decimal point to comma ===
    corrections[r'\b(\d+)\.(\d+)\b'] = {
        "replacement": r"\1,\2",
        "applies_to": None
    }

    # === CAPITALIZATION: Die Linke ===
    corrections[r'\bdie Linke\b'] = {
        "replacement": "Die Linke",
        "applies_to": None  # Apply to all templates
    }

    corrections[r'\bder Linken\b'] = {
        "replacement": "Der Linken",
        "applies_to": None  # Apply to all templates
    }

    # === LOCATION: in Kreis → im Kreis ===
    corrections[r'\b([iI])n Kreis\b'] = {
        "replacement": r"\1m Kreis",
        "applies_to": None
    }

    # === COUNTING: von 1 von → von einem von ===
    corrections[r'Auszählung von 1 von'] = {
        "replacement": "Auszählung von einem von",
        "applies_to": None
    }

    # === CAPITALIZATION: Sentence starts after period ===
    def capitalize_after_period(match):
        return '. ' + match.group(1).upper()

    corrections[r'\. ([a-zäöü])'] = {
        "replacement": capitalize_after_period,
        "applies_to": None
    }

    # === NUMBER FORMATTING: Add . between thousands ===
    def format_german_number(m):
        num = m.group(1)
        return f"{int(num):,}".replace(",", ".")

    corrections[r'\b(\d{5,})\b'] = {
        "replacement": format_german_number,
        "applies_to": None
    }

    return corrections