########################
#
# Dieses Script enthält Projekt-Variablen für ndrwahltexte
# Ersetzt parteigrammatik.csv durch regex-basierte Korrekturen
# -> l.sander.fm@ndr.de 
# 
#########################
import re

# Parteien nach grammatischem Geschlecht gruppiert
PLURAL_PARTEIEN = {
    'Grüne': 'Grünen',
}

PARTEIEN = {
    'feminin': ['SPD', 'CDU', 'AfD', 'FDP', 'CSU', 'MLPD', 'Tierschutzpartei', 'Linke'],
    'neutrum': ['BSW', 'Bündnis Deutschland'],
    'maskulin': [],
    'mit_partei_davor': ['Volt', 'dieBasis LV', 'FW-PB'],  # FW-PB = "die Partei Freie Wähler",
    'plural': list(PLURAL_PARTEIEN.keys()),
}

DATIV_FORMS = {
               'Linke': 'Linken',
}

# Partei-Namen für "mit Partei davor" Kategorie
PARTEI_NAMEN = {
    'Volt': 'Volt',
    'dieBasis LV': 'dieBasis',
    'FW-PB': 'Freie Wähler',
}

# Pronomen für Parteien (Sie/Er/Es)
PARTEI_PRONOMEN = {}
for partei in PARTEIEN['neutrum']:
    PARTEI_PRONOMEN[partei] = 'Es'
for partei in PARTEIEN['maskulin']:
    PARTEI_PRONOMEN[partei] = 'Er'
for partei in PARTEIEN['feminin'] + PARTEIEN['mit_partei_davor']:
    PARTEI_PRONOMEN[partei] = 'Sie'
# Add plural parties
for partei in PARTEIEN['plural']:
    PARTEI_PRONOMEN[partei] = 'Sie'