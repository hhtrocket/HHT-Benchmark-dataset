## 6. MAJ-EVAL: Multi-Agent-as-Judge

**Domain**: General / Multi-dimensional Human Alignment

**Persona Construction Phase**
This phase utilizes a Persona Miner to automate the creation of evaluator profiles. Instead of relying on manual prompts, the system analyzes source documents such as research papers or official grading rubrics to extract specific evaluation dimensions. These dimensions are then used to instantiate multiple stakeholder agents. Each agent represents a distinct professional or user perspective, such as a domain expert, an end-user, or a technical auditor, ensuring the evaluation is grounded in realistic and diverse criteria.

**Collaborative Evaluation Phase**
The framework employs a structured Multi-round Debate and Reflection mechanism to process the target agent's response. The workflow consists of three sub-steps:

1. **Independent Assessment**: Each stakeholder agent provides an initial score and feedback based strictly on their assigned persona and expertise.
2. **Interactive Debate**: Agents exchange their evaluations and engage in a multi-turn discussion. This process forces the agents to defend their reasoning, identify overlooked details in the response, and challenge the biases of other participants.
3. **Reflection and Revision**: Following the debate, agents reflect on the group discussion and update their individual evaluations to reach a more nuanced conclusion.

**Final Synthesis and Aggregation**
An Impartial Aggregator agent collects the final reflections from all stakeholders. This aggregator identifies key areas of consensus and unresolved points of contention. The output includes a consolidated diagnostic report and a set of multi-dimensional scores. This method significantly reduces common single-judge issues such as self-preference bias and position bias while providing high-quality qualitative feedback.

### Workflow Visualization

```mermaid
graph LR
    %% Style Definitions
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef actor fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef score fill:#ffcdd2,stroke:#c62828,stroke-width:2px,rx:50,ry:50;
    classDef report fill:#e0e0e0,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% === Phase 1:Persona Construction  ===
    subgraph Phase1 ["Phase 1: Persona Construction"]
        Docs["1. Source Documents<br/>Domain Papers / Rubrics"]:::input
        Miner["2. Persona Miner<br/>Dimension Extraction"]:::phase1
        Agents["3. Stakeholder Agents<br/>Specialized Personas"]:::actor
        
        Docs --> Miner --> Agents
    end

    %% === Phase 2: Collaborative Evaluation ===
    subgraph Phase2 ["Phase 2: Multi-Agent Evaluation"]
        Target["4. Target Response<br/>Agent Output"]:::input
        Debate{"5. Multi-turn Debate<br/>Reflection Cycle"}:::phase2
        Aggregator["6. Impartial Aggregator<br/>Consensus Synthesis"]:::phase2
        
        Target --> Debate
        Agents <-->|Cross-Feedback| Debate
        Debate --> Aggregator
    end

    %% === Output Section ===
    Metric1(("7. Multi-dim Scores<br/>Stakeholder Metrics")):::score
    Report["8. Consolidated Report<br/>Diagnostic Feedback"]:::report

    Aggregator --> Metric1
    Aggregator --> Report

```
