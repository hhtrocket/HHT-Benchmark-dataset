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

    subgraph P1 [Phase 1: Setup]
        direction TB
        N1["1. EHR Notes & Summaries"]:::input
        N2["2. PDSQI-9 Rubric"]:::input
        N3["3. Human Expert Benchmark"]:::phase1
        
        N1 --> N3
        N2 --> N3
    end

    subgraph P2 [Phase 2: AI Evaluation]
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
graph TB
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph P1 [Phase 1 Agent Optimization]
        N1["1. EHR Tasks"]:::input
        N2["2. Prompt Engineering"]:::phase1
        N3["3. Tool Calling"]:::phase1
        N4["4. Memory Feedback"]:::phase1
        
        N1 --> N2
        N2 --> N3
        N3 --> N4
    end

    subgraph P2 [Phase 2 Execution and Evaluation]
        N5["5. Clinical Execution"]:::phase2
        N6["6. Custom Evaluation Functions"]:::phase2
        N7["7. Logic Verification"]:::phase2
        N8["8. Success Rate Metric"]:::report
        
        N5 --> N6
        N6 --> N7
        N7 --> N8
    end

    N4 --> N5
```

---
