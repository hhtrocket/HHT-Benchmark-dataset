# Closing the Outreach Gap in Clinical Trial Recruitment with Multi-Agent LLM

## The Problem

Clinical trials are the foundation of evidence-based medicine — but the evidence base is constructed from a systematically skewed population. Black and Hispanic patients are consistently underrepresented, meaning that approved drugs and therapies are validated on data that may not generalize across racial and ethnic groups. This is not a peripheral concern: the FDA has formally flagged the issue, NIH mandated diversity reporting requirements in 2023, and the disparity remains largely unresolved.

The root causes are layered and mutually reinforcing. Economic barriers — including lost wages and transportation costs associated with repeated clinical visits — impose a disproportionate burden on minority patients employed in hourly-wage or service-sector positions. Historical distrust, shaped by documented abuses such as the Tuskegee Syphilis Study, has produced multigenerational wariness toward institutional medical research among Black communities. Overly restrictive eligibility criteria systematically exclude minority patients who carry higher rates of comorbidities, themselves a downstream consequence of decades of unequal healthcare access. Finally, physician communication bias compounds these structural factors: clinicians frequently fail to extend trial invitations to patients they implicitly assume will be non-compliant or unable to sustain follow-up schedules.

Most of these barriers demand systemic, policy-level intervention. One barrier, however, is uniquely addressable through AI: the information asymmetry layer. Many top-tier clinical trials already include provisions for transportation reimbursement, bilingual coordinators, and flexible visit scheduling. These provisions exist but are routinely buried within lengthy informed consent documents, inaccessible to patients with limited health literacy and unmentioned by time-constrained physicians. The enrollment failure in these cases is not a resource deficit — it is an information delivery failure.

---

## What the AI Agents Do

The proposed system is a LangGraph-based three-agent pipeline designed to address this information delivery failure at each stage of the recruitment process.

**Agent 1 — Clinical Parser** reads unstructured electronic health record notes and extracts a structured patient profile. Critically, the extraction extends beyond clinical diagnoses to capture social determinants of health signals embedded in free-text clinical documentation — notes indicating transportation barriers, missed follow-up appointments, language preference, or socioeconomic constraints. These SDOH tags form the input that drives downstream personalization.

**Agent 2 — Criteria Matcher** receives the structured patient profile and queries ClinicalTrials.gov through its public API, applying retrieval-augmented generation over trial descriptions to reason through complex inclusion and exclusion criteria. The agent handles temporal logic — determining, for instance, whether a surgical procedure performed six months prior triggers a three-month exclusion window — a category of reasoning where single-model systems have demonstrated hallucination rates as high as 55 percent in recent evaluations.

**Agent 3 — Cultural Communicator** is the primary research contribution. This agent receives the matched trial specification alongside the patient's SDOH profile and generates a concise, personalized outreach message through three distinct mechanisms:

1. **Information surfacing**: a grounded extraction sub-chain scans the full trial protocol for assistance provisions and positions them at the opening of the message rather than the closing.
2. **De-jargoning**: clinical terminology that activates distrust in minority populations — particularly language around randomization and placebo assignment — is translated into plain-language reassurances calibrated to a sixth-grade reading level.
3. **Behavioral nudging**: multi-step enrollment instructions are collapsed into a single low-friction call to action, reducing cognitive load at the decision moment rather than demanding that patients navigate institutional phone systems or paperwork independently.

A fairness auditor module runs post-hoc across the full pipeline to detect whether Agent 3's output quality is systematically weaker for any particular demographic stratum, operationalizing equity as a measurable property of the system rather than an aspirational design goal.

---

## Building Agent 3

The construction of Agent 3 presents challenges distinct from those of Agents 1 and 2. Matching tasks have ground truth; outreach generation does not. The failure modes are also different — not factual incorrectness in the traditional sense, but hallucinated reassurance, where the agent fabricates assistance provisions that do not exist in the trial protocol. A patient who acts on fabricated information and discovers the discrepancy at their first visit experiences a trust collapse that is likely irreversible.

To address this, Agent 3 is implemented as a three-step chain rather than a single prompt.

### Step 1: Grounded Provision Extraction

The first step is a dedicated provision extraction pass over the full protocol document, using a structured prompt that enumerates specific provision categories — transportation reimbursement, language support, visit timing flexibility, childcare assistance, and compensation — and requires exact textual quotation for any claim. Only provisions confirmed by this extraction pass are available to the message generation step.

This grounding constraint is non-negotiable: the message generator receives a confirmed provisions dictionary, not the full protocol text, and is explicitly instructed that it may not introduce any claim not present in that dictionary.

```
full_protocol_text
    |
    v
Extraction prompt: "Find and quote exact text for each category:
  - Transportation or travel reimbursement
  - Visit timing flexibility (weekends, evenings)
  - Language or interpreter support
  - Childcare assistance
  - Compensation or stipends
  - Remote or telehealth visit options
  If a category is not mentioned, return null."
    |
    v
confirmed_provisions: { transport: "...", language: null, ... }
```

### Step 2: Patient Concern Mapping

Given the patient's SDOH tags and demographic profile, the agent identifies and ranks the two or three concerns most likely to suppress enrollment for that specific patient. A patient flagged with transportation barriers and employment in hourly-wage work presents a different priority ordering than a patient flagged with limited English proficiency and documented wariness of medical institutions, even if both are matched to the same trial.

### Step 3: Message Generation

Message generation is conditioned jointly on the confirmed provisions dictionary and the ranked concern list. Key constraints enforced in the system prompt:

| Constraint | Implementation |
|---|---|
| 150-word ceiling | Messages exceeding this limit are returned for condensation |
| Single call to action | No alternative instructions or contact options |
| Sixth-grade reading level | Post-generation Flesch-Kincaid check; targeted rewrite triggered if exceeded |
| No fabricated claims | Generator receives only confirmed_provisions, not raw protocol |
| SDOH-conditional tone | Prompt instructions keyed to patient's specific barrier tags |

### De-jargoning: Key Term Translations

Specific clinical phrases that activate distrust require custom translations, not just simplified English:

| Clinical term | What minority patients may hear | Agent 3 translation |
|---|---|---|
| "Randomized double-blind placebo-controlled" | "50% chance I get no treatment" | "You will never lose your current treatment. You will either continue it or receive an additional new therapy on top." |
| "Experimental drug" | "Guinea pig" | "A therapy that has already passed initial safety reviews and is now being tested for effectiveness" |
| "Withdraw at any time" | Buried in legalese, ignored | Moved to the second sentence of the message |

### Behavioral Nudging Design

The nudging layer is implemented through conditional prompt instructions keyed to SDOH tags:

- Patient flagged as hourly-wage worker: message explicitly surfaces evening and weekend coordinator availability
- Patient with limited English proficiency: message written in documented language preference with explicit mention of a bilingual coordinator
- All patients: enrollment instruction collapsed to a single response CTA with an opt-out default framing

The goal is not persuasion through pressure but the reduction of enrollment friction at the precise points where minority patients are most likely to disengage.

---

## Evaluation Framework

Evaluating Agent 3 requires a framework that is reproducible and does not depend on deployment in a live clinical environment, where RCT conditions would be required to make causal claims about enrollment outcomes.

### Synthetic Patient Benchmark

The study constructs a synthetic patient profile benchmark comprising 200 profiles stratified across:

- Race and ethnicity: Black, Hispanic, White, Asian
- Socioeconomic status: low, mid, high
- SDOH barrier type: transportation, language, employment constraints, historical distrust

Profiles are generated using clinical note templates derived from MIMIC-IV. Each profile is passed through the full pipeline and the resulting outreach message is evaluated on four dimensions:

| Metric | Tool | Measures |
|---|---|---|
| Readability | Flesch-Kincaid grade level | Health literacy appropriateness |
| SDOH barrier coverage | Rule-based + LLM | Proportion of patient barriers addressed in message |
| Trust signal density | LLM-as-judge | Presence of language countering documented distrust triggers |
| Nudge structure | Rule-based | Single low-friction CTA present |

### LLM-as-Judge Protocol

Evaluation uses an LLM-as-judge ensemble comprising GPT-4o, Claude Sonnet, and Gemini, employing pairwise comparison between Agent 3-generated messages and standard recruitment templates:

1. Presentation order randomized to mitigate position bias
2. Judges produce chain-of-thought reasoning before scoring
3. Outputs calibrated against anchor examples with established human labels
4. 20 percent subset independently rated by a clinical communication expert
5. Intraclass correlation coefficients computed to validate ensemble against human judgment

### Fairness Audit

The fairness audit applies analysis of variance across demographic strata on each metric. The system is flagged if any group's coverage rate falls more than ten percentage points below the cross-group mean, making equitable performance a quantifiable pass/fail criterion rather than a narrative claim.

---

## Research Contributions

1. **System**: A complete three-agent clinical trial recruitment pipeline with a culturally-adaptive outreach agent as its primary novel component
2. **Benchmark**: A synthetic patient profile benchmark for reproducible evaluation of minority-specific outreach quality
3. **Evaluation framework**: An LLM-as-judge multi-ensemble protocol validated against human expert ratings, with explicit bias mitigation procedures

---

## Scope and Limitations

Agent 3 addresses the information asymmetry layer only. It cannot compensate for trials that offer no logistical support, override a patient's considered decision not to participate, or substitute for a bilingual human coordinator in complex enrollment conversations. The measurable claim is bounded: Agent 3-generated messages produce higher scores on readability, SDOH barrier coverage, and trust signal density than standard template outreach, as evaluated by a validated LLM-as-judge framework. The downstream effect on actual enrollment rates requires a randomized controlled trial that is outside the scope of this paper.

---

