# AI Agent Evaluation Frameworks: A Comparative Survey

This repository provides a concise overview and visualization of evaluation methodologies from three significant papers in the field of AI Agents. The focus is on understanding **how** these agents are evaluated across different domains: Clinical Simulation, Tool Utilization, and Data Science.

---

## 1. AgentClinic: Multimodal Clinical Simulation
> **Domain:** Healthcare / Interactive Diagnosis

**Dynamic Interaction Phase** The agent operates as a physician in a virtual clinic, replacing static Q&A with active role-play. Starting with incomplete information, it must lead a multi-turn dialogue with a simulated patient and autonomously deploy diagnostic tools. This setup rigorously evaluates long-horizon reasoning and active information gathering strategies.

**Multidimensional Scoring System** Performance is evaluated through three distinct lenses:
* **Objective:** A moderator agent verifies diagnostic accuracy against ground truth case data.
* **Subjective:** The patient agent rates soft skills, including trust, professionalism, and compliance.
* **Robustness:** Adversarial noise and biases are injected to test stability and objectivity under pressure.

### Workflow Visualization

```mermaid
graph LR
    %% Style Definitions
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef actor fill:#e1f5fe,stroke:#01579b,stroke-width:2px,rx:10,ry:10;
    classDef score fill:#ffcdd2,stroke:#c62828,stroke-width:2px,rx:50,ry:50;
    classDef report fill:#e0e0e0,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% 1. Input Section
    Case["1. Test Case<br/>(Ground Truth)"]:::input
    Noise["2. Bias / Noise<br/>(Interference)"]:::input

    %% 2. Interaction Section (The Core)
    Target("3. Target Agent<br/>(The Student)"):::actor
    SimUser("4. Sim User<br/>(The Environment)"):::actor

    %% Connections
    Case --> Target
    Noise -.-> Target
    Target <-->|5. Multi-turn<br/>Dialogue| SimUser
    
    %% 3. Output Section
    Target -->|6. Submit| Decision["7. Final Decision"]:::actor

    %% 4. Scoring Section (Three Metrics)
    Decision --Vs Truth--> Metric1(("8. Accuracy<br/>Score")):::score
    SimUser --Feedback--> Metric2(("9. User<br/>Satisfaction")):::score
    Noise -.->|Check Impact| Metric3(("10. Robustness<br/>Score")):::score

    %% 5. Final Report
    Metric1 --> Report["11. Evaluation Report"]:::report
    Metric2 --> Report
    Metric3 --> Report
