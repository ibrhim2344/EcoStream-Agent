# agents/nodes/execution.py
import os
from google import genai
from agents.state import AgentState
from agents.tools.scada_api import isolate_valve
from agents.tools.cmms_api import check_warehouse_inventory
from agents.tools.mail_service import send_emergency_dispatch_email

def execution_node(state: AgentState) -> dict:
    """
    Node for Agent 3 (Action & Orchestration). Calls tools and builds generative repair runbooks.
    """
    logs = state.get("logs", [])
    logs.append("[Node: Execution] Dispatching automation runbooks and checking parts logistics...")
    
    leak_rate = state.get("leak_rate", 0.0)
    pressure = state.get("pressure", 0.0)
    risk = state.get("esg_risk_level", "Low")
    
    # 1. Trigger SCADA Tool
    scada_res = isolate_valve("V-102", trigger_automatic=(leak_rate >= 5.0))
    
    # 2. Trigger CMMS Inventory Tool
    inventory_res = check_warehouse_inventory("Replacement Valve V-102 Kit")
    
    # Technical specs setup
    tech_name = "Engineer Khalid"
    tech_contact = "+966 55-XXX-XXXX"
    
    # 3. Compile Runbook via Gemini LLM
    runbook_text = ""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if leak_rate >= 5.0:
        if api_key:
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                Generate a professional Oil & Gas engineering repair runbook.
                Asset Context: Pipeline Segment PL-07 / Valve V-102
                Telemetry: Methane Leak={leak_rate} kg/hr, Pressure={pressure} PSI, ESG Risk={risk}
                Inventory status: {inventory_res['details']}
                Assigned Staff: {tech_name}
                Include critical isolation safety markers and torque requirements (95 N.m). Be explicit and technical.
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-09-2025",
                    contents=prompt
                )
                runbook_text = response.text
            except Exception as e:
                runbook_text = f"Emergency fallback runbook active. AI engine link down: {str(e)}"
        else:
            # Fallback text if no API key is set
            runbook_text = f"Local Fallback Runbook:\n- Don PPE Level 3.\n- Close manual safety valves.\n- Retrieve part from {inventory_res['details'].get('warehouse_zone', 'Main Store')}."
            
        # 4. Trigger Mail/SMS alert tool
        send_emergency_dispatch_email(tech_name, tech_contact, runbook_text)
        dispatch_status = f"Emergency Order Issued to {tech_name}"
    else:
        runbook_text = "Baseline Operational Parameters: Asset healthy. No maintenance required."
        dispatch_status = "Inbound monitoring idle."

    logs.append("[Node: Execution] Prescriptive engine workflow finished safely.")
    
    return {
        "scada_signal_sent": scada_res["status"] == "SUCCESS",
        "scada_log": scada_res["message"],
        "inventory_available": inventory_res["part_found"],
        "dispatch_status": dispatch_status,
        "generated_runbook": runbook_text,
        "logs": logs
    }