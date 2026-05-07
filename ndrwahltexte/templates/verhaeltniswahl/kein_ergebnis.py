"""
Templates for Verhältniswahl with no result data available.
(Only results with "Kein Ergebnis")
"""

TEMPLATES = {
    # === TITEL ===
    "titel_kein_ergebnis": {
        "topic": "ergebnis",
        "conditions": [],
        "text": "{name}: Noch kein Ergebnis bei {wahlorgan}swahl"
    },

    # === ABSATZ1 ===
    "absatz1_kein_ergebnis": {
        "topic": "absatz1",
        "conditions": [],
        "text": "Für die {wahlorgan}swahl in {name} gibt es noch kein Ergebnis."
    },

    # === WAHLBETEILIGUNG ===
    "absatz1_wahlberechtigte": {
        "topic": "absatz1",
        "conditions": [],
        "text": "In {name} leben {wahlberechtigte} Wahlberechtigte."
    },
}

# Optional: Template-specific corrections (rarely needed)
# These only apply to templates in THIS file
LOCAL_CORRECTIONS = {
    # Example: Fix a specific typo only in these templates
    # r'Zweitstimme\b': {
    #     "replacement": "Zweitstimmen",
    #     "applies_to": ["absatz1_gleichauf"]
    # }
}