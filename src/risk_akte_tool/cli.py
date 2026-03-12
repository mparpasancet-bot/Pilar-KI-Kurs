from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .exporter import Exporter
from .extractor import InformationExtractor
from .parser import DocumentParser
from .risk_engine import RiskEngine
from .template_generator import RiskFileTemplateGenerator


def configure_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def run(input_path: str, output_dir: str) -> None:
    parser = DocumentParser()
    extractor = InformationExtractor()
    engine = RiskEngine()
    template = RiskFileTemplateGenerator()
    exporter = Exporter()

    raw = parser.parse(input_path)
    info = extractor.extract(raw)
    risk_file = engine.generate(info)
    markdown = template.to_markdown(risk_file)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    exporter.export_markdown(markdown, str(out_dir / "risikoakte.md"))
    exporter.export_csv_matrix(risk_file, str(out_dir / "risikomatrix.csv"))


def main() -> None:
    argp = argparse.ArgumentParser(description="Automatische Risikoakte-Generierung (MVP)")
    argp.add_argument("input", help="Pfad zu Eingabedokument (.md/.txt/.docx/.pdf)")
    argp.add_argument("--output-dir", default="output", help="Ausgabeverzeichnis")
    argp.add_argument("--verbose", action="store_true")
    args = argp.parse_args()

    configure_logging(args.verbose)
    run(args.input, args.output_dir)


if __name__ == "__main__":
    main()
