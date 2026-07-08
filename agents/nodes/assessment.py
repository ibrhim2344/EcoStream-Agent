# agents/nodes/assessment.py
from agents.state import AgentState

def assessment_node(state: AgentState) -> dict:
    """
    Node for Agent 2 (Risk & ESG Assessment). Calculates metrics based on physical leak rates.
    """
    logs = state.get("logs", [])
    logs.append("[Node: Assessment] Initiating carbon accounting & financial penalty algorithms...")
    
    leak_rate = state.get("leak_rate", 0.0)
    
    # Constants
    methane_price_per_kg = 0.08
    gwp_ch4 = 28
    carbon_tax_per_tonne = 85.0
    
    # Environmental math
    gas_lost_cost = leak_rate * methane_price_per_kg
    co2e_kgph = leak_rate * gwp_ch4
    carbon_penalty = (co2e_kgph / 1000.0) * carbon_tax_per_tonne
    
    # Risk stratification
    if leak_rate >= 50:
        risk_level = "High"
    elif leak_rate >= 15:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    logs.append(f"[Node: Assessment] Calculation complete. ESG Impact Class: {risk_level}")
    
    return {
        "gas_lost_cost_hourly": gas_lost_cost,
        "carbon_penalty_hourly": carbon_penalty,
        "co2_equivalent_rate": co2e_kgph,
        "esg_risk_level": risk_level,
        "logs": logs
    }