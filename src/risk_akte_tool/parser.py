from __future__ import annotations

import io
import logging
import re
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


class DocumentParser:
    """Reads common text-based document formats and returns plain text."""

    def parse(self, file_path: str) -> str:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")
        if suffix == ".docx":
            return self._parse_docx(path)
        if suffix == ".pdf":
            return self._parse_pdf(path)
        raise ValueError(f"Unsupported input format: {suffix}")

    def _parse_docx(self, path: Path) -> str:
        try:
            with zipfile.ZipFile(path) as zf:
                xml_content = zf.read("word/document.xml").decode("utf-8", errors="ignore")
            xml_content = re.sub(r"</w:p>", "\n", xml_content)
            text = re.sub(r"<[^>]+>", "", xml_content)
            return text
        except Exception as exc:  # pragma: no cover - safety guard
            logger.exception("DOCX parsing failed")
            raise RuntimeError(f"Failed to parse DOCX: {path}") from exc

    def _parse_pdf(self, path: Path) -> str:
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "PDF support requires the optional dependency 'pypdf'."
            ) from exc

        with path.open("rb") as f:
            reader = PdfReader(io.BytesIO(f.read()))
            pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
