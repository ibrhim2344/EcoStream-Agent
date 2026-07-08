# agents/nodes/monitor.py
import os
from google import genai
from google.genai import types
from agents.state import AgentState

def monitor_node(state: AgentState) -> dict:
    """
    Node for Agent 1 (Multimodal Monitor). Processes sensory inputs and checks bounds.
    """
    logs = state.get("logs", [])
    logs.append("[Node: Monitor] Checking incoming line sensor metrics...")
    
    leak_rate = state.get("leak_rate", 0.0)
    pressure = state.get("pressure", 0.0)
    image_bytes = state.get("image_bytes", None)
    
    # Heuristic metrics boundaries
    anomaly_detected = leak_rate >= 5.0
    telemetry_status = "⚠️ Pressure/Concentration Anomaly Detected" if (pressure >= 800 or leak_rate >= 30) else "✅ Normal Operating Envelope"
    
    visual_summary = "No field media provided."
    
    # Execute Gemini vision model if an asset photo is uploaded
    if image_bytes:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-09-2025",
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        "Analyze this industrial gas asset infrastructure. Flag visible methane plumes or gas venting clouds."
                    ]
                )
                visual_summary = response.text
            except Exception as e:
                visual_summary = f"Multimodal engine temporarily bypass-mode: {str(e)}"
        else:
            visual_summary = "Gemini API key missing. Vision processing skipped."
    elif anomaly_detected:
        visual_summary = "☁️ Anomalous Thermal Plume Spotted Near Valve V-102 (Simulated)"
    else:
        visual_summary = "✅ Field of view completely clear."

    logs.append(f"[Node: Monitor] Anomaly detection run finished. Flag={anomaly_detected}")
    
    # Return updates to the state
    return {
        "anomaly_detected": anomaly_detected,
        "telemetry_status": telemetry_status,
        "visual_analysis_summary": visual_summary,
        "logs": logs
    }