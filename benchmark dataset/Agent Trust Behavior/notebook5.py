# %% [markdown]
# # 5. Agent Trust Behavior
# **Category:** AI Agent Core Capabilities
#
# **Source:** [CAMEL-AI / agent-trust](https://github.com/camel-ai/agent-trust)
#
# **Description:** Used for game theory research to train agents on decision-making
# logic regarding trust, betrayal, and reciprocity.
#
# **Data Content:** Multi-turn interaction logs from Trust Games, including records
# of the agent's Belief, Desire, and Intention (BDI).
#
# **Paper:** [Can Large Language Models Serve as Rational Players in Game Theory?](https://arxiv.org/abs/2310.01983)

# %% [markdown]
# ## 1. Setup

# %%
# Install dependencies (uncomment if needed)
# !pip install pandas matplotlib seaborn

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["figure.dpi"] = 100

# %% [markdown]
# ## 2. Dataset Overview
#
# The agent-trust dataset records behavioral economics experiments where LLM agents
# play classic game theory scenarios. Each agent is assigned a persona (name, age,
# gender, profession, personality) and makes decisions using a **Belief-Desire-Intention
# (BDI)** framework.
#
# **Game types:**
#
# | Game | Description | Decision |
# |------|-------------|----------|
# | **Trust Game** | Give $N (tripled) to a player who may return some | Dollar amount (0-10) |
# | **Dictator Game** | Give $N (tripled) to a player, no return expected | Dollar amount (0-10) |
# | **Risky Dictator Problem** | Trust/not trust with probabilistic payoffs | trust / not trust |
# | **Trust Problem** | Trust/not trust with reciprocal decisions | trust / not trust |
# | **Lottery Problem** | Fixed vs. probabilistic payoff comparison | trust / not trust |
#
# **Models tested:** GPT-4, GPT-3.5-Turbo, LLaMA-2 (7B/13B/70B), Vicuna (7B/13B/33B)
#
# **Experiment variants:**
# - `res/`: Baseline (no demographic persona)
# - `person_res/`: With persona (name, age, gender, profession, personality)
# - `male_res/`, `female_res/`: Gender-specific personas
# - `African American_res/`, `Asian American_res/`, etc.: Race-specific personas
# - `COT_res/`: Chain-of-Thought prompting
# - `more_trust_2_res/`, `less_trust_2_res/`: Trust-biased personas

# %% [markdown]
# ## 3. Data Loading

# %%
# Clone the repository (skip if already cloned)
REPO_DIR = Path("agent-trust")
if not REPO_DIR.exists():
    os.system("git clone https://github.com/camel-ai/agent-trust.git")
    print("Repository cloned.")
else:
    print(f"Repository already exists at {REPO_DIR}")

DATA_DIR = REPO_DIR / "agent_trust"

# %%
# List available experiment directories
no_repeat_dir = DATA_DIR / "No repeated res"
repeat_dir = DATA_DIR / "repeated res"

print("=== Non-Repeated Experiment Variants ===")
for d in sorted(no_repeat_dir.iterdir()):
    if d.is_dir():
        print(f"  {d.name}/")

print(f"\n=== Repeated Experiment Variants ===")
for d in sorted(repeat_dir.iterdir()):
    if d.is_dir():
        print(f"  {d.name}/")

# %%
# Load a single JSON result file
def load_game_json(filepath):
    """Load a game result JSON and return a list of record dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    res_list = data.get("res", [])
    dialog_list = data.get("dialog", [])

    # Handle two formats: flat list vs per-entry
    if isinstance(res_list, list) and isinstance(dialog_list, list):
        for i in range(min(len(res_list), len(dialog_list))):
            entry = dialog_list[i]
            record = {
                "decision": res_list[i],
                "index": entry[0] if len(entry) > 0 else i,
                "persona": entry[1] if len(entry) > 1 else "",
                "response": entry[2] if len(entry) > 2 else "",
            }
            records.append(record)
    return records


def load_all_games(variant_dir):
    """Load all game JSON files from a model's result directory."""
    all_records = []
    if not variant_dir.exists():
        return all_records

    for json_file in sorted(variant_dir.glob("*.json")):
        filename = json_file.stem
        # Extract game type and model from filename
        records = load_game_json(json_file)
        for r in records:
            r["filename"] = filename
            r["source_file"] = json_file.name
        all_records.extend(records)
    return all_records

# %%
# Load non-repeated baseline results for all models
baseline_dir = no_repeat_dir / "res"
all_baseline = []

for model_dir in sorted(baseline_dir.iterdir()):
    if model_dir.is_dir():
        model_name = model_dir.name.replace("_res", "")
        records = load_all_games(model_dir)
        for r in records:
            r["model"] = model_name
        all_baseline.extend(records)

df_baseline = pd.DataFrame(all_baseline)
print(f"Baseline records loaded: {df_baseline.shape}")
print(f"Models: {df_baseline['model'].unique().tolist()}")

# %%
# Load persona-based results for all models
persona_dir = no_repeat_dir / "person_res"
all_persona = []

for model_dir in sorted(persona_dir.iterdir()):
    if model_dir.is_dir():
        model_name = model_dir.name.replace("_res", "")
        records = load_all_games(model_dir)
        for r in records:
            r["model"] = model_name
        all_persona.extend(records)

df_persona = pd.DataFrame(all_persona)
print(f"Persona records loaded: {df_persona.shape}")

# %% [markdown]
# ## 4. Data Schema & Samples

# %%
print("=== Baseline Data Schema ===")
print(f"Columns: {list(df_baseline.columns)}")
print(f"Shape: {df_baseline.shape}\n")
df_baseline.head(5)

# %%
# Classify game type from filename
def classify_game(filename):
    fname = filename.lower()
    if "trust_game" in fname:
        return "Trust Game"
    elif "dictator_game" in fname:
        return "Dictator Game"
    elif "risky_dictator" in fname:
        return "Risky Dictator"
    elif "trust_problem" in fname or "map_trust" in fname:
        return "Trust Problem"
    elif "lottery" in fname:
        return "Lottery Problem"
    else:
        return "Other"

df_baseline["game_type"] = df_baseline["filename"].apply(classify_game)
df_persona["game_type"] = df_persona["filename"].apply(classify_game)

print("Game type distribution (baseline):")
print(df_baseline["game_type"].value_counts().to_string())

# %%
# Sample BDI responses from Trust Game
trust_game = df_persona[df_persona["game_type"] == "Trust Game"]
if len(trust_game) > 0:
    for i, row in trust_game.head(2).iterrows():
        print(f"--- Model: {row['model']} | Decision: ${row['decision']:.0f} ---")
        # Show persona (truncated)
        persona_text = row["persona"][:200] if isinstance(row["persona"], str) else ""
        print(f"Persona: {persona_text}...")
        # Show BDI response (truncated)
        response_text = row["response"][:300] if isinstance(row["response"], str) else ""
        print(f"BDI Response: {response_text}...")
        print()

# %% [markdown]
# ## 5. Exploratory Data Analysis
#
# ### 5.1 Trust Game: Giving Amount by Model

# %%
trust_baseline = df_baseline[df_baseline["game_type"] == "Trust Game"].copy()
trust_baseline["decision"] = pd.to_numeric(trust_baseline["decision"], errors="coerce")
trust_baseline = trust_baseline.dropna(subset=["decision"])

if len(trust_baseline) > 0:
    model_order = trust_baseline.groupby("model")["decision"].mean().sort_values(ascending=False).index

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=trust_baseline, x="model", y="decision", order=model_order, palette="Set2")
    plt.title("Trust Game: Distribution of Giving Amount by Model")
    plt.xlabel("Model")
    plt.ylabel("Amount Given ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    print("Mean giving amount per model:")
    print(trust_baseline.groupby("model")["decision"].agg(["mean", "median", "std"]).round(2).sort_values("mean", ascending=False).to_string())
else:
    print("No Trust Game data found in baseline.")

# %% [markdown]
# ### 5.2 Dictator Game: Giving Amount by Model

# %%
dictator_baseline = df_baseline[df_baseline["game_type"] == "Dictator Game"].copy()
dictator_baseline["decision"] = pd.to_numeric(dictator_baseline["decision"], errors="coerce")
dictator_baseline = dictator_baseline.dropna(subset=["decision"])

if len(dictator_baseline) > 0:
    model_order = dictator_baseline.groupby("model")["decision"].mean().sort_values(ascending=False).index

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=dictator_baseline, x="model", y="decision", order=model_order, palette="Set3")
    plt.title("Dictator Game: Distribution of Giving Amount by Model")
    plt.xlabel("Model")
    plt.ylabel("Amount Given ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
else:
    print("No Dictator Game data found in baseline.")

# %% [markdown]
# ### 5.3 Trust Game vs Dictator Game Comparison

# %%
monetary_games = df_baseline[df_baseline["game_type"].isin(["Trust Game", "Dictator Game"])].copy()
monetary_games["decision"] = pd.to_numeric(monetary_games["decision"], errors="coerce")
monetary_games = monetary_games.dropna(subset=["decision"])

if len(monetary_games) > 0:
    comparison = monetary_games.groupby(["model", "game_type"])["decision"].mean().unstack(fill_value=0)

    comparison.plot(kind="bar", figsize=(12, 6), color=["steelblue", "coral"])
    plt.title("Mean Giving Amount: Trust Game vs Dictator Game")
    plt.xlabel("Model")
    plt.ylabel("Mean Amount Given ($)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Game Type")
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ### 5.4 Effect of Persona on Trust Decisions

# %%
# Compare baseline (no persona) vs persona-based Trust Game
_bl = df_baseline[df_baseline["game_type"] == "Trust Game"].copy()
_bl["decision"] = pd.to_numeric(_bl["decision"], errors="coerce")
trust_bl = _bl.dropna(subset=["decision"]).groupby("model")["decision"].mean()

_ps = df_persona[df_persona["game_type"] == "Trust Game"].copy()
_ps["decision"] = pd.to_numeric(_ps["decision"], errors="coerce")
trust_ps = _ps.dropna(subset=["decision"]).groupby("model")["decision"].mean()

compare_df = pd.DataFrame({"Baseline (no persona)": trust_bl, "With Persona": trust_ps}).dropna()

if len(compare_df) > 0:
    compare_df.plot(kind="bar", figsize=(10, 5), color=["steelblue", "coral"])
    plt.title("Effect of Persona on Trust Game Giving Amount")
    plt.xlabel("Model")
    plt.ylabel("Mean Amount Given ($)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Condition")
    plt.tight_layout()
    plt.show()

    print("Difference (Persona - Baseline):")
    diff = (compare_df["With Persona"] - compare_df["Baseline (no persona)"]).round(2)
    print(diff.to_string())

# %% [markdown]
# ### 5.5 Demographic Variants: Trust Game Comparison

# %%
demographic_dirs = {
    "Male": "male_res",
    "Female": "female_res",
    "African American": "African American_res",
    "Asian American": "Asian American_res",
    "Latino American": "Latino American_res",
    "White American": "White American_res",
}

demo_results = {}
for label, dirname in demographic_dirs.items():
    variant_dir = no_repeat_dir / dirname
    if variant_dir.exists():
        all_records = []
        for model_dir in sorted(variant_dir.iterdir()):
            if model_dir.is_dir():
                model_name = model_dir.name.replace("_res", "")
                records = load_all_games(model_dir)
                for r in records:
                    r["model"] = model_name
                    r["filename_lower"] = r.get("filename", "").lower()
                all_records.extend(records)
        df_var = pd.DataFrame(all_records)
        if len(df_var) > 0:
            df_var["game_type"] = df_var["filename"].apply(classify_game)
            trust_var = df_var[df_var["game_type"] == "Trust Game"].copy()
            trust_var["decision"] = pd.to_numeric(trust_var["decision"], errors="coerce")
            trust_var = trust_var.dropna(subset=["decision"])
            if len(trust_var) > 0:
                demo_results[label] = trust_var["decision"].mean()

if demo_results:
    demo_df = pd.Series(demo_results).sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(demo_df.index, demo_df.values, color="mediumseagreen")
    plt.title("Trust Game: Mean Giving Amount by Demographic Persona")
    plt.ylabel("Mean Amount Given ($)")
    plt.xticks(rotation=45, ha="right")
    for bar, val in zip(bars, demo_df.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f"${val:.1f}", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.show()
else:
    print("No demographic variant data found.")

# %% [markdown]
# ### 5.6 Game Type Distribution & Record Counts

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Game type distribution
game_counts = df_baseline["game_type"].value_counts()
axes[0].barh(game_counts.index, game_counts.values, color="steelblue")
axes[0].set_title("Records per Game Type (Baseline)")
axes[0].set_xlabel("Number of Records")
axes[0].invert_yaxis()

# Model distribution
model_counts = df_baseline["model"].value_counts()
axes[1].barh(model_counts.index, model_counts.values, color="coral")
axes[1].set_title("Records per Model (Baseline)")
axes[1].set_xlabel("Number of Records")
axes[1].invert_yaxis()

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.7 Summary Statistics

# %%
_numeric = df_baseline.copy()
_numeric["decision"] = pd.to_numeric(_numeric["decision"], errors="coerce")
summary = _numeric.dropna(subset=["decision"]).groupby(["game_type", "model"])["decision"].agg(
    ["count", "mean", "std", "min", "max"]
).round(2)
print(summary.to_string())

# %% [markdown]
# ## 6. Key Observations
#
# 1. **BDI Framework:** Each agent articulates Belief, Desire, and Intention before
#    making a decision, providing interpretable reasoning traces for game-theoretic analysis.
#
# 2. **Model differences:** Different LLMs exhibit distinct trust/generosity profiles.
#    GPT-4 tends to be more "generous" in trust games compared to smaller models.
#
# 3. **Persona effects:** Assigning demographic personas to agents can shift their
#    trust behavior, revealing potential biases embedded in LLMs.
#
# 4. **Trust vs. Dictator:** Agents often give more in Trust Games (where reciprocation
#    is possible) than in Dictator Games, mirroring human behavioral patterns.
#
# 5. **Research relevance (IS/AI):**
#    - **Agent alignment:** Evaluate whether LLM agents align with rational or prosocial norms
#    - **Bias detection:** Test if demographic personas cause disparate trust behavior
#    - **Multi-agent simulation:** Build game-theoretic environments for agent interaction research
#    - **Behavioral economics:** Use LLMs as proxies for human subjects in economic experiments
