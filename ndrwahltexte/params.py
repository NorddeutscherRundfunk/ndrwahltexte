########################
#
# Dieses Script enthält Projekt-Variablen für ndrwahltexte
# Ersetzt parteigrammatik.csv durch regex-basierte Korrekturen
# -> l.sander.fm@ndr.de 
# 
#########################

# Templates für Wahltexte
# Jedes Template verwendet Parteinamen im Rohformat (z.B. "SPD", "Grüne")
# Die Korrekturen fügen die grammatisch korrekten Artikel hinzu

TEMPLATES = {
    "titel": {
        "topic": "ergebnis",
        "text": "In {ortsname} gingen die meisten Zweitstimmen an {gewinner_partei}."
    }
}

# Korrekturen für grammatisch korrekte Parteinamen
# Der Satz "...gingen an {partei}" erfordert Akkusativ
# applies_to: ["titel"] stellt sicher, dass nur dieses Template betroffen ist

CORRECTIONS = {
    # Feminine Parteien (die meisten): "an die ..."
    r"\ban SPD\b": {
        "replacement": "an die SPD",
        "applies_to": ["titel"]
    },
    r"\ban CDU\b": {
        "replacement": "an die CDU",
        "applies_to": ["titel"]
    },
    r"\ban AfD\b": {
        "replacement": "an die AfD",
        "applies_to": ["titel"]
    },
    r"\ban FDP\b": {
        "replacement": "an die FDP",
        "applies_to": ["titel"]
    },
    r"\ban MLPD\b": {
        "replacement": "an die MLPD",
        "applies_to": ["titel"]
    },
    r"\ban Tierschutzpartei\b": {
        "replacement": "an die Tierschutzpartei",
        "applies_to": ["titel"]
    },
    
    # Pluralformen: "an die ..."
    r"\ban Grüne\b": {
        "replacement": "an die Grünen",
        "applies_to": ["titel"]
    },
    r"\ban Linke\b": {
        "replacement": "an Die Linke",
        "applies_to": ["titel"]
    },
    
    # Wählergemeinschaften mit "Freie": "an die Freien ..."
    r"\ban FW-PB\b": {
        "replacement": "an die Freien Wähler",
        "applies_to": ["titel"]
    },
    
    # Parteien mit "Partei" davor: "an die Partei ..."
    r"\ban Volt\b": {
        "replacement": "an die Partei Volt",
        "applies_to": ["titel"]
    },
    r"\ban dieBasis LV\b": {
        "replacement": "an die Partei dieBasis",
        "applies_to": ["titel"]
    },
    
    # Neutrum Parteien: "an das ..."
    r"\ban BSW\b": {
        "replacement": "an das BSW",
        "applies_to": ["titel"]
    },
    r"\ban Bündnis Deutschland\b": {
        "replacement": "an das Bündnis Deutschland",
        "applies_to": ["titel"]
    },
}