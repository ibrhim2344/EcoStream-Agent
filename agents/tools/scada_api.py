# agents/tools/scada_api.py
import time

def isolate_valve(valve_id: str, trigger_automatic: bool = True) -> dict:
    """
    Sends a digital command sequence to the remote SCADA RTU to isolate a physical valve.
    """
    if not trigger_automatic:
        return {"status": "SKIPPED", "message": f"SCADA: Valve {valve_id} remains in manual override status."}
        
    # Simulate hardware network latency
    time.sleep(0.4) 
    
    return {
        "status": "SUCCESS",
        "valve_id": valve_id,
        "flow_reduction_pct": 98.5,
        "timestamp": time.time(),
        "message": f"SCADA: Digital signal sent successfully. Valve {valve_id} confirmed closed. Flow reduced by 98.5%."
    }