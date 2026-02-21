## 6. MEDPI: Medical Interactive Agent Evaluation

**Domain**: Medical Dialogue Simulation and Clinical Evaluation

**Environment Construction and Dialogue Simulation Phase**
The framework utilizes synthetic electronic health records to construct patient packets. AI patients are instantiated based on these patient packets, integrated with memory and emotion systems. The evaluation task is defined by a matrix comprising encounter reasons and encounter objectives. The target agent acts as a doctor, conducting multi-turn text-based consultations with the AI patient to generate an interaction trajectory.

**Multidimensional Fine-Grained Evaluation Phase**
The evaluation framework contains 105 fine-grained dimensions mapped to medical competency categories. A committee of large language model judges conducts internal discussions on the dialogue trajectories and extracts evidence. Based on the discussion results, the judges assign discrete scores from one to four across all dimensions. The system ultimately outputs a comprehensive evaluation report containing quantitative scores and associated evidence.

### Workflow Visualization

```mermaid
graph LR
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Phase1 [Phase 1 Setup and Simulation]
        Task["1. Task<br/>Matrix"]:::input
        Data["2. Patient<br/>Packets"]:::input
        SimUser["3. AI Patient<br/>Agent"]:::phase1
        Agent["4. Target Doctor<br/>Agent"]:::phase1
        
        Task --> SimUser
        Data --> SimUser
        SimUser <--> Agent
    end

    subgraph Phase2 [Phase 2 Multidimensional Evaluation]
        Trace["5. Conversation<br/>Trajectory"]:::input
        Rubric["6. Evaluation<br/>Framework"]:::input
        Judge["7. AI Judge<br/>Committee"]:::phase2
        Extract["8. Evidence<br/>Extraction"]:::phase2
        Score["9. Dimension<br/>Scoring"]:::phase2
        
        Agent --> Trace
        SimUser --> Trace
        Trace --> Judge
        Rubric --> Judge
        Judge --> Extract
        Extract --> Score
    end

    Metrics["10. Competency<br/>Metrics"]:::report
    Report["11. Evaluation<br/>Report"]:::report

    Score --> Metrics
    Score --> Report
```

7. MedChain: Continuous Clinical Decision-Making Agent Evaluation

Domain: Clinical Decision-Making and Continuous Interactive Evaluation
Dynamic Interaction Testing: A local model acts as a standardized patient and the target agent acts as a doctor. They engage in multi-turn dialogues to assess the agent ability to dynamically gather information and provide personalized care.

Continuous Execution and Hybrid Scoring: Agents sequentially complete five tasks including triage, history-taking, examination, diagnosis and treatment. The output of one stage serves as the input for the next to test error propagation. Scoring uses hybrid metrics where Intersection over Union evaluates the triage and treatment stages. Meanwhile a large language model judge performs text matching and comprehensive scoring for the examination and diagnosis stages based on clinical standards.
