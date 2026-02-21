## 7. MEDPI: Medical Interactive Agent Evaluation

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
        Task[1. Task Matrix]:::input
        Data[2. Patient Packets]:::input
        SimUser[3. AI Patient Agent]:::phase1
        Agent[4. Target Doctor Agent]:::phase1
        
        Task --> SimUser
        Data --> SimUser
        SimUser <--> Agent
    end

    subgraph Phase2 [Phase 2 Multidimensional Evaluation]
        Trace[5. Conversation Trajectory]:::input
        Rubric[6. Evaluation Framework]:::input
        Judge[7. AI Judge Committee]:::phase2
        Extract[8. Evidence Extraction]:::phase2
        Score[9. Dimension Scoring]:::phase2
        
        Agent --> Trace
        SimUser --> Trace
        Trace --> Judge
        Rubric --> Judge
        Judge --> Extract
        Extract --> Score
    end

    Metrics[10. Competency Metrics]:::report
    Report[11. Evaluation Report]:::report

    Score --> Metrics
    Score --> Report
```
