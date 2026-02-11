# %% [markdown]
# # 4. AI Personas (PersonaHub)
# **Category:** AI Agent Core Capabilities
#
# **Source:** [Tencent AI Lab - PersonaHub](https://github.com/tencent-ailab/persona-hub) |
# [HuggingFace](https://huggingface.co/datasets/proj-persona/PersonaHub)
#
# **Description:** Used to train User Simulators, enabling agents to role-play
# specific demographic backgrounds for large-scale social simulation.
#
# **Data Content:** A vast collection of synthetic user persona descriptions
# and their behavioral reaction data within specific contexts.
#
# **Paper:** [Scaling Synthetic Data Creation with 1,000,000,000 Personas](https://arxiv.org/abs/2406.20094)

# %% [markdown]
# ## 1. Setup

# %%
# Install dependencies (uncomment if needed)
# !pip install datasets pandas matplotlib seaborn wordcloud

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datasets import load_dataset

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["figure.dpi"] = 100

# %% [markdown]
# ## 2. Dataset Overview
#
# PersonaHub releases **8 subsets**:
#
# | Subset | Rows | Description |
# |--------|------|-------------|
# | `persona` | 200,000 | Core persona descriptions |
# | `instruction` | 50,000 | Persona-driven instructions |
# | `math` | 50,000 | Persona-driven math problems |
# | `reasoning` | 50,000 | Persona-driven logical reasoning |
# | `knowledge` | 10,000 | Persona-driven knowledge-rich texts |
# | `npc` | 10,000 | Game NPC personas |
# | `tool` | 5,000 | Persona-driven tool/function descriptions |
# | `elite_persona` | 370M | Full-scale persona collection (too large to load here) |
#
# We focus on the **persona**, **instruction**, **math**, and **npc** subsets below.

# %% [markdown]
# ## 3. Data Loading

# %%
# Load main subsets from HuggingFace
print("Loading persona subset (200k rows)...")
ds_persona = load_dataset("proj-persona/PersonaHub", name="persona", split="train")

print("Loading instruction subset (50k rows)...")
ds_instruction = load_dataset("proj-persona/PersonaHub", name="instruction", split="train")

print("Loading math subset (50k rows)...")
ds_math = load_dataset("proj-persona/PersonaHub", name="math", split="train")

print("Loading npc subset (10k rows)...")
ds_npc = load_dataset("proj-persona/PersonaHub", name="npc", split="train")

print("All subsets loaded successfully!")

# %%
# Convert to DataFrames for easier analysis
df_persona = ds_persona.to_pandas()
df_instruction = ds_instruction.to_pandas()
df_math = ds_math.to_pandas()
df_npc = ds_npc.to_pandas()

print(f"Persona subset:     {df_persona.shape}")
print(f"Instruction subset: {df_instruction.shape}")
print(f"Math subset:        {df_math.shape}")
print(f"NPC subset:         {df_npc.shape}")

# %% [markdown]
# ## 4. Data Schema & Samples

# %%
# Persona subset schema
print("=== Persona Subset ===")
print(f"Columns: {list(df_persona.columns)}")
print(f"Shape: {df_persona.shape}\n")
df_persona.head(5)

# %%
# Sample persona descriptions
for i in range(5):
    print(f"[{i+1}] {df_persona['persona'].iloc[i]}")
    print()

# %%
# Instruction subset schema
print("=== Instruction Subset ===")
print(f"Columns: {list(df_instruction.columns)}")
print(f"Shape: {df_instruction.shape}\n")
df_instruction.head(3)

# %%
# Sample instruction entries
for i in range(2):
    print(f"--- Instruction {i+1} ---")
    print(f"Input Persona:   {df_instruction['input persona'].iloc[i][:150]}...")
    print(f"Synthesized Text: {df_instruction['synthesized text'].iloc[i][:200]}...")
    print(f"Description:      {df_instruction['description'].iloc[i]}")
    print()

# %% [markdown]
# ## 5. Exploratory Data Analysis
#
# ### 5.1 Persona Description Length

# %%
df_persona["char_len"] = df_persona["persona"].astype(str).apply(len)
df_persona["word_count"] = df_persona["persona"].astype(str).apply(lambda x: len(x.split()))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_persona["char_len"], bins=50, color="steelblue", edgecolor="white")
axes[0].set_title("Persona Description Length (characters)")
axes[0].set_xlabel("Character Count")
axes[0].set_ylabel("Frequency")

axes[1].hist(df_persona["word_count"], bins=50, color="coral", edgecolor="white")
axes[1].set_title("Persona Description Length (words)")
axes[1].set_xlabel("Word Count")
axes[1].set_ylabel("Frequency")

plt.tight_layout()
plt.show()

print(f"Character length - Mean: {df_persona['char_len'].mean():.0f}, "
      f"Median: {df_persona['char_len'].median():.0f}, "
      f"Max: {df_persona['char_len'].max()}")
print(f"Word count - Mean: {df_persona['word_count'].mean():.1f}, "
      f"Median: {df_persona['word_count'].median():.0f}, "
      f"Max: {df_persona['word_count'].max()}")

# %% [markdown]
# ### 5.2 Top Keywords in Persona Descriptions

# %%
# Extract most frequent meaningful words (skip common stopwords)
stopwords = {
    "a", "an", "the", "and", "or", "of", "in", "to", "for", "is", "are",
    "was", "were", "be", "been", "being", "has", "have", "had", "do", "does",
    "did", "will", "would", "could", "should", "may", "might", "can", "with",
    "at", "by", "from", "on", "as", "it", "its", "this", "that", "their",
    "who", "which", "what", "where", "when", "how", "not", "no", "but", "if",
    "about", "into", "through", "during", "before", "after", "between", "all",
    "each", "every", "both", "such", "than", "too", "very", "also", "just",
    "so", "more", "most", "other", "some", "any", "they", "them", "he", "she",
    "his", "her", "him", "we", "our", "you", "your",
}

all_words = []
for text in df_persona["persona"].astype(str):
    words = text.lower().split()
    all_words.extend([w.strip(".,;:!?()\"'") for w in words if w.strip(".,;:!?()\"'") not in stopwords and len(w) > 2])

word_freq = Counter(all_words).most_common(30)
words, counts = zip(*word_freq)

plt.figure(figsize=(14, 6))
plt.barh(range(len(words)), counts, color="steelblue")
plt.yticks(range(len(words)), words)
plt.gca().invert_yaxis()
plt.title("Top 30 Keywords in Persona Descriptions")
plt.xlabel("Frequency")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.3 Persona Role Categories
#
# We extract role-related keywords to understand the distribution of persona types.

# %%
role_keywords = {
    "Professional/Expert": ["expert", "specialist", "professional", "analyst", "consultant", "advisor"],
    "Student/Learner": ["student", "learner", "studying", "undergraduate", "graduate"],
    "Teacher/Educator": ["teacher", "professor", "educator", "instructor", "tutor"],
    "Engineer/Developer": ["engineer", "developer", "programmer", "software", "architect"],
    "Researcher/Scientist": ["researcher", "scientist", "academic", "scholar"],
    "Artist/Creative": ["artist", "designer", "writer", "musician", "creative"],
    "Healthcare": ["doctor", "nurse", "physician", "therapist", "medical"],
    "Business/Manager": ["manager", "entrepreneur", "business", "executive", "ceo"],
}

role_counts = {}
for role, keywords in role_keywords.items():
    count = df_persona["persona"].astype(str).apply(
        lambda x: any(kw in x.lower() for kw in keywords)
    ).sum()
    role_counts[role] = count

role_df = pd.DataFrame(list(role_counts.items()), columns=["Role Category", "Count"])
role_df = role_df.sort_values("Count", ascending=False)

plt.figure(figsize=(10, 5))
bars = plt.barh(role_df["Role Category"], role_df["Count"], color="coral")
plt.gca().invert_yaxis()
plt.title("Persona Role Categories (keyword-based classification)")
plt.xlabel("Number of Personas")
for bar, val in zip(bars, role_df["Count"]):
    plt.text(bar.get_width() + 200, bar.get_y() + bar.get_height() / 2,
             f"{val:,}", va="center", fontsize=10)
plt.tight_layout()
plt.show()

print(f"Note: Categories are not mutually exclusive; one persona may match multiple categories.")

# %% [markdown]
# ### 5.4 Cross-Subset Comparison: Text Length

# %%
subsets = {
    "Persona (description)": df_persona["persona"].astype(str),
    "Instruction (synthesized)": df_instruction["synthesized text"].astype(str),
    "Math (synthesized)": df_math["synthesized text"].astype(str),
    "NPC (synthesized)": df_npc["synthesized text"].astype(str),
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
colors = ["steelblue", "coral", "mediumseagreen", "orchid"]

for ax, (name, texts), color in zip(axes.flat, subsets.items(), colors):
    lengths = texts.apply(len)
    ax.hist(lengths, bins=50, color=color, edgecolor="white", alpha=0.8)
    ax.set_title(f"{name}\nMean={lengths.mean():.0f} chars, Median={lengths.median():.0f}")
    ax.set_xlabel("Character Count")
    ax.set_ylabel("Frequency")

plt.suptitle("Text Length Distribution Across Subsets", fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.5 Instruction Description Types

# %%
desc_counts = df_instruction["description"].value_counts().head(15)

plt.figure(figsize=(12, 5))
desc_counts.plot(kind="barh", color="mediumseagreen")
plt.gca().invert_yaxis()
plt.title("Top 15 Instruction Description Types")
plt.xlabel("Count")
plt.ylabel("Description")
plt.tight_layout()
plt.show()

print(f"Total unique description types: {df_instruction['description'].nunique()}")

# %% [markdown]
# ### 5.6 Subset Size Summary

# %%
summary = pd.DataFrame({
    "Subset": ["persona", "instruction", "math", "npc"],
    "Rows": [len(df_persona), len(df_instruction), len(df_math), len(df_npc)],
    "Columns": [df_persona.shape[1], df_instruction.shape[1],
                df_math.shape[1], df_npc.shape[1]],
    "Avg Text Length (chars)": [
        df_persona["persona"].astype(str).apply(len).mean(),
        df_instruction["synthesized text"].astype(str).apply(len).mean(),
        df_math["synthesized text"].astype(str).apply(len).mean(),
        df_npc["synthesized text"].astype(str).apply(len).mean(),
    ],
})
summary["Avg Text Length (chars)"] = summary["Avg Text Length (chars)"].round(0).astype(int)
print(summary.to_string(index=False))

# %% [markdown]
# ## 6. Key Observations
#
# 1. **Scale:** PersonaHub provides 200k curated personas (and 370M elite personas),
#    making it one of the largest persona collections available for research.
#
# 2. **Diversity:** Personas span a wide range of roles - from engineers and researchers
#    to artists, educators, and healthcare professionals - enabling diverse user simulation.
#
# 3. **Multi-purpose:** Beyond persona descriptions, the dataset includes
#    persona-driven synthesized content (instructions, math, reasoning, NPC, tools),
#    demonstrating how personas can drive diverse data generation.
#
# 4. **Concise descriptions:** Persona descriptions are relatively short and focused,
#    making them practical as prompts or system instructions for LLMs.
#
# 5. **Research relevance (IS/AI):**
#    - **User simulation:** Train agents to mimic specific demographics for A/B testing
#    - **Synthetic data generation:** Use personas as seeds for creating diverse training data
#    - **Social simulation:** Build multi-agent systems where each agent has a distinct persona
#    - **Bias auditing:** Test model behavior across different persona backgrounds
