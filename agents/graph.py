# agents/graph.py
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes.monitor import monitor_node
from agents.nodes.assessment import assessment_node
from agents.nodes.execution import execution_node

def compile_workflow():
    """
    Assembles individual nodes and links them sequentially using LangGraph.
    """
    # 1. Initialize StateGraph with our structured state object
    workflow = StateGraph(AgentState)
    
    # 2. Register operational nodes into the graph workspace
    workflow.add_node("multimodal_monitor", monitor_node)
    workflow.add_node("risk_assessment", assessment_node)
    workflow.add_node("action_orchestration", execution_node)
    
    # 3. Establish the operational route edges (Sensing -> Analysis -> Response)
    workflow.set_entry_point("multimodal_monitor")
    workflow.add_edge("multimodal_monitor", "risk_assessment")
    workflow.add_edge("risk_assessment", "action_orchestration")
    workflow.add_edge("action_orchestration", END)
    
    # 4. Compile the graph into an executable application instance
    return workflow.compile()

# Global compiled application instance for simple import
app_graph = compile_workflow()