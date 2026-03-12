# Risikoakte-Entwurf für Elektromedizinprodukt

## 1. Produktidentifikation
- Produkt: CardioGuard CGM-200

## 2. Zweckbestimmung
- Das System dient zur kontinuierlichen Überwachung von Herzfrequenz, SpO2 und nichtinvasivem Blutdruck bei erwachsenen Patienten auf Normalstationen und in der Notaufnahme.

## 3. Annahmen und Eingangsdaten
- Risikokennzahlen (S/P) sind MVP-Startwerte und müssen projektspezifisch kalibriert werden.
- Die Anwendung erzeugt keinen regulatorischen Freigabeentscheid.

## 4. Liste identifizierter Gefährdungen
- R-001: Elektrischer Schlag (derived)
- R-002: Fehlalarm / ausbleibender Alarm (derived)
- R-003: Softwarefehler (derived)
- R-004: Ausfall Stromversorgung (derived)
- R-005: Datenintegritäts- oder Kommunikationsfehler (derived)
- R-006: Elektromagnetische Störung (generic)

## 5. Risikobewertung vor Maßnahmen
- Semiquantitative Bewertung via SxP-Regel (1-5) als Entwurfsstand.

## 6. Risikokontrollmaßnahmen
- Maßnahmenvorschläge aus Regelbasis; Wirksamkeit muss verifiziert werden.

## 7. Bewertung des Restrisikos
- Restrisiken sind nur vorläufig bewertet; Benefit-Risk Entscheidung durch Fachgremium.

## 8. Verifikation der Maßnahmen
- Verifikationsnachweise sind Platzhalter und müssen im V&V-Plan konkretisiert werden.

## 9. Offene Punkte / manueller Review erforderlich
- Keine

## 10. Warnungen

- Keine

## 11. Risikomatrix

| ID | Gefährdung | Ursache | Gefährdungssituation | möglicher Schaden | betroffene Person | S | P | Risiko vor Maßnahme | Maßnahme | Risiko nach Maßnahme | Restrisiko akzeptabel | Verweis auf Nachweis / Test / Dokument | Kommentar | Herkunft |
|---|---|---|---|---|---|---:|---:|---:|---|---:|---|---|---|---|
| R-001 | Elektrischer Schlag | Isolationsfehler oder defekte Schutzerdung | Patient oder Anwender berührt spannungsführende Teile | Stromschlag bis schwerer Verletzung | Patient/Anwender | 5 | 2 | 10 | Schutzisolation, Ableitstromprüfung, PE-Überwachung | 4 | Ja | IEC 60601-1 Sicherheitsprüfung | Heuristisch aus Dokumentinhalt abgeleitet. | Abgeleitet |
| R-002 | Fehlalarm / ausbleibender Alarm | Fehlkonfiguration, Sensorfehler oder SW-Defekt | Kritischer Zustand wird nicht oder falsch signalisiert | Behandlungsverzögerung | Patient | 5 | 3 | 15 | Alarm-Logik-Test, Prioritätskonzept, Human Factors Validierung | 8 | Nein | Alarm-Verifikationstest | Heuristisch aus Dokumentinhalt abgeleitet. | Abgeleitet |
| R-003 | Softwarefehler | Anforderungs- oder Implementierungsfehler | Steuerungslogik arbeitet außerhalb Spezifikation | Falscher Output / Unterbrechung | Patient/Anwender | 4 | 3 | 12 | SW-Lifecycle nach IEC 62304, Reviews, Unit/Integrationstests | 6 | Ja | Software V&V Bericht | Heuristisch aus Dokumentinhalt abgeleitet. | Abgeleitet |
| R-004 | Ausfall Stromversorgung | Energiequelle fällt aus | Gerät stoppt während Nutzung | Therapieunterbrechung | Patient | 4 | 2 | 8 | Akku-Management, Power-Fail Alarm, sichere Abschaltung | 3 | Ja | Betriebsdauertest / Fallback-Test | Heuristisch aus Dokumentinhalt abgeleitet. | Abgeleitet |
| R-005 | Datenintegritäts- oder Kommunikationsfehler | Datenverlust, Paketfehler, Mappingfehler | Falsche Patientendaten oder lückenhafte Trends | Fehlentscheidung | Patient | 4 | 2 | 8 | CRC/Checksummen, Interface-Protokolltests, Audit-Log | 3 | Ja | Integrationstest Schnittstellen | Heuristisch aus Dokumentinhalt abgeleitet. | Abgeleitet |
| R-006 | Elektromagnetische Störung | EMV-Störaussendung oder Störbeeinflussung | Fehlfunktion durch Störfelder | Falsche Therapie/Monitoring | Patient | 4 | 3 | 12 | EMV-Design, IEC 60601-1-2 Test, Abschirmung | 6 | Manuelle Bewertung erforderlich | EMV Prüfbericht | Generisches Basisrisiko für Elektromedizinprodukt. | Generisch |