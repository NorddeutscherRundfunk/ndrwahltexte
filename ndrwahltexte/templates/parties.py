########################
#
# Dieses Script enthält Projekt-Variablen für ndrwahltexte
# Ersetzt parteigrammatik.csv durch regex-basierte Korrekturen
# -> l.sander.fm@ndr.de 
# 
#########################
import re

# Parteien nach grammatischem Geschlecht gruppiert
PARTEIEN = {
    'feminin': ['SPD', 'CDU', 'AfD', 'FDP', 'CSU', 'MLPD', 'Tierschutzpartei'],
    'neutrum': ['BSW', 'Bündnis Deutschland'],
    'mit_partei_davor': ['Volt', 'dieBasis LV', 'FW-PB'],  # FW-PB = "die Partei Freie Wähler"
}

# Spezielle Pluralformen
PLURAL_PARTEIEN = {
    'Grüne': 'Grünen',
    'Linke': 'Linken',
}

# Partei-Namen für "mit Partei davor" Kategorie
PARTEI_NAMEN = {
    'Volt': 'Volt',
    'dieBasis LV': 'dieBasis',
    'FW-PB': 'Freie Wähler',
}

# Pronomen für Parteien (Sie/Er/Es)
PARTEI_PRONOMEN = {
    'SPD': 'Sie',
    'CDU': 'Sie',
    'AfD': 'Sie',
    'FDP': 'Sie',
    'Grüne': 'Sie',
    'Linke': 'Sie',
    'BSW': 'Es',
    'CSU': 'Sie',
    'FW-PB': 'Sie',
    'Volt': 'Sie',
    'dieBasis LV': 'Sie',
    'MLPD': 'Sie',
    'Tierschutzpartei': 'Sie',
    'Bündnis Deutschland': 'Es',
}