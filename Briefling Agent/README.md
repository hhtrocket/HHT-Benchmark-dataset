# Research Article Briefing Agent

A **LangGraph-based multi-agent system** for discovering and summarizing recent academic papers. Designed for Information Systems researchers studying **AI agent evaluation in healthcare and data science**.

---

## Purpose

Keeping up with rapidly growing academic literature is time-consuming. This agent automates the two most tedious steps:

1. **Discovery** — searches multiple academic databases for papers matching your topic and date range
2. **Summarization** — generates a structured, consistent briefing for each paper you select

The result is a set of ready-to-read briefings you can use for literature reviews, seminar prep, or research planning.

---

## Pipeline Overview

```
START
  │
  ▼
[Gate 1] Set search parameters
  │  date range · research topic · papers per batch
  ▼
Search academic papers  (Tavily — arXiv, Semantic Scholar, PubMed, ACM, IEEE, etc.)
  │
  ▼
[Gate 2a] Review papers in batches
  │  browse · select papers · or search again with a new topic
  ▼
[Gate 2b] Set briefing parameters
  │  focus prompt · word limit per briefing
  ▼
Generate structured briefings  (LLM)
  │
  ▼
[Gate 3] Review briefings
  │  approve · request revisions · or reselect papers
  ▼
END  →  saves  briefings_<timestamp>.md  +  meta.yaml
```

At every **Human Gate** the agent pauses, displays its output as rendered Markdown, and waits for your input before continuing.

---

## Briefing Format

Every generated briefing follows this fixed structure:

```
---
**Title:**  <full paper title>
**Domain:** <research domain, e.g. "Healthcare AI", "EHR Systems", "AI Agent Evaluation">

<Paragraph 1 — background, motivation, and the research problem addressed>

<Paragraph 2 — methods, key findings, and implications for the field>
---
```

---

## Setup

### 1. Install dependencies

```bash
pip install langchain-openai langgraph tavily-python pydantic typing-extensions pyyaml
```

### 2. Get API keys

| Key | Where to get it | Required |
|-----|----------------|----------|
| `LLM_API_KEY` | [openrouter.ai](https://openrouter.ai) (or your own LLM provider) | ✅ |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) — free tier available | ✅ |

### 3. Open the notebook

Open `research_briefing_agent.ipynb` in **Jupyter Lab**, **Jupyter Notebook**, or **Google Colab**.

---

## How to Use (Step-by-Step)

### Cell 2 — Paste your API keys

```python
os.environ["LLM_API_KEY"]    = "sk-or-..."          # your OpenRouter or LLM key
os.environ["LLM_BASE_URL"]   = "https://openrouter.ai/api/v1"
os.environ["TAVILY_API_KEY"] = "tvly-..."            # your Tavily key
```

### Cell 3 — Adjust configuration (optional)

```python
CFG = {
    "models": {
        "brief_agent": "openai/gpt-4o",   # change to any model on your provider
    },
    "default_date_from":        "2024-01",
    "default_date_to":          "2026-01",
    "default_topic":            "AI agent evaluation healthcare data science",
    "default_papers_per_batch": 5,         # 1–10 papers shown at a time
    "max_papers_to_fetch":      20,        # total papers fetched
    "default_briefing_prompt":  "summarize key contributions, methodology, and implications",
    "default_word_limit":       300,       # words per briefing
    "max_revisions":            3,
}
```

### Run all cells in order (Cells 1–9)

These set up the tools, state schema, node functions, and compile the graph. No interaction needed.

---

### Cell 10 — Interactive Agent Run

This is where you interact with the agent. Three gates will appear:

---

#### Gate 1 — Search Setup

The agent asks for your search parameters.

**Input format:**
```
<date_from> | <date_to> | <topic> | <papers_per_batch>
```

**Examples:**
```
2024-11 | 2026-01 | AI agent evaluation in clinical EHR systems | 5
2023-01 | 2026-01 | LLM-based agents for data science automation | 8
2024-06 | 2025-12 | patient safety AI agent healthcare | 5
```

Press **Enter** to use the defaults from `CFG`.

---

#### Gate 2a — Paper Review & Selection

The agent displays papers one batch at a time.

| What you want to do | What to type |
|---------------------|-------------|
| Select specific papers | `1,3,5` or `2 4` or `1-3` |
| See the next batch | `more` |
| Search with a different topic | `search: new topic keywords` |

**Examples:**
```
> 1,3,5
> more
> search: AI agent benchmark evaluation metrics healthcare 2025
```

---

#### Gate 2b — Briefing Parameters

Set what the briefing should focus on and how long it should be.

**Input format:**
```
<focus prompt> | <word limit>
```

**Examples:**
```
focus on evaluation methodology and clinical implications | 350
explain the agent architecture, benchmark design, and key results | 400
summarize contributions and highlight limitations | 250
```

Press **Enter** to use defaults (`summarize key contributions and methods | 300`).

---

#### Gate 3 — Final Review

The agent displays all generated briefings.

| What you want to do | What to type |
|---------------------|-------------|
| Approve and save | Press **Enter**, or type `approve` |
| Request revisions | Type your feedback, e.g. `make paragraph 2 more concise` |
| Go back to paper selection | `reselect` |

The agent will revise up to **3 times** before finalizing automatically.

---

### Cell 11 — Save Results

Saves two files to a timestamped folder (e.g. `20260224_143021/`):

| File | Contents |
|------|----------|
| `briefings_<timestamp>.md` | All briefings in Markdown format |
| `meta.yaml` | Run metadata: topic, date range, model, paper list, elapsed time |

---

## Example Session

```
Gate 1 input:
> 2024-11 | 2026-01 | AI agent evaluation in EHR clinical decision support | 5

Gate 2a input (after reviewing 5 papers):
> 1,4,5

Gate 2b input:
> explain evaluation framework, metrics used, and clinical validity | 350

Gate 3 input:
> approve
```

**Output briefing example:**

```
---
**Title:** Evaluating LLM-based Clinical Decision Support Agents on EHR Benchmarks
**Domain:** Healthcare AI

Recent advances in large language models have enabled AI agents capable of
reasoning over electronic health record data to support clinical decisions.
However, standardized evaluation frameworks for such agents remain scarce,
limiting reproducibility and clinical trust.

This paper proposes a multi-dimensional evaluation protocol covering
factual accuracy, reasoning consistency, and clinical safety across
five EHR benchmark datasets. Experiments on GPT-4 and Llama-3 agents
demonstrate that safety-critical metrics diverge significantly from
accuracy scores, underscoring the need for domain-specific benchmarks
in clinical AI deployment.
---
```

---

## Academic Sources Searched

The agent targets these platforms via Tavily:

- arXiv · Semantic Scholar · PubMed
- ACM Digital Library · IEEE Xplore
- Springer · Nature · ScienceDirect · Wiley
- ResearchGate · Google Scholar · PLOS · JAMA · BMJ

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `AssertionError: ⚠ Please fill in LLM_API_KEY` | Add your API key in Cell 2 |
| `Search failed` | Check your `TAVILY_API_KEY`; ensure internet access |
| LLM returns empty response | Try a different model in `CFG["models"]["brief_agent"]` |
| No papers found | Broaden your topic or extend the date range |
| Gate input not recognized | Follow the pipe-separated format exactly |

---

## Tech Stack

| Component | Library |
|-----------|---------|
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM calls | [LangChain OpenAI](https://github.com/langchain-ai/langchain) via [OpenRouter](https://openrouter.ai) |
| Web search | [Tavily](https://tavily.com) |
| Structured outputs | Pydantic v2 |
| Notebook interface | Jupyter / Google Colab |
