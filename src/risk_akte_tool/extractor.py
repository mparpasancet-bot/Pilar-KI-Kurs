from __future__ import annotations

import re
from typing import Dict, List

from .models import ExtractedInfo

SECTION_ALIASES = {
    "product name": "product_name",
    "produktname": "product_name",
    "product category": "product_category",
    "produktkategorie": "product_category",
    "intended use": "intended_use",
    "zweckbestimmung": "intended_use",
    "anwendergruppen": "user_groups",
    "user groups": "user_groups",
    "patientengruppen": "patient_groups",
    "einsatzumgebung": "environment",
    "environment": "environment",
    "funktionsbeschreibung": "function_description",
    "software": "software_components",
    "schnittstellen": "interfaces",
    "interfaces": "interfaces",
    "zubehör": "accessories",
    "warnhinweise": "warnings",
    "kontraindikationen": "contraindications",
    "restrisiken": "known_residual_risks",
    "schutzmaßnahmen": "protective_measures",
}

LIST_FIELDS = {
    "user_groups",
    "patient_groups",
    "environment",
    "electrical_mechanical_features",
    "software_components",
    "interfaces",
    "accessories",
    "warnings",
    "contraindications",
    "known_residual_risks",
    "protective_measures",
}


class InformationExtractor:
    def extract(self, raw_text: str) -> ExtractedInfo:
        sections = self._split_sections(raw_text)
        info = ExtractedInfo(raw_sections=sections)

        for sec_title, sec_text in sections.items():
            mapped = SECTION_ALIASES.get(sec_title.lower().strip())
            if mapped:
                self._apply_field(info, mapped, sec_text)

        # fallback regex extraction for unstructured docs
        info.product_name = info.product_name or self._extract_line(raw_text, r"(?im)^\s*(product\s*name|produktname)\s*[:\-]\s*(.+)$")
        info.product_category = info.product_category or self._extract_line(raw_text, r"(?im)^\s*(product\s*category|produktkategorie)\s*[:\-]\s*(.+)$")
        info.intended_use = info.intended_use or self._extract_line(raw_text, r"(?im)^\s*(intended\s*use|zweckbestimmung)\s*[:\-]\s*(.+)$")

        if not info.product_name:
            info.parsing_warnings.append("Produktname fehlt – manuelle Bewertung erforderlich.")
        if not info.intended_use:
            info.parsing_warnings.append("Zweckbestimmung fehlt – manuelle Bewertung erforderlich.")

        if not info.user_groups:
            info.assumptions.append("Anwendergruppen wurden nicht explizit gefunden.")
        return info

    def _split_sections(self, text: str) -> Dict[str, str]:
        sections: Dict[str, str] = {}
        current = "_document"
        buf: List[str] = []
        for line in text.splitlines():
            m = re.match(r"^\s{0,3}(#+\s+)?([A-Za-zÄÖÜäöüß0-9\-/ ]{3,}):\s*$", line)
            if m:
                sections[current] = "\n".join(buf).strip()
                current = m.group(2).strip()
                buf = []
            else:
                buf.append(line)
        sections[current] = "\n".join(buf).strip()
        return {k: v for k, v in sections.items() if v}

    def _apply_field(self, info: ExtractedInfo, field_name: str, value: str) -> None:
        value = value.strip()
        if not value:
            return
        if field_name in LIST_FIELDS:
            entries = [re.sub(r"^[-*]\s*", "", line).strip() for line in value.splitlines() if line.strip()]
            getattr(info, field_name).extend(entries)
        else:
            setattr(info, field_name, value)

    @staticmethod
    def _extract_line(text: str, pattern: str) -> str | None:
        m = re.search(pattern, text)
        return m.group(2).strip() if m else None
