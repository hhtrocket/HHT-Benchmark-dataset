# %% [markdown]
# # 6. Thought Source
# **Category:** AI Agent Core Capabilities
#
# **Source:** [OpenBioLink / ThoughtSource](https://github.com/OpenBioLink/ThoughtSource)
#
# **Description:** Designed to enhance agent reasoning capabilities using
# Chain-of-Thought (CoT) data, teaching models to think through steps before answering.
#
# **Data Content:** A collection of triplets consisting of Questions, Detailed
# Rationales (intermediate reasoning steps), and Final Answers across 14+ source datasets.
#
# **Paper:** [ThoughtSource: A central hub for large language model reasoning data](https://arxiv.org/abs/2301.11596)

# %% [markdown]
# ## 1. Setup

# %%
# Install dependencies (uncomment if needed)
# !pip install datasets pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import load_dataset

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["figure.dpi"] = 100

# %% [markdown]
# ## 2. Dataset Overview
#
# ThoughtSource unifies **14+ datasets** across 3 reasoning domains into a common
# (Question, Chain-of-Thought, Answer) schema. Here we load 4 representative
# source datasets directly from HuggingFace:
#
# | Dataset | Domain | CoT Field | Records |
# |---------|--------|-----------|---------|
# | **GSM8K** | Math | answer (contains step-by-step + final) | ~8.8k |
# | **AQUA-RAT** | Math | `rationale` (explicit reasoning) | ~98k |
# | **CommonsenseQA** | General QA | (ThoughtSource adds generated CoT) | ~12k |
# | **OpenBookQA** | Science | (ThoughtSource adds generated CoT) | ~6k |
#
# The full ThoughtSource collection also includes: WorldTree, EntailmentBank,
# StrategyQA, QED, MedQA, MedMCQA, MMLU, PubMedQA, ASDIV, MAWPS, SVAMP.

# %% [markdown]
# ## 3. Data Loading

# %%
print("Loading GSM8K (math reasoning with step-by-step solutions)...")
ds_gsm8k = load_dataset("gsm8k", "main")

print("Loading AQUA-RAT (math with explicit rationales)...")
ds_aqua = load_dataset("aqua_rat", "raw")

print("Loading CommonsenseQA (multiple-choice commonsense)...")
ds_csqa = load_dataset("commonsense_qa")

print("Loading OpenBookQA (science multiple-choice)...")
ds_obqa = load_dataset("allenai/openbookqa", "main")

print("All datasets loaded!")

# %%
# Show sizes per split
for name, ds in [("GSM8K", ds_gsm8k), ("AQUA-RAT", ds_aqua),
                 ("CommonsenseQA", ds_csqa), ("OpenBookQA", ds_obqa)]:
    splits_info = {k: len(v) for k, v in ds.items()}
    print(f"{name:15s} {splits_info}")

# %% [markdown]
# ## 4. Data Schema & Samples

# %%
# GSM8K schema — answer field contains rationale + "#### final_answer"
print("=== GSM8K ===")
print(f"Columns: {ds_gsm8k['train'].column_names}\n")

for i in range(2):
    item = ds_gsm8k["train"][i]
    print(f"--- Example {i+1} ---")
    print(f"Question: {item['question']}")
    print(f"Answer (rationale + final):\n{item['answer']}")
    print()

# %%
# AQUA-RAT schema — has explicit 'rationale' field
print("=== AQUA-RAT ===")
print(f"Columns: {ds_aqua['train'].column_names}\n")

item = ds_aqua["train"][0]
print(f"Question: {item['question']}")
print(f"Options: {item['options']}")
print(f"Rationale: {item['rationale']}")
print(f"Correct: {item['correct']}")

# %%
# CommonsenseQA schema — multiple choice, no built-in CoT
print("\n=== CommonsenseQA ===")
print(f"Columns: {ds_csqa['train'].column_names}\n")

item = ds_csqa["train"][0]
print(f"Question: {item['question']}")
print(f"Concept: {item['question_concept']}")
print(f"Choices: {list(zip(item['choices']['label'], item['choices']['text']))}")
print(f"Answer: {item['answerKey']}")

# %%
# OpenBookQA schema — science multiple choice
print("\n=== OpenBookQA ===")
print(f"Columns: {ds_obqa['train'].column_names}\n")

item = ds_obqa["train"][0]
print(f"Question: {item['question_stem']}")
print(f"Choices: {list(zip(item['choices']['label'], item['choices']['text']))}")
print(f"Answer: {item['answerKey']}")

# %% [markdown]
# ## 5. Exploratory Data Analysis
#
# ### 5.1 Dataset Sizes

# %%
size_data = {
    "GSM8K": sum(len(v) for v in ds_gsm8k.values()),
    "AQUA-RAT": sum(len(v) for v in ds_aqua.values()),
    "CommonsenseQA": sum(len(v) for v in ds_csqa.values()),
    "OpenBookQA": sum(len(v) for v in ds_obqa.values()),
}

plt.figure(figsize=(8, 5))
bars = plt.bar(size_data.keys(), size_data.values(),
               color=["steelblue", "coral", "mediumseagreen", "orchid"])
plt.title("Total Records per Dataset")
plt.ylabel("Number of Records")
for bar, val in zip(bars, size_data.values()):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
             f"{val:,}", ha="center", fontsize=10)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.2 GSM8K: Rationale Analysis
#
# In GSM8K, the `answer` field contains step-by-step reasoning followed by
# `#### <final_answer>`. We can parse this to study rationale characteristics.

# %%
df_gsm = ds_gsm8k["train"].to_pandas()

# Parse rationale and final answer
df_gsm["rationale"] = df_gsm["answer"].apply(lambda x: x.split("####")[0].strip())
df_gsm["final_answer"] = df_gsm["answer"].apply(
    lambda x: x.split("####")[1].strip() if "####" in x else ""
)
df_gsm["rationale_len"] = df_gsm["rationale"].apply(len)
df_gsm["rationale_steps"] = df_gsm["rationale"].apply(lambda x: x.count("\n") + 1)
df_gsm["question_len"] = df_gsm["question"].apply(len)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].hist(df_gsm["rationale_steps"], bins=range(1, 15), color="steelblue",
             edgecolor="white", align="left")
axes[0].set_title("GSM8K: Number of Reasoning Steps")
axes[0].set_xlabel("Steps")
axes[0].set_ylabel("Frequency")

axes[1].hist(df_gsm["rationale_len"], bins=50, color="coral", edgecolor="white")
axes[1].set_title("GSM8K: Rationale Length (chars)")
axes[1].set_xlabel("Character Count")

axes[2].scatter(df_gsm["question_len"], df_gsm["rationale_len"],
                alpha=0.1, s=5, color="mediumseagreen")
axes[2].set_title("Question Length vs Rationale Length")
axes[2].set_xlabel("Question Length (chars)")
axes[2].set_ylabel("Rationale Length (chars)")

plt.tight_layout()
plt.show()

print(f"Reasoning steps - Mean: {df_gsm['rationale_steps'].mean():.1f}, "
      f"Median: {df_gsm['rationale_steps'].median():.0f}, "
      f"Max: {df_gsm['rationale_steps'].max()}")
print(f"Rationale length - Mean: {df_gsm['rationale_len'].mean():.0f} chars, "
      f"Max: {df_gsm['rationale_len'].max()}")

# %% [markdown]
# ### 5.3 AQUA-RAT: Rationale Analysis

# %%
df_aqua = ds_aqua["train"].to_pandas()

df_aqua["rationale_len"] = df_aqua["rationale"].apply(len)
df_aqua["question_len"] = df_aqua["question"].apply(len)
df_aqua["rationale_steps"] = df_aqua["rationale"].apply(lambda x: x.count("\n") + 1)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_aqua["rationale_len"], bins=50, color="coral", edgecolor="white")
axes[0].set_title("AQUA-RAT: Rationale Length (chars)")
axes[0].set_xlabel("Character Count")
axes[0].set_ylabel("Frequency")

# Answer distribution
ans_counts = df_aqua["correct"].value_counts().sort_index()
axes[1].bar(ans_counts.index, ans_counts.values, color="steelblue")
axes[1].set_title("AQUA-RAT: Correct Answer Distribution")
axes[1].set_xlabel("Answer Choice")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.show()

print(f"Rationale length - Mean: {df_aqua['rationale_len'].mean():.0f} chars, "
      f"Max: {df_aqua['rationale_len'].max()}")
print(f"Rationale steps - Mean: {df_aqua['rationale_steps'].mean():.1f}")

# %% [markdown]
# ### 5.4 Question Length Comparison Across Datasets

# %%
q_lengths = {
    "GSM8K": ds_gsm8k["train"].to_pandas()["question"].apply(len),
    "AQUA-RAT": df_aqua["question_len"],
    "CommonsenseQA": ds_csqa["train"].to_pandas()["question"].apply(len),
    "OpenBookQA": ds_obqa["train"].to_pandas()["question_stem"].apply(len),
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
colors = ["steelblue", "coral", "mediumseagreen", "orchid"]

for ax, (name, lengths), color in zip(axes.flat, q_lengths.items(), colors):
    ax.hist(lengths, bins=40, color=color, edgecolor="white", alpha=0.8)
    ax.set_title(f"{name}\nMean={lengths.mean():.0f} chars, Median={lengths.median():.0f}")
    ax.set_xlabel("Character Count")
    ax.set_ylabel("Frequency")

plt.suptitle("Question Length Distribution Across Datasets", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.5 CommonsenseQA: Answer & Concept Distribution

# %%
df_csqa = ds_csqa["train"].to_pandas()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Answer key distribution
ans_counts = df_csqa["answerKey"].value_counts().sort_index()
axes[0].bar(ans_counts.index, ans_counts.values, color="mediumseagreen")
axes[0].set_title("CommonsenseQA: Answer Key Distribution")
axes[0].set_xlabel("Answer Key")
axes[0].set_ylabel("Count")

# Top question concepts
top_concepts = df_csqa["question_concept"].value_counts().head(20)
axes[1].barh(range(len(top_concepts)), top_concepts.values, color="orchid")
axes[1].set_yticks(range(len(top_concepts)))
axes[1].set_yticklabels(top_concepts.index, fontsize=8)
axes[1].invert_yaxis()
axes[1].set_title("Top 20 Question Concepts")
axes[1].set_xlabel("Count")

plt.tight_layout()
plt.show()

print(f"Unique question concepts: {df_csqa['question_concept'].nunique()}")

# %% [markdown]
# ### 5.6 CoT Availability: With vs Without Rationales

# %%
cot_status = pd.DataFrame({
    "Dataset": ["GSM8K", "AQUA-RAT", "CommonsenseQA", "OpenBookQA"],
    "Has Built-in CoT": ["Yes (in answer)", "Yes (rationale field)", "No", "No"],
    "ThoughtSource Adds": ["Unified format", "Unified format", "Generated CoT", "Generated CoT"],
    "Domain": ["Math", "Math", "General QA", "Science"],
    "Train Size": [len(ds_gsm8k["train"]), len(ds_aqua["train"]),
                   len(ds_csqa["train"]), len(ds_obqa["train"])],
})
print(cot_status.to_string(index=False))

# %% [markdown]
# ### 5.7 GSM8K vs AQUA-RAT: Rationale Depth Comparison

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Steps comparison
axes[0].hist(df_gsm["rationale_steps"], bins=range(1, 15), alpha=0.6,
             label="GSM8K", color="steelblue", edgecolor="white", align="left")
axes[0].hist(df_aqua["rationale_steps"].clip(upper=14), bins=range(1, 15), alpha=0.6,
             label="AQUA-RAT", color="coral", edgecolor="white", align="left")
axes[0].set_title("Number of Reasoning Steps")
axes[0].set_xlabel("Steps")
axes[0].set_ylabel("Frequency")
axes[0].legend()

# Length comparison (normalized)
axes[1].hist(df_gsm["rationale_len"], bins=50, alpha=0.6, density=True,
             label="GSM8K", color="steelblue", edgecolor="white")
axes[1].hist(df_aqua["rationale_len"], bins=50, alpha=0.6, density=True,
             label="AQUA-RAT", color="coral", edgecolor="white")
axes[1].set_title("Rationale Length Distribution (normalized)")
axes[1].set_xlabel("Character Count")
axes[1].set_ylabel("Density")
axes[1].legend()

plt.tight_layout()
plt.show()

print("Comparison of reasoning depth:")
comparison = pd.DataFrame({
    "Metric": ["Mean steps", "Median steps", "Mean length (chars)", "Median length (chars)"],
    "GSM8K": [df_gsm["rationale_steps"].mean(), df_gsm["rationale_steps"].median(),
              df_gsm["rationale_len"].mean(), df_gsm["rationale_len"].median()],
    "AQUA-RAT": [df_aqua["rationale_steps"].mean(), df_aqua["rationale_steps"].median(),
                 df_aqua["rationale_len"].mean(), df_aqua["rationale_len"].median()],
})
print(comparison.round(1).to_string(index=False))

# %% [markdown]
# ## 6. Key Observations
#
# 1. **Unified schema:** ThoughtSource standardizes 14+ datasets into a common
#    (Question, CoT, Answer) format, enabling cross-domain reasoning research.
#
# 2. **Explicit vs. generated CoT:** Math datasets (GSM8K, AQUA-RAT) include
#    human-written rationales, while QA datasets (CommonsenseQA, OpenBookQA)
#    rely on LLM-generated chains added by ThoughtSource.
#
# 3. **Reasoning depth varies:** GSM8K averages more structured multi-step
#    reasoning, while AQUA-RAT rationales tend to be shorter and more formulaic.
#
# 4. **Scale difference:** AQUA-RAT (~97k) is much larger than GSM8K (~7.5k),
#    offering quantity vs. quality tradeoffs for training.
#
# 5. **Research relevance (IS/AI):**
#    - **Reasoning enhancement:** Fine-tune agents to produce step-by-step rationales
#    - **Explainability:** Train models that show their work, not just final answers
#    - **Cross-domain transfer:** Study whether CoT reasoning transfers across domains
#    - **Human vs. machine reasoning:** Compare human-written and LLM-generated chains
