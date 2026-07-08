from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    """
    Represents the shared state passed between the three EcoStream agents.
    """
    # Inputs from sensors
    leak_rate: float
    pressure: float
    image_bytes: Optional[bytes]
    
    # Agent 1 outputs (Multimodal Monitor)
    anomaly_detected: bool
    telemetry_status: str
    visual_analysis_summary: str
    
    # Agent 2 outputs (Risk & ESG Assessment)
    gas_lost_cost_hourly: float
    carbon_penalty_hourly: float
    co2_equivalent_rate: float
    esg_risk_level: str  # Low, Medium, High
    
    # Agent 3 outputs (Action & Orchestration)
    scada_signal_sent: bool
    scada_log: str
    inventory_available: bool
    dispatch_status: str
    generated_runbook: str
    
    # Execution routing metadata
    current_agent: str
    logs: List[str]
