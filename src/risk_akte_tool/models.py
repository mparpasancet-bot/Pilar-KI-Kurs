from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class EvidenceType(str, Enum):
    EXTRACTED = "extracted"
    DERIVED = "derived"
    GENERIC = "generic"


@dataclass
class ExtractedInfo:
    product_name: Optional[str] = None
    product_category: Optional[str] = None
    intended_use: Optional[str] = None
    user_groups: List[str] = field(default_factory=list)
    patient_groups: List[str] = field(default_factory=list)
    environment: List[str] = field(default_factory=list)
    function_description: Optional[str] = None
    electrical_mechanical_features: List[str] = field(default_factory=list)
    software_components: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    accessories: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    known_residual_risks: List[str] = field(default_factory=list)
    protective_measures: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    raw_sections: Dict[str, str] = field(default_factory=dict)
    parsing_warnings: List[str] = field(default_factory=list)


@dataclass
class RiskItem:
    risk_id: str
    hazard: str
    cause: str
    hazardous_situation: str
    potential_harm: str
    affected_person: str
    severity: int
    probability: int
    pre_control_risk: int
    control_measure: str
    post_control_risk: int
    residual_risk_acceptable: Optional[bool]
    verification_reference: str
    comment: str
    evidence_type: EvidenceType
    evidence_note: str


@dataclass
class RiskFile:
    product_identification: str
    intended_use: str
    assumptions_and_inputs: List[str]
    identified_hazards: List[RiskItem]
    pre_control_assessment: str
    risk_control_summary: str
    residual_risk_assessment: str
    verification_summary: str
    open_points: List[str]
    generation_warnings: List[str]
