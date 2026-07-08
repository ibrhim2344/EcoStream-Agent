🤖 EcoStream-Agent Multi-Agent Architecture

Welcome to the technical engineering guide for the EcoStream-Agent framework. This platform leverages Multi-Agent Systems (MAS) powered by stateful workflows (such as LangGraph) to automate the detection, assessment, and autonomous mitigation of methane leaks in oil and gas infrastructure.

🏗️ Agentic Workflow & Communication Topology

Our agent network utilizes a highly efficient, deterministic "Chain-of-Agents" routing protocol. Instead of relying on generalist LLM prompt-loops, each agent has distinct boundaries, state access, and execution triggers to manage critical industrial scenarios safely.

                  ┌──────────────────────┐
                  │    User Interface    │
                  │   (Streamlit App)    │
                  └──────────▲───────────┘
                             │ (Telemetry Input / Simulation)
                  ┌──────────▼───────────┐
                  │ 📡  Monitor Agent    │
                  └──────────┬───────────┘
                             │ (State: Leak Detected)
                  ┌──────────▼───────────┐
                  │ 📊  Assessment Agent │
                  └──────────┬───────────┘
                             │ (State: Calculated ESG/Fin Risk)
                  ┌──────────▼───────────┐
                  │ ⚡ Orchestrator Agent │
                  └──────────────────────┘
                   (Executes SCADA valve 
                    shutoff, CMMS queries, 
                    & technician dispatch)


👥 Agent Roles, Responsibilities & Tooling

1. Multimodal Monitor Agent (MonitorAgent)

Core Role: The "Senses" of the system. It continuously parses thermal imagery and physical sensor data to verify anomalies.

Technical Responsibilities:

Monitors real-time pipeline pressure, gas flow rates, and ambient temperature telemetry.

Processes simulated optical gas imaging (OGI) or thermal feeds to verify invisible methane cloud plumes.

Transitions the system state to leak_detected = True upon anomaly verification.

Core Tools: Edge Telemetry Profiler, Thermal Image Analyzer, Pressure Drop Validator.

2. Risk & ESG Assessment Agent (AssessmentAgent)

Core Role: The "Analyst" of the system. It quantifies the financial, environmental, and compliance impact of the detected event.

Technical Responsibilities:

Computes volumetric gas loss over elapsed time and calculates immediate raw commodity value loss ($).

Calculates carbon-equivalent emissions and estimated Carbon Tax Penalties using the scientific equation:

$$\text{CO}_2\text{e} = \dot{m}_{\text{CH}_4} \times \text{GWP}_{\text{CH}_4}$$

(Using a standard Global Warming Potential $\text{GWP}$ of 28 for methane).

Assigns an automated ESG Risk Severity level (Low, Medium, High).

Core Tools: Carbon Penalty Calculator, Financial Loss Estimator, Regulatory Risk Scorer.

3. Action & Orchestration Agent (OrchestrationAgent)

Core Role: The "Hands" of the system. It translates analytical insights into immediate, safety-compliant physical and logistical actions.

Technical Responsibilities:

Simulates secure commands to SCADA systems to isolate the leaking line section (e.g., closing virtual valves).

Queries CMMS/ERP inventory databases (such as SAP/Maximo) to check replacement part availability (valves, gaskets, flanges).

Geolocates the nearest field engineer, triggers a dispatch notification, and generates a context-specific maintenance repair runbook using Generative AI.

Core Tools: SCADA Controller Connector, CMMS Inventory Checker, Automated Runbook Generator.

🤝 Stateful Collaboration Protocol (Simulation Example)

When a physical leak occurs on Line-A, the agents update the shared AgentState sequentially:

Detection: MonitorAgent observes a sudden pressure drop from 900 PSI to 450 PSI. It flags the event, updates leak_detected = True, and passes state control forward.

Quantification: AssessmentAgent calculates that at 450 PSI, the leak rate is $25\text{ kg/hr}$. It computes that every hour of inaction costs $\$48$ in lost gas and $\$1,344$ in carbon tax penalties ($25 \times 28 = 700\text{ kg } \text{CO}_2\text{e}\text{ per hour}$).

Prescription: OrchestrationAgent receives this critical risk payload. It instantly transmits an override command to shut Valve-12, queries the warehouse for a replacement valve kit, and dispatches a detailed work order to the closest technician with a step-by-step safety runbook.

🛠️ Technology Stack & Standards

Orchestration: LangGraph (Stateful multi-agent pipelines with cyclic memory).

Core Cognitive Engine: gemini-2.5-flash-preview-09-2025 (optimized for hyper-low latency tool execution and structured outputs).

Knowledge Base (RAG): ChromaDB vectorized with EPA (Environmental Protection Agency) guidelines, safety standards, and manufacturer equipment manuals.

User Presentation: Streamlit Web Dashboard.