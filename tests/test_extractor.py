from risk_akte_tool.extractor import InformationExtractor


def test_extracts_core_fields():
    text = """Produktname:\nX100\n\nIntended Use:\nMonitoring\n\nAnwendergruppen:\n- Klinikpersonal\n"""
    info = InformationExtractor().extract(text)
    assert info.product_name == "X100"
    assert info.intended_use == "Monitoring"
    assert "Klinikpersonal" in info.user_groups
