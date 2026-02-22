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

---

## 7. MedChain: Continuous Clinical Decision-Making Agent Evaluation

**Domain**: Clinical Decision-Making and Continuous Interactive Evaluation

**Dynamic Interaction Testing**
A local model acts as a standardized patient and the target agent acts as a doctor. They engage in multi-turn dialogues to assess the agent's ability to dynamically gather information and provide personalized care.

**Continuous Execution and Hybrid Scoring**
Agents sequentially complete five tasks including triage, history-taking, examination, diagnosis, and treatment. The output of one stage serves as the input for the next to test error propagation. Scoring uses hybrid metrics where Intersection over Union evaluates the triage and treatment stages, while a large language model judge performs text matching and comprehensive scoring for the examination and diagnosis stages based on clinical standards.

```mermaid
graph LR
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Phase1 [Phase 1 Setup and Simulation]
        EHR["1. EHR<br/>Cases"]:::input
        SimUser["2. AI Patient<br/>Agent"]:::phase1
        Agent["3. Target Doctor<br/>Agent"]:::phase1
        Interaction["4. Dynamic<br/>Consultation"]:::phase1
        
        EHR --> SimUser
        SimUser <--> Interaction
        Agent <--> Interaction
    end

    subgraph Phase2 [Phase 2 Sequential Evaluation]
        Stages["5. Five Sequential<br/>Tasks"]:::input
        Output["6. Task<br/>Outputs"]:::phase2
        RuleEval["7. IoU and<br/>Accuracy"]:::phase2
        LLMEval["8. LLM Judge<br/>Scoring"]:::phase2
        ErrorCheck["9. Error Cascade<br/>Tracking"]:::phase2
        
        Interaction --> Stages
        Stages --> Output
        Output --> RuleEval
        Output --> LLMEval
        Output --> ErrorCheck
    end

    Metrics["10. Final<br/>Metrics"]:::report
    Report["11. Comprehensive<br/>Report"]:::report

    RuleEval --> Metrics
    LLMEval --> Metrics
    ErrorCheck --> Metrics
    Metrics --> Report
```

---

## 8. MedAgentBoard Comprehensive Medical Multi Agent Collaboration Evaluation

**Domain**: Medical Multimodal Tasks and Multi Agent Evaluation

**Heterogeneous Task and Benchmark Construction Phase**
The framework constructs four medical tasks including medical question answering medical record summary generation electronic health record prediction and clinical workflow automation. To evaluate system performance this benchmark tests various multi agent collaboration frameworks and introduces single large language models and task specific traditional machine learning models as strong baselines.

**Hybrid Metrics and Human Intervention Evaluation Phase**
Differentiated evaluation standards are adopted for tasks with distinct modalities and complexities. Multiple choice and predictive model tasks use objective quantitative metrics like accuracy or area under the receiver operating characteristic curve. Open ended question answering uses a large language model judge to evaluate semantic correctness and factual consistency. Clinical workflow automation tasks introduce a multidisciplinary expert team for manual review to assess code execution rate and clinical validity.

```mermaid
graph LR
    classDef phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,rx:5,ry:5;
    classDef phase2 fill:#fce4ec,stroke:#c2185b,stroke-width:2px,rx:5,ry:5;
    classDef input fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,rx:5,ry:5;
    classDef report fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,rx:10,ry:10;

    subgraph Phase1 [Phase 1 Task and Baseline Setup]
        Task["1. Diverse Medical<br/>Tasks"]:::input
        MultiAgent["2. Multi Agent<br/>Frameworks"]:::phase1
        SingleLLM["3. Single LLM<br/>Baselines"]:::phase1
        ConvML["4. Conventional<br/>ML Models"]:::phase1
        Exec["5. Execution<br/>Environment"]:::phase1
        
        Task --> MultiAgent
        Task --> SingleLLM
        Task --> ConvML
        MultiAgent --> Exec
        SingleLLM --> Exec
        ConvML --> Exec
    end

    subgraph Phase2 [Phase 2 Hybrid Evaluation]
        Out["6. Task<br/>Outputs"]:::input
        Obj["7. Objective<br/>Metrics"]:::phase2
        Judge["8. LLM<br/>Judge"]:::phase2
        Human["9. Expert<br/>Panel"]:::phase2
        Score["10. Final<br/>Scores"]:::phase2
        
        Exec --> Out
        Out --> Obj
        Out --> Judge
        Out --> Human
        Obj --> Score
        Judge --> Score
        Human --> Score
    end

    Report["11. Comprehensive<br/>Report"]:::report
    
    Score --> Report
```

---
