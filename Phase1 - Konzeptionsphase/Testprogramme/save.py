import json

daten = {
    "ects": 5,
    "bestanden": True
}

# In JSON Datei schreiben
with open("daten.json", "w", encoding = "utf-8") as datei:
    json.dump(daten, datei, indent = 4, ensure_ascii = False)

print("Gespeichert!")

#Aus Datei lesen
with open("daten.json", "r", encoding="utf-8") as datei:
    geladene_daten = json.load(datei)

for x, y in geladene_daten.items():
    print(f"{x}: {y}")