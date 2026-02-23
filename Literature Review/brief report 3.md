## 11. Medical LLM-as-a-Judge: Automated Clinical Summary Evaluation

**Domain** : Clinical Summarization and Automated Evaluation

Link: https://doi.org/10.1101/2025.04.22.25326219

**Benchmark Alignment & Single-Model Scoring**

This study employs Large Language Models (LLMs) as judges to evaluate the quality of medical record summaries. The evaluation uses the PDSQI-9 scale, validated by human experts, as the benchmark. By inputting the original records, candidate summaries, and scoring rubrics, the system prompts the LLM to generate multi-dimensional scores. Researchers then calculate the Intraclass Correlation Coefficient (ICC) between LLM and expert ratings to measure the consistency between machine and human judgment.

**Multi-Agent Collaboration & Strategy Optimization**

The research further introduces a multi-agent discussion framework. Agents are assigned specific roles—such as "high-score" or "low-score" biased evaluators—to engage in cross-debates regarding summary quality. A coordinator then synthesizes these perspectives into a consensus score. Additionally, the study tests zero-shot, few-shot, and preference optimization strategies to identify the automated evaluation approach that most closely aligns with human cognitive standards.
### Workflow Visualization

```mermaid
flowchart TB
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Setup
        direction TB
        N1["1. EHR Notes & Summaries"]:::input
        N2["2. PDSQI-9 Rubric"]:::input
        N3["3. Human Expert Benchmark"]:::phase1
        
        N1 --> N3
        N2 --> N3
    end

    subgraph  AI Evaluation
        direction TB
        N4["4. Prompt Engineering"]:::phase2
        N5["5. Single & Multi-Agent Setup"]:::phase2
        N6["6. AI Models Inference"]:::phase2
        N7["7. Output: Scores & Reasoning"]:::phase2
        N8["8. ICC Reliability Validation"]:::phase2
        N9["9. Error & Cost Analysis"]:::phase2
        N10["10. Cross-Task Validation"]:::phase2
        N11["11. Final Evaluation Report"]:::report
        
        N4 --> N5
        N5 --> N6
        N6 --> N7
        N7 --> N8
        N8 --> N9
        N9 --> N10
        N10 --> N11
    end

    %% Minimal Cross-Phase Connections
    N1 --> N4
    N2 --> N4
    N3 -.->|Gold Standard| N8
```

---
## 12.MedAgent Bench v2: Medical LLM Agent Design
**Domain: EHR Agent Evaluation**

link：https://www.worldscientific.com/doi/10.1142/9789819824755_0025

**Agent Construction & Optimization**

This phase focuses on optimizing medical agents by refining prompt engineering and tool integration. The system requires agents to generate step-by-step plans before taking any action. Agents are equipped with specialized tools for querying FHIR standard APIs, performing mathematical calculations, and formatting outputs. Additionally, a memory feedback mechanism was introduced, allowing agents to extract lessons from past mistakes and update their system prompts, enabling strategy adaptation across different tasks.

**Clinical Task Testing & Evaluation**

The evaluation goes beyond standard benchmarks by introducing 300 new, complex, multi-step clinical tasks developed with the help of human doctors to test generalization. For each task, the system uses custom-coded evaluation functions to automatically verify the agent's clinical reasoning logic and the accuracy of its API calls. The core metric for the final assessment is the First-Trial Success Rate.
### Workflow Visualization

```mermaid
graph TD
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef phase3 fill:#fff3e0,stroke:#e65100,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Construction 

        direction TB
        N1["1. Prompt Engineering<br/>for Chain of Thought"]:::phase1
        N2["2. Medical API &<br/>Calculation Tools Integration"]:::phase1
        N3["3. Extract Errors &<br/>Update Memory Rules"]:::phase1
        
        N1 --> N2
        N2 --> N3
    end

    subgraph Benchmark

        direction TB
        N4["4. 300 New Complex<br/>Clinical Tasks"]:::input
        N5["5. Agent-EHR<br/>Environment Interaction"]:::phase2
        
        N4 --> N5
    end

    subgraph Verification

        direction TB
        N6["6. Inject Custom<br/>Evaluation Functions"]:::phase3
        N7["7. Verify Clinical<br/>Timing & Dosing Logic"]:::phase3
        N8["8. Check API<br/>Execution Fidelity"]:::phase3
        N9["9. Output First-Try<br/>Success Rate"]:::report
        N10["10. Assess System<br/>Cost & Latency"]:::report
        
        N6 --> N7
        N6 --> N8
        N7 & N8 --> N9
        N9 --> N10
    end

    N3 --> N5
    N5 --> N6
```

---
## 13. RadOnc-GPT: Clinical Outcomes Labeling Agent
**Domain: Clinical Outcomes Labeling**

Link ：https://arxiv.org/html/2509.25540v1

**Two-Level Task Evaluation**

This study uses a two-level strategy to evaluate the medical AI agent. The first level focuses on structured data extraction,testing how accurately the agent retrieves basic patient information and radiotherapy plans from the database. These results are checked directly against the source data. The second level involves "complex clinical outcome labeling." Here, the agent must analyze both structured records and unstructured clinical notes to independently identify conditions like radiation necrosis or cancer recurrence.

**Expert Review & Data Auditing**

When the agent’s results in the second level differ from existing human-made labels in the registry, independent doctors are brought in to judge the discrepancy. These experts categorize each difference as either areal model error or a baseline erro in the original data. This evaluation process does more than just measure the agent's performance; it also acts as a reverse audit, helping to identify and correct many human labeling errors or omissions in existing medical databases.
### Workflow Visualization

```mermaid
graph TD
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Two Tier Evaluation
        direction TB
        N1["1. Database and EHR Input"]:::input
        N2["2. Tier 1 Structured Extraction"]:::phase1
        N3["3. Tier 2 Complex Labeling"]:::phase1
        
        N1 --> N2
        N2 --> N3
    end

    subgraph Adjudication and Audit
        direction TB
        N4["4. Compare with Ground Truth"]:::phase2
        N5["5. Independent Expert Adjudication"]:::phase2
        N6["6. Categorize Model Errors"]:::phase2
        N7["7. Categorize Registry Errors"]:::phase2
        N8["8. Final Accuracy Metrics"]:::report
        
        N4 --> N5
        N5 --> N6
        N5 --> N7
        N6 & N7 --> N8
    end

    N3 --> N4
```

---
## 14. DSAEval: Data Science Agent Evaluation
**Domain: Data Science Agent Evaluation**

Link: https://arxiv.org/pdf/2601.13591

**Multimodal Interaction & Task Execution**

The system creates a multi-round query environment based on real-world datasets. Agents receive multimodal inputs (both text and visuals), simulating the iterative process of an actual data science project. They are required to step-by-step generate reasoning logic, executable code, and final results.

**Multi-Dimensional Judge Evaluation**

The evaluation framework employs an LLM-as-a-judge to score the agent’s entire output trajectory across three dimensions: reasoning, code quality, and final outcomes. By moving beyond simple "single-answer" comparisons, this mechanism fully quantifies the agent's comprehensive performance when solving open-ended data science problems.

```mermaid
graph LR
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Environment Setup
        direction LR
        N1["1. Real World Datasets<br/>Text and Vision"]:::input
        N2["2. Multimodal<br/>Perception"]:::phase1
        N3["3. Multi Query<br/>Iterative Interaction"]:::phase1
        N4["4. Code and Reasoning<br/>Generation"]:::phase1
        N5["5. Execution Outputs<br/>and Trajectories"]:::phase1
        
        N1 --> N2
        N2 --> N3
        N3 --> N4
        N4 --> N5
    end

    subgraph Complex Evaluation
        direction LR
        N6["6. LLM as a Judge<br/>System"]:::phase2
        N7["7. Dimension 1<br/>Reasoning Logic"]:::phase2
        N8["8. Dimension 2<br/>Code Quality"]:::phase2
        N9["9. Dimension 3<br/>Final Results"]:::phase2
        N10["10. Trajectory Scoring<br/>and Aggregation"]:::phase2
        N11["11. Comprehensive<br/>Evaluation Report"]:::report
        
        N6 --> N7
        N6 --> N8
        N6 --> N9
        N7 & N8 & N9 --> N10
        N10 --> N11
    end

    N5 --> N6
```

---

## 15. Data Interpreter: An LLM Agent For Data Science
**Field: Data Science Agent Evaluation**

Link：https://aclanthology.org/2025.findings-acl.1016.pdf

**Multi-Task Benchmarking**

This study establishes a comprehensive evaluation system covering data analysis, machine learning, mathematical reasoning, and open-ended tasks. Testing is conducted on real-world datasets and multiple standardized benchmarks, such as Kaggle competition data and the MATH dataset. The process requires the agent to independently manage the entire workflow—from data preprocessing and feature engineering to model training and evaluation—to test its integrated capability in handling multi-step, complex data science tasks.

**Multi-Dimensional Quantitative Evaluation**

The evaluation framework combines task completion rates with normalized performance scores to calculate a comprehensive final grade. Beyond just checking final accuracy, the system strictly monitors execution time and resource consumption costs. Furthermore, the study uses various ablation experiments to independently verify the effectiveness of core modules—such as code execution, iterative graph refinement, and programmable node generation—in automated error correction and long-context management.

```mermaid
graph LR
    %% Style Definitions
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef decision fill:#ffffff,stroke:#333,stroke-width:2px,shape:diamond;
    classDef score fill:#ffcdd2,stroke:#c62828,stroke-width:2px,rx:50,ry:50;
    classDef report fill:#e0e0e0,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% === Benchmark Execution ===
    subgraph Phase1 ["Phase 1: Benchmark Execution and Trajectory Capture"]
        Tasks["1. Multi Domain Benchmarks<br/>Math ML and Open Tasks"]:::input
        Agent["2. Target Agent Execution"]:::phase1
        Trajectory["3. Execution Trajectory<br/>Logs and Outputs"]:::input

        Tasks --> Agent
        Agent -->|Record Process| Trajectory
    end

    %% ===  Metric Scoring Logic ===
    subgraph Phase2 ["Phase 2: Dual Metric Verification Logic"]
        StepCheck{"4. Step Execution<br/>Valid and Compliant?"}:::decision
        CR(("5. Completion<br/>Rate Score")):::score
        PerfCheck{"6. Raw Task Metrics<br/>Standardized?"}:::decision
        NPS(("7. Normalized<br/>Performance Score")):::score
        CS(("8. Comprehensive<br/>Weighted Score")):::score

        Trajectory -->|Extract Steps| StepCheck
        StepCheck --"Yes / Partial / No"--> CR
        
        Trajectory -->|Extract Results| PerfCheck
        PerfCheck --"Normalize to 0-1 Scale"--> NPS
        
        CR & NPS -->|Aggregate| CS
    end

    %% === Analysis ===
    subgraph Phase3 ["Phase 3: Deep Analysis and Profiling"]
        Efficiency["9. Cost and Latency<br/>Profiling"]:::phase2
        Report["10. Final Evaluation<br/>Report"]:::report

        CS --> Efficiency
        Efficiency --> Report
    end
```

---
## 16. FDABench: Data Agent Benchmark
**Domain: Heterogeneous Data Agent Evaluation**

Link：https://arxiv.org/pdf/2509.02473

**Heterogeneous Data Environment & Multi-Source Querying**

This study establishes a multi-source data lake testing environment containing both structured and unstructured data. Agents receive complex analytical instructions and must independently coordinate LLMs and external tools. They perform cross-modal retrieval and joint queries across text, images, and relational databases to generate a complete data analysis trajectory.

**Multi-Granularity Verification & Performance Evaluation**

The system performs rigorous scoring by comparing the agent's intermediate query steps against its final outputs. The evaluation framework independently breaks down and verifies the accuracy of tool calls, the logical coherence of cross-modal data integration, and the correctness rate of the final data solution. This benchmark effectively quantifies the reasoning bottlenecks of existing models when processing heterogeneous data.

```mermaid
graph LR
    %% Style Definitions
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px;
    classDef decision fill:#ffffff,stroke:#333,stroke-width:2px,shape:diamond;
    classDef score fill:#ffcdd2,stroke:#c62828,stroke-width:2px,rx:50,ry:50;
    classDef report fill:#e0e0e0,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;

    %% === Execution ===
    subgraph Phase1 ["Phase 1: Execution and Trajectory Capture"]
        Query["1. Analytical Query<br/>(User Input)"]:::input
        DataLake["2. Data Lake<br/>(SQL, Text, Vision)"]:::input
        
        Agent["3. Target Agent<br/>(Student)"]:::phase1
        Routing["4. Tool Routing &<br/>Cross-Modal Retrieval"]:::phase1
        
        Trajectory["5. Execution Trajectory<br/>(Steps + Final Answer)"]:::input

        Query --> Agent
        DataLake --> Agent
        Agent -->|Decompose| Routing
        Routing -->|Generate| Trajectory
    end

    %% === Multi-Granularity Evaluation ===
    subgraph Phase2 ["Phase 2: Granular Verification Logic"]
        StepCheck{"6. Tool & Logic<br/>Accurate?"}:::decision
        FinalCheck{"7. Final Answer<br/>Correct?"}:::decision
        Bottleneck["8. Bottleneck Diagnosis<br/>(Routing / Retrieval Error)"]:::phase2

        Trajectory -->|Extract Steps| StepCheck
        StepCheck --"No (Step Failed)"--> Bottleneck
        StepCheck --"Yes (Step Passed)"--> FinalCheck
    end

    %% === Final Assessment ===
    subgraph Phase3 ["Phase 3: Scoring and Reporting"]
        M1(("9. Tool Execution<br/>Score")):::score
        M2(("10. End-to-End<br/>Accuracy")):::score
        Report["11. Diagnostic<br/>Evaluation Report"]:::report

        Bottleneck --> M1
        StepCheck -.-> M1
        FinalCheck --"Yes / No"--> M2
        
        M1 --> Report
        M2 --> Report
    end
```

---
