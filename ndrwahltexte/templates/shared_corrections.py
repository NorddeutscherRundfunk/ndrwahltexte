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

    # === LOCATION: in Kreis → im Kreis ===
    corrections[r'\b([iI])n ([A-Za-zÄÖÜäöüß]+[Kk]reis)\b'] = {
        "replacement": r"\1m \2",
        "applies_to": None
    } #applies to Kreis and Xyzkreis like Landkreis or Heidekreis

    corrections[r'\b([iI])n Region\b'] = {
        "replacement": r"\1n der Region",
        "applies_to": None
    }

    corrections[r'\b([iI])n Wesermarsch\b'] = {
        "replacement": r"\1n der Wesermarsch",
        "applies_to": None
    }

    corrections[r'\b([iI])n Grafschaft\b'] = {
        "replacement": r"\1n der Grafschaft",
        "applies_to": None
    }

    corrections[r'\b([iI])n Emsland\b'] = {
        "replacement": r"\1m Emsland",
        "applies_to": None
    }

    # === COUNTING: von 1 von → von einem von ===
    corrections[r'Auszählung von 1 von'] = {
        "replacement": "Auszählung von einem von",
        "applies_to": None
    }
    
    corrections[r'sind 1 von'] = {
        "replacement": "ist 1 von",
        "applies_to": None
    }

    # === CAPITALIZATION: Sentence starts after period ===
    def capitalize_after_period(match):
        return '. ' + match.group(1).upper()

    corrections[r'\. ([a-zäöü])'] = {
        "replacement": capitalize_after_period,
        "applies_to": None
    }

    # === CAPITALIZATION: Start of string ===
    def capitalize_start(match):
        return match.group(1).upper()

    corrections[r'^([a-zäöü])'] = {
        "replacement": capitalize_start,
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

    # === Miscellaneous spelling corrections ===
    corrections[r'Abgeordnetenhausswahl'] = {
        "replacement": "Abgeordnetenhauswahl",
        "applies_to": None
    }

    return corrections