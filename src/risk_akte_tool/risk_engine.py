from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .models import EvidenceType, ExtractedInfo, RiskFile, RiskItem


@dataclass
class HazardRule:
    hazard: str
    triggers: List[str]
    cause: str
    hazardous_situation: str
    potential_harm: str
    default_affected_person: str
    base_severity: int
    base_probability: int
    control_measure: str
    verification_reference: str


HAZARD_RULES = [
    HazardRule("Elektrischer Schlag", ["spannung", "netzteil", "ac", "stromversorgung"], "Isolationsfehler oder defekte Schutzerdung", "Patient oder Anwender berührt spannungsführende Teile", "Stromschlag bis schwerer Verletzung", "Patient/Anwender", 5, 2, "Schutzisolation, Ableitstromprüfung, PE-Überwachung", "IEC 60601-1 Sicherheitsprüfung"),
    HazardRule("Elektromagnetische Störung", ["funk", "bluetooth", "wifi", "schnittstelle", "emv"], "EMV-Störaussendung oder Störbeeinflussung", "Fehlfunktion durch Störfelder", "Falsche Therapie/Monitoring", "Patient", 4, 3, "EMV-Design, IEC 60601-1-2 Test, Abschirmung", "EMV Prüfbericht"),
    HazardRule("Fehlalarm / ausbleibender Alarm", ["alarm", "warn"], "Fehlkonfiguration, Sensorfehler oder SW-Defekt", "Kritischer Zustand wird nicht oder falsch signalisiert", "Behandlungsverzögerung", "Patient", 5, 3, "Alarm-Logik-Test, Prioritätskonzept, Human Factors Validierung", "Alarm-Verifikationstest"),
    HazardRule("Softwarefehler", ["software", "update", "firmware"], "Anforderungs- oder Implementierungsfehler", "Steuerungslogik arbeitet außerhalb Spezifikation", "Falscher Output / Unterbrechung", "Patient/Anwender", 4, 3, "SW-Lifecycle nach IEC 62304, Reviews, Unit/Integrationstests", "Software V&V Bericht"),
    HazardRule("Ausfall Stromversorgung", ["akku", "batterie", "stromversorgung", "netz"], "Energiequelle fällt aus", "Gerät stoppt während Nutzung", "Therapieunterbrechung", "Patient", 4, 2, "Akku-Management, Power-Fail Alarm, sichere Abschaltung", "Betriebsdauertest / Fallback-Test"),
    HazardRule("Bedienfehler", ["anwender", "display", "bedien"], "Missverständliche UI oder unzureichende Schulung", "Falscher Modus oder Parameter wird gewählt", "Ungeeignete Behandlung", "Patient", 4, 3, "Usability Engineering nach IEC 62366-1, Training, klare IFU", "Usability Summative Evaluation"),
    HazardRule("Mechanische Gefährdung", ["beweglich", "halterung", "mechan"], "Instabile oder scharfkantige Komponenten", "Quetschen/Schneiden bei Handhabung", "Verletzung", "Anwender/Patient", 3, 2, "Mechanische Schutzkanten, Stabilitätsprüfung", "Mechanischer Belastungstest"),
    HazardRule("Datenintegritäts- oder Kommunikationsfehler", ["schnittstelle", "hl7", "usb", "ethernet", "daten"], "Datenverlust, Paketfehler, Mappingfehler", "Falsche Patientendaten oder lückenhafte Trends", "Fehlentscheidung", "Patient", 4, 2, "CRC/Checksummen, Interface-Protokolltests, Audit-Log", "Integrationstest Schnittstellen"),
]


class RiskEngine:
    def generate(self, info: ExtractedInfo) -> RiskFile:
        corpus = "\n".join([str(v) for v in info.raw_sections.values()]).lower()
        risks: List[RiskItem] = []
        open_points: List[str] = []
        generation_warnings = list(info.parsing_warnings)

        risk_counter = 1
        for rule in HAZARD_RULES:
            matched = any(trigger in corpus for trigger in rule.triggers)
            if matched:
                pre = rule.base_severity * rule.base_probability
                post = max(1, (rule.base_severity - 1) * max(1, rule.base_probability - 1))
                risks.append(
                    RiskItem(
                        risk_id=f"R-{risk_counter:03d}",
                        hazard=rule.hazard,
                        cause=rule.cause,
                        hazardous_situation=rule.hazardous_situation,
                        potential_harm=rule.potential_harm,
                        affected_person=rule.default_affected_person,
                        severity=rule.base_severity,
                        probability=rule.base_probability,
                        pre_control_risk=pre,
                        control_measure=rule.control_measure,
                        post_control_risk=post,
                        residual_risk_acceptable=post <= 6,
                        verification_reference=rule.verification_reference,
                        comment="Heuristisch aus Dokumentinhalt abgeleitet.",
                        evidence_type=EvidenceType.DERIVED,
                        evidence_note="Trigger im Dokument gefunden.",
                    )
                )
                risk_counter += 1

        # ensure baseline generic hazards if not captured
        if not risks:
            generation_warnings.append("Keine spezifischen Trigger erkannt; generische Standardrisiken wurden ergänzt.")

        for fallback in HAZARD_RULES[:4]:
            if all(r.hazard != fallback.hazard for r in risks):
                pre = fallback.base_severity * fallback.base_probability
                post = max(1, (fallback.base_severity - 1) * max(1, fallback.base_probability - 1))
                risks.append(
                    RiskItem(
                        risk_id=f"R-{risk_counter:03d}",
                        hazard=fallback.hazard,
                        cause=fallback.cause,
                        hazardous_situation=fallback.hazardous_situation,
                        potential_harm=fallback.potential_harm,
                        affected_person=fallback.default_affected_person,
                        severity=fallback.base_severity,
                        probability=fallback.base_probability,
                        pre_control_risk=pre,
                        control_measure=fallback.control_measure,
                        post_control_risk=post,
                        residual_risk_acceptable=None,
                        verification_reference=fallback.verification_reference,
                        comment="Generisches Basisrisiko für Elektromedizinprodukt.",
                        evidence_type=EvidenceType.GENERIC,
                        evidence_note="Kein direkter Trigger; manuelle Relevanzprüfung erforderlich.",
                    )
                )
                risk_counter += 1

        if not info.product_name:
            open_points.append("Produktname durch Regulatory/QM ergänzen.")
        if not info.intended_use:
            open_points.append("Zweckbestimmung nach IEC 60601-Kontext präzisieren.")
        if not info.software_components:
            open_points.append("Softwareanteile und SOUP-Anteile prüfen (IEC 62304).")
        if not info.interfaces:
            open_points.append("Schnittstellenrisiken und Datenpfade manuell bewerten.")

        assumptions = list(info.assumptions)
        assumptions.extend(
            [
                "Risikokennzahlen (S/P) sind MVP-Startwerte und müssen projektspezifisch kalibriert werden.",
                "Die Anwendung erzeugt keinen regulatorischen Freigabeentscheid.",
            ]
        )

        return RiskFile(
            product_identification=info.product_name or "manuelle Bewertung erforderlich",
            intended_use=info.intended_use or "manuelle Bewertung erforderlich",
            assumptions_and_inputs=assumptions,
            identified_hazards=risks,
            pre_control_assessment="Semiquantitative Bewertung via SxP-Regel (1-5) als Entwurfsstand.",
            risk_control_summary="Maßnahmenvorschläge aus Regelbasis; Wirksamkeit muss verifiziert werden.",
            residual_risk_assessment="Restrisiken sind nur vorläufig bewertet; Benefit-Risk Entscheidung durch Fachgremium.",
            verification_summary="Verifikationsnachweise sind Platzhalter und müssen im V&V-Plan konkretisiert werden.",
            open_points=open_points,
            generation_warnings=generation_warnings,
        )
