# Produkt-Informationsdokument

Produktname:
CardioGuard CGM-200

Produktkategorie:
Mobiles Patientenmonitoring-System

Intended Use:
Das System dient zur kontinuierlichen Überwachung von Herzfrequenz, SpO2 und nichtinvasivem Blutdruck bei erwachsenen Patienten auf Normalstationen und in der Notaufnahme.

Anwendergruppen:
- Pflegefachkräfte
- Ärztliches Personal

Patientengruppen:
- Erwachsene
- Kreislaufinstabile Patienten

Einsatzumgebung:
- Krankenhausstation
- Notaufnahme

Funktionsbeschreibung:
Das Gerät erfasst Vitalparameter über angeschlossene Sensoren und zeigt Grenzwertüberschreitungen akustisch und visuell an.

Software:
- Embedded Firmware für Signalverarbeitung
- Alarm-Engine mit Priorisierung
- Netzwerkmodul für HL7-Export

Schnittstellen:
- Ethernet
- USB-Serviceport
- HL7 über TCP/IP

Warnhinweise:
- Nicht in MRI-Umgebung einsetzen.
- Alarmgrenzen patientenspezifisch einstellen.

Bekannte Restrisiken:
- Kurzzeitiger Signalverlust bei Bewegung.

Schutzmaßnahmen:
- Schutzerdung am Netzteil
- Watchdog für Softwareprozess
- Akku-Puffer bei Netzausfall
