from __future__ import annotations

from .models import EvidenceType, RiskFile


class RiskFileTemplateGenerator:
    def to_markdown(self, risk_file: RiskFile) -> str:
        lines = [
            "# Risikoakte-Entwurf für Elektromedizinprodukt",
            "",
            "## 1. Produktidentifikation",
            f"- Produkt: {risk_file.product_identification}",
            "",
            "## 2. Zweckbestimmung",
            f"- {risk_file.intended_use}",
            "",
            "## 3. Annahmen und Eingangsdaten",
        ]
        lines.extend([f"- {a}" for a in risk_file.assumptions_and_inputs] or ["- Keine"])

        lines.extend(["", "## 4. Liste identifizierter Gefährdungen"])
        for r in risk_file.identified_hazards:
            lines.append(f"- {r.risk_id}: {r.hazard} ({r.evidence_type.value})")

        lines.extend(
            [
                "",
                "## 5. Risikobewertung vor Maßnahmen",
                f"- {risk_file.pre_control_assessment}",
                "",
                "## 6. Risikokontrollmaßnahmen",
                f"- {risk_file.risk_control_summary}",
                "",
                "## 7. Bewertung des Restrisikos",
                f"- {risk_file.residual_risk_assessment}",
                "",
                "## 8. Verifikation der Maßnahmen",
                f"- {risk_file.verification_summary}",
                "",
                "## 9. Offene Punkte / manueller Review erforderlich",
            ]
        )
        lines.extend([f"- {p}" for p in risk_file.open_points] or ["- Keine"])

        lines.extend(["", "## 10. Warnungen", ""])
        lines.extend([f"- {w}" for w in risk_file.generation_warnings] or ["- Keine"])

        lines.extend(["", "## 11. Risikomatrix", ""])
        lines.append(
            "| ID | Gefährdung | Ursache | Gefährdungssituation | möglicher Schaden | betroffene Person | S | P | Risiko vor Maßnahme | Maßnahme | Risiko nach Maßnahme | Restrisiko akzeptabel | Verweis auf Nachweis / Test / Dokument | Kommentar | Herkunft |"
        )
        lines.append("|---|---|---|---|---|---|---:|---:|---:|---|---:|---|---|---|---|")

        for r in risk_file.identified_hazards:
            acceptable = (
                "Ja" if r.residual_risk_acceptable is True else "Nein" if r.residual_risk_acceptable is False else "Manuelle Bewertung erforderlich"
            )
            lines.append(
                f"| {r.risk_id} | {r.hazard} | {r.cause} | {r.hazardous_situation} | {r.potential_harm} | {r.affected_person} | {r.severity} | {r.probability} | {r.pre_control_risk} | {r.control_measure} | {r.post_control_risk} | {acceptable} | {r.verification_reference} | {r.comment} | {self._evidence_label(r.evidence_type)} |"
            )
        return "\n".join(lines)

    @staticmethod
    def _evidence_label(ev: EvidenceType) -> str:
        if ev == EvidenceType.EXTRACTED:
            return "Direkt extrahiert"
        if ev == EvidenceType.DERIVED:
            return "Abgeleitet"
        return "Generisch"
