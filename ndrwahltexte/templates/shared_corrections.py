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

    # === NUMBER FORMATTING: Add . between thousands ===
    def format_german_number(m):
        num = m.group(1)
        return f"{int(num):,}".replace(",", ".")

    corrections[r'\b(\d{5,})\b'] = {
        "replacement": format_german_number,
        "applies_to": None
    }

    return corrections