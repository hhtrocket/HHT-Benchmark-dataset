## 7. Medical LLM-as-a-Judge: Automated Clinical Summary Evaluation

**Domain** : Clinical Summarization and Automated Evaluation

Link: https://doi.org/10.1101/2025.04.22.25326219

**Benchmark Alignment & Single-Model Scoring**
This study employs Large Language Models (LLMs) as judges to evaluate the quality of medical record summaries. The evaluation uses the PDSQI-9 scale, validated by human experts, as the benchmark. By inputting the original records, candidate summaries, and scoring rubrics, the system prompts the LLM to generate multi-dimensional scores. Researchers then calculate the Intraclass Correlation Coefficient (ICC) between LLM and expert ratings to measure the consistency between machine and human judgment.

**Multi-Agent Collaboration & Strategy Optimization**
The research further introduces a multi-agent discussion framework. Agents are assigned specific roles—such as "high-score" or "low-score" biased evaluators—to engage in cross-debates regarding summary quality. A coordinator then synthesizes these perspectives into a consensus score. Additionally, the study tests zero-shot, few-shot, and preference optimization strategies to identify the automated evaluation approach that most closely aligns with human cognitive standards.
### Workflow Visualization

```mermaid
graph LR
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Phase1 [Phase 1 Data and Benchmark Setup]
        Notes["1. Raw EHR<br/>Notes"]:::input
        Summaries["2. AI-Generated<br/>Summaries"]:::input
        Rubric["3. PDSQI-9<br/>Rubric"]:::input
        HumanEval["4. Human Expert<br/>Benchmark"]:::phase1
        
        Notes --> Summaries
        Summaries --> HumanEval
        Rubric --> HumanEval
    end

    subgraph Phase2 [Phase 2 AI Judging and Evaluation]
        SingleAgent["5. Single LLM<br/>Prompting"]:::phase2
        TunedAgent["6. Fine-Tuned LLM<br/>(SFT/DPO)"]:::phase2
        MultiAgent["7. Multi-Agent<br/>Framework"]:::phase2
        LLMScore["8. LLM Grading &<br/>Reasoning"]:::phase2
        Validation["9. ICC Reliability<br/>Validation"]:::phase2
        
        Notes --> SingleAgent
        Summaries --> SingleAgent
        Rubric --> SingleAgent
        
        Notes --> TunedAgent
        Summaries --> TunedAgent
        Rubric --> TunedAgent
        
        Notes --> MultiAgent
        Summaries --> MultiAgent
        Rubric --> MultiAgent
        
        SingleAgent --> LLMScore
        TunedAgent --> LLMScore
        MultiAgent --> LLMScore
        
        LLMScore --> Validation
        HumanEval --> Validation
    end

    Metrics["10. Evaluation<br/>Metrics (ICC)"]:::report
    Report["11. Automated<br/>Evaluation Report"]:::report

    Validation --> Metrics
    Validation --> Report
```

---
