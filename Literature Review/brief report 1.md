# AI Agent Evaluation Frameworks: A Comparative Survey

This repository provides a concise overview and visualization of evaluation methodologies from three significant papers in the field of AI Agents. The focus is on understanding how these agents are evaluated across different domains: Healthcare, Tool Utilization, and Data Science.

---

## 1. AgentClinic: Multimodal Clinical Simulation
> **Domain:** Healthcare / Interactive Diagnosis
> 
Link: https://arxiv.org/pdf/2405.07960

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

```

---

## 2. MCPEval: Automatic MCP-based Deep Evaluation

> **Domain:** Tool Use / Model Context Protocol
> 
Link:https://arxiv.org/pdf/2507.12806

**Phase 1: Benchmark Construction** The system automates dataset creation by employing a Generator LLM to synthesize tasks based on specific tool definitions. To ensure validity, a Verifier Agent attempts to solve each generated task. Only scenarios that are successfully resolved by this frontier model are retained in the final Benchmark Set, while unsolvable ones are discarded to maintain high quality.

**Phase 2: Evaluation Pipeline** The assessment stage involves the Target Agent executing these verified tasks to produce a Predicted Trajectory. An automated LLM Judge then compares this output against the reference Gold Trajectory. The performance is quantified using metrics such as Exact Match for precision and Plan Quality for reasoning logic, providing a comprehensive score of agent capability.

### Workflow Visualization

```mermaid
graph LR
    %% Style Definitions
    classDef p1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef p2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef data fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,stroke-dasharray: 5 5;
    classDef decision fill:#ffffff,stroke:#333,stroke-width:2px,shape:diamond;

    %% === Phase 1: Benchmark Construction ===
    subgraph Phase1 ["Phase 1: Benchmark Construction"]
        Tools["1. MCP Tools<br/>(API Defs)"]:::p1
        Generator["2. Task Generator<br/>(LLM)"]:::p1
        Verifier["3. Verifier Agent<br/>(Frontier Model)"]:::p1
        
        Check{"4. Solvable?"}:::decision
        
        GoldData["5. Benchmark Set<br/>(Task + Gold Trajectory)"]:::data
        
        Tools --> Generator --> Verifier --> Check
        Check --No (Discard)--> Generator
        Check --Yes (Keep)--> GoldData
    end

    %% === Phase 2: Evaluation Pipeline ===
    subgraph Phase2 ["Phase 2: Evaluation Pipeline"]
        Target["6. Target Agent<br/>(Student)"]:::p2
        Output["7. Predicted<br/>Trajectory"]:::data
        
        Judge["8. LLM Judge /<br/>Matcher"]:::p2
        
        %% Metrics
        M1(("9. Exact<br/>Match")):::p2
        M2(("10. Fuzzy<br/>Match")):::p2
        M3(("11. Plan<br/>Quality")):::p2
        
        %% Flow
        Target --> Output
        Output --> Judge
        GoldData --> Judge
        
        Judge --> M1
        Judge --> M2
        Judge --> M3
    end

    %% Connect the two phases
    GoldData --> Target

```

---

## 3. DeepAnalyze: Autonomous Data Science

> **Domain:** Data Analysis / End-to-End Execution
> 
Link:https://arxiv.org/abs/2510.16872

**Autonomous Execution Phase** The target agent receives natural language instructions and raw data, autonomously managing the full loop from code generation to execution. It must not only ensure the Python code runs successfully to produce accurate charts but also synthesize these findings into a deep research report, replicating the workflow of a human data analyst.

**Hybrid Evaluation Phase** The scoring system integrates objective rules with subjective judgment. A Rule-Based Judge verifies hard metrics such as code executability, file validity, and calculation accuracy. Simultaneously, an LLM Judge assesses soft metrics regarding the research report, including its helpfulness, logical coherence, and readability. These are combined into a final weighted score to ensure the assessment is both precise and holistic.

### Workflow Visualization

```mermaid
graph LR
    %% Style Definitions
    classDef p1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef p2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef output fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,stroke-dasharray: 5 5;
    classDef metric fill:#ffffff,stroke:#333,stroke-width:2px,rx:5,ry:5;

    %% === Phase 1: Autonomous Execution ===
    subgraph Phase1 ["Phase 1: Autonomous Execution Pipeline"]
        Query["1. User Instruction"]:::input
        Data["2. Raw Data Source"]:::input
        
        Agent["3. DeepAnalyze Agent"]:::p1
        Code["4. Code Generation"]:::p1
        Exec["5. Python Executor"]:::p1
        
        Result["6. Execution Outputs<br/>(Charts / Files)"]:::output
        Report["7. Research Report<br/>(Markdown / PDF)"]:::output
        
        %% Flow
        Query --> Agent
        Data --> Agent
        Agent --> Code --> Exec
        Exec --Success--> Result
        Result --> Agent
        Agent --> Report
    end

    %% === Phase 2: Hybrid Evaluation ===
    subgraph Phase2 ["Phase 2: Hybrid Evaluation System"]
        %% Stream A: Objective
        RuleJudge["8. Rule-Based Judge"]:::p2
        M1(("9. Exec<br/>Success")):::metric
        M2(("10. File<br/>Validity")):::metric
        M3(("11. Data<br/>Accuracy")):::metric
        
        %% Stream B: Subjective
        LLMJudge["12. LLM Judge<br/>(GPT-4)"]:::p2
        M4(("13. Help<br/>fulness")):::metric
        M5(("14. Inform<br/>ativeness")):::metric
        M6(("15. Coher<br/>ence")):::metric
        M7(("16. Read<br/>ability")):::metric
        
        %% Aggregation
        FinalScore["17. Final Weighted<br/>Score"]:::p2
        
        %% Connections
        Result --> RuleJudge
        Report --> LLMJudge
        RuleJudge --> M1 & M2 & M3
        LLMJudge --> M4 & M5 & M6 & M7
        M1 & M2 & M3 --> FinalScore
        M4 & M5 & M6 & M7 --> FinalScore
    end

    %% Link Phases
    Phase1 --> Phase2

```

---
## 4. Survey on Evaluation of LLM-based Agents

**Domain**: General Evaluation Methodologies and Frameworks

link: https://arxiv.org/abs/2503.16416

**Capability and Scenario Benchmarking Phase**
Evaluating agents requires building benchmarks from two dimensions. The first evaluates capabilities including multi-step planning, tool use, self-reflection, and memory management. The second evaluates application-specific and general scenarios by placing agents in simulated environments to test performance in real-world tasks.

**Multi-level Granular Evaluation Phase**
Evaluation frameworks analyze the complete interaction trajectory to diagnose execution quality. Evaluations occur at these levels:

1. **Stepwise Evaluation**: Examines individual actions or parameter selections for root cause analysis.
2. **Trajectory Assessment**: Compares the executed sequence of steps against the optimal path to evaluate decision logic and tool invocation order.
3. **Final Response Evaluation**: Uses model judges or objective metrics to assess output quality and consistency.
4. **Interactive Environment Testing**: Monitors agent responses to changing states through a simulation framework.

### Workflow Visualization

```mermaid
graph LR
    %% Style Definitions
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    %% === Phase 1: Setup and Environment ===
    subgraph Phase1 [Phase 1: Setup and Environment]
        Cap[1. Agent Capabilities]:::input
        Agent[2. Target Agent]:::phase1
        Bench[3. Benchmark Tasks]:::input
        Env[4. Simulated Environment]:::phase1
        
        Cap --> Agent
        Bench --> Env
        Agent <-->|Interactive Execution| Env
    end

    %% === Phase 2: Granular Evaluation ===
    subgraph Phase2 [Phase 2: Granular Evaluation]
        Trace[5. Execution Trajectory]:::input
        Step[6. Stepwise Assessment]:::phase2
        Traj[7. Trajectory Assessment]:::phase2
        Final[8. Final Response Eval]:::phase2
        Cost[9. Cost & Efficiency]:::phase2
        Safe[10. Safety & Compliance]:::phase2
        Judge[11. LLM-as-a-Judge]:::phase1
        
        %% Diverging flow from Trace
        Trace --> Step
        Trace --> Traj
        Trace --> Final
        Trace --> Cost
        Trace --> Safe
        
        %% Judge inputs
        Judge -.->|Scores| Step
        Judge -.->|Scores| Final
    end

    %% === Cross-Phase Connections ===
    Env -->|Generates| Trace
    
    %% === Output Section ===
    Report[12. Comprehensive Report]:::report
    
    %% Converging flow to Report
    Step --> Report
    Traj --> Report
    Final --> Report
    Cost --> Report
    Safe --> Report

```

---
## 5. MAJ-EVAL: Multi-Agent-as-Judge

**Domain**: General / Multi-dimensional Human Alignment

Link:https://arxiv.org/abs/2507.21028

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

    %% === Phase 1: Persona Construction ===
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

---
