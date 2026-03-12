from risk_akte_tool.extractor import InformationExtractor
from risk_akte_tool.risk_engine import RiskEngine


def test_generates_risks_and_open_points():
    text = """Produktname:\nX100\n\nIntended Use:\nMonitoring\n\nSoftware:\n- Firmware\n\nSchnittstellen:\n- USB\n\nWarnhinweise:\n- Alarm prüfen\n"""
    info = InformationExtractor().extract(text)
    rf = RiskEngine().generate(info)

    assert rf.identified_hazards
    assert any(r.hazard == "Softwarefehler" for r in rf.identified_hazards)
    assert all(r.risk_id.startswith("R-") for r in rf.identified_hazards)
