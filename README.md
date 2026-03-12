# Risikoakte-Generator (MVP)

Python-MVP zur automatischen Erstellung eines **Risikoakte-Entwurfs** für Elektromedizinprodukte auf Basis eines Produkt-Informationsdokuments.

## Architekturüberblick

1. **Parser (`parser.py`)**
   - Liest `.txt`, `.md`, `.docx`, `.pdf`.
   - PDF ist optional (`pypdf`).
2. **Information Extraction (`extractor.py`)**
   - Struktur-/Regex-basierte Extraktion zentraler Produktinformationen.
   - Kennzeichnet fehlende Pflichtangaben mit Warnungen.
3. **Risk Engine (`risk_engine.py`)**
   - Regelbasierte Heuristik für Gefährdungen (ISO-14971-orientiert).
   - Trennung von Herkunft: extrahiert/abgeleitet/generisch.
4. **Template Generator (`template_generator.py`)**
   - Erzeugt strukturierte Risikoakte inkl. Risikomatrix als Markdown.
5. **Exporter (`exporter.py`)**
   - Schreibt Risikoakte als Markdown und Risikomatrix als CSV.
6. **CLI (`cli.py`)**
   - End-to-end-Ausführung mit Logging.

## Projektstruktur

```text
src/risk_akte_tool/
  __init__.py
  cli.py
  exporter.py
  extractor.py
  models.py
  parser.py
  risk_engine.py
  template_generator.py
examples/
  sample_product_info.md
tests/
  test_extractor.py
  test_risk_engine.py
  test_template.py
output/
```

## Start

```bash
python -m pip install -e .
risk-akte examples/sample_product_info.md --output-dir output
```

Erzeugte Dateien:
- `output/risikoakte.md`
- `output/risikomatrix.csv`

## Regulatory-/QM-Review (zwingend)

Das Tool erstellt **nur einen Entwurf**. Mindestens folgende Punkte benötigen menschlichen Review/Freigabe:
- Zweckbestimmung und klinischer Kontext.
- Vollständigkeit von Gefährdungen, Ereignisabfolgen, Schäden.
- S/P-Bewertungsmaßstab und Akzeptanzkriterien.
- Wirksamkeit/Nachweis der Maßnahmen (Test, Inspektion, Analyse).
- Restrisikobeurteilung inkl. Benefit-Risk.
- Normative Zuordnung (u. a. ISO 14971, IEC 60601-1/-1-2, IEC 62304, IEC 62366-1).

## Hinweise

- Keine automatische finale regulatorische Entscheidung.
- Fehlende oder uneindeutige Daten werden als „manuelle Bewertung erforderlich“ markiert.
- Regelbasis ist erweiterbar (weitere Normen/Produktklassen).
