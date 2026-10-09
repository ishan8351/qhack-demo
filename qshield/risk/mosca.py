from enum import Enum
from typing import Dict, Any

class DataClassification(str, Enum):
    FINANCIAL_RECORDS = "financial_records"  # 10 years retention
    HEALTHCARE_DATA = "healthcare_data"      # 30-50 years retention
    GOVERNMENT_DEFENSE = "government_defense" # 25+ years retention
    TRANSIENT_SESSION = "transient_session"  # <1 year retention
    CUSTOMER_PII = "customer_pii"            # 7-10 years retention

DATA_CLASS_DEFAULT_SHELF_LIFE = {
    DataClassification.FINANCIAL_RECORDS: 10.0,
    DataClassification.HEALTHCARE_DATA: 35.0,
    DataClassification.GOVERNMENT_DEFENSE: 30.0,
    DataClassification.TRANSIENT_SESSION: 0.5,
    DataClassification.CUSTOMER_PII: 8.0,
}

def evaluate_mosca_inequality(
    shelf_life_years: float,
    migration_time_years: float,
    q_day_years: float,
    data_class: DataClassification = DataClassification.FINANCIAL_RECORDS
) -> Dict[str, Any]:
    """
    Evaluates Mosca's Inequality: Data is at risk when X + Y > Z
    X = shelf_life_years (years data must remain confidential)
    Y = migration_time_years (years required to migrate crypto)
    Z = q_day_years (years until Cryptanalytically Relevant Quantum Computer)
    """
    total_horizon = round(shelf_life_years + migration_time_years, 2)
    margin = round(total_horizon - q_day_years, 2)
    is_at_risk = total_horizon > q_day_years

    if margin > 0.0:
        exposure_level = "HIGH"
        verdict = f"Critical risk detected: RSA/ECC-protected records outlive their encryption by {margin} years. Migration has to start now."
    elif margin >= -2.0:
        exposure_level = "MEDIUM"
        verdict = f"Moderate risk window: {abs(margin)} years buffer remaining. Planning and PQC gateway deployment recommended."
    else:
        exposure_level = "LOW"
        verdict = f"Low risk: {abs(margin)} years buffer. System within safe migration thresholds."

    return {
        "shelf_life_years_X": shelf_life_years,
        "migration_time_years_Y": migration_time_years,
        "q_day_years_Z": q_day_years,
        "total_risk_horizon": total_horizon,
        "margin_years": margin,
        "is_at_risk": is_at_risk,
        "exposure_level": exposure_level,
        "data_classification": data_class.value,
        "verdict": verdict
    }
