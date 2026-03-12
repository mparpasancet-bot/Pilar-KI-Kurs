from __future__ import annotations

import csv
from pathlib import Path

from .models import RiskFile


class Exporter:
    def export_markdown(self, content: str, output_path: str) -> None:
        Path(output_path).write_text(content, encoding="utf-8")

    def export_csv_matrix(self, risk_file: RiskFile, output_path: str) -> None:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Gefährdung",
                    "Ursache",
                    "Gefährdungssituation",
                    "möglicher Schaden",
                    "betroffene Person",
                    "S",
                    "P",
                    "Risiko vor Maßnahme",
                    "Maßnahme",
                    "Risiko nach Maßnahme",
                    "Restrisiko akzeptabel",
                    "Verweis auf Nachweis / Test / Dokument",
                    "Kommentar",
                    "Herkunft",
                ]
            )
            for r in risk_file.identified_hazards:
                writer.writerow(
                    [
                        r.risk_id,
                        r.hazard,
                        r.cause,
                        r.hazardous_situation,
                        r.potential_harm,
                        r.affected_person,
                        r.severity,
                        r.probability,
                        r.pre_control_risk,
                        r.control_measure,
                        r.post_control_risk,
                        r.residual_risk_acceptable,
                        r.verification_reference,
                        r.comment,
                        r.evidence_type.value,
                    ]
                )
