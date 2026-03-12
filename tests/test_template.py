from risk_akte_tool.extractor import InformationExtractor
from risk_akte_tool.risk_engine import RiskEngine
from risk_akte_tool.template_generator import RiskFileTemplateGenerator


def test_markdown_contains_matrix_header():
    info = InformationExtractor().extract("Produktname:\nX\n\nIntended Use:\nY")
    rf = RiskEngine().generate(info)
    md = RiskFileTemplateGenerator().to_markdown(rf)
    assert "| ID | Gefährdung |" in md
    assert "## 9. Offene Punkte / manueller Review erforderlich" in md
