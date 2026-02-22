## 7. Medical LLM-as-a-Judge: Automated Clinical Summary Evaluation

**Domain** : Clinical Summarization and Automated Evaluation

Link: https://doi.org/10.1101/2025.04.22.25326219

**Benchmark Alignment & Single-Model Scoring**

This study employs Large Language Models (LLMs) as judges to evaluate the quality of medical record summaries. The evaluation uses the PDSQI-9 scale, validated by human experts, as the benchmark. By inputting the original records, candidate summaries, and scoring rubrics, the system prompts the LLM to generate multi-dimensional scores. Researchers then calculate the Intraclass Correlation Coefficient (ICC) between LLM and expert ratings to measure the consistency between machine and human judgment.

**Multi-Agent Collaboration & Strategy Optimization**

The research further introduces a multi-agent discussion framework. Agents are assigned specific roles—such as "high-score" or "low-score" biased evaluators—to engage in cross-debates regarding summary quality. A coordinator then synthesizes these perspectives into a consensus score. Additionally, the study tests zero-shot, few-shot, and preference optimization strategies to identify the automated evaluation approach that most closely aligns with human cognitive standards.
### Workflow Visualization

```mermaid
graph TD
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Phase1 [Phase 1: Data Preparation & Benchmark]
        Data["1. Clinical Data (EHR Notes & AI Summaries)"]:::input
        Rubric["2. PDSQI-9 Evaluation Rubric"]:::input
        Benchmark["3. Human Expert Benchmark"]:::phase1
        
        Data --> Benchmark
        Rubric --> Benchmark
    end

    subgraph Phase2 [Phase 2: AI Evaluation & Validation]
        Setup["4. Prompt Engineering & Setup"]:::phase2
        Models["5. AI Models (GPT-o3 / DeepSeek / Mixtral)"]:::phase2
        Outputs["6. LLM Outputs (Scores & Reasoning)"]:::phase2
        Validation["7. ICC Reliability Validation"]:::phase2
        Analysis["8. Error & Cost Analysis"]:::phase2
        CrossTask["9. Cross-Task Validation (ProbSum)"]:::phase2
        Report["10. Final Evaluation Report"]:::report
        
        Setup --> Models
        Models --> Outputs
        Outputs --> Validation
        Validation --> Analysis
        Analysis --> CrossTask
        CrossTask --> Report
    end

    %% Minimal Cross-Phase Connections
    Data --> Setup
    Rubric --> Setup
    Benchmark --> Validation
```

---
