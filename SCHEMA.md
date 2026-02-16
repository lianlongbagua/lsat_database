# LSAT Database Schema - AI Agent Guide

This document provides detailed schema information for AI agents working with the LSAT database.

## Overview

The database consists of 8 JSON files containing LSAT questions, passages, and pedagogical materials. The two primary files are:

- **LR questions** (~152k entries, ~24 MB)
- **RC passages** (~10 MB)

---

## LR Metadata (lr_metadata_enriched.json)

### Key Format

Keys follow this pattern: `"{PT}.{Section}.{Question}.LR.{TaskCode}.({Answer})"`

**Example**: `"101.2.1.LR.AG.(B)"`

- PT 101
- Section 2
- Question 1
- Task type: AG (Argument)
- Answer: B

### Field Reference

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `task_code` | string | High-level question category | `"AG"`, `"IN"`, `"ST"`, `"AS"` |
| `engine_code` | string | Reasoning engine type | `"IN"`, `"DE"`, `"CA"`, `"NO"` |
| `difficulty` | int | Original difficulty (1-5) | `1`, `2`, `3` |
| `detailed_task_code` | string | Specific question type | `"FL"`, `"SR"`, `"WE"`, `"NA"` |
| `detailed_difficulty` | int | Detailed difficulty (1-5) | `1` to `5` |
| `answer` | string | Correct answer | `"A"`, `"B"`, `"C"`, `"D"`, `"E"` |
| `text` | string | Full question text | Full question string |
| `stimulus` | string | Argument passage | Text of the stimulus |
| `stem` | string | Question stem | "Which one of the following..." |
| `choices` | dict | Answer choices | `{"A": "...", "B": "..."}` |
| `canonical_explanation` | dict | Comprehensive explanation | See below |
| `structure` | dict | Parsed argument structure | See below |

### Task Code Hierarchy

The database uses a two-level classification system. Each question has:

- A high-level `task_code` (4 categories)
- A specific `detailed_task_code` (14 types total)

Every detailed code belongs to exactly one high-level category.

#### AG (Argument) — 1,440 questions (36.6%)

Questions that evaluate, critique, or modify an argument.

- **FL**: Flaw (636)
- **WE**: Weaken (334)
- **SR**: Strengthen (295)
- **PF**: Parallel Flaw (155)
- **EV**: Evaluate (20)

#### AS (Assumption) — 770 questions (19.6%)

Questions that identify what an argument depends on.

- **NA**: Necessary Assumption (407)
- **SA**: Sufficient Assumption (363)

#### IN (Inference) — 936 questions (23.8%)

Questions about what follows from the information given.

- **IN**: Inference (665)
- **RP**: Resolve Paradox (271)

#### ST (Structure) — 787 questions (20.0%)

Questions about how the argument works or is organized.

- **MP**: Main Point (242)
- **RO**: Role (of statement) (159)
- **PI**: Point at Issue (140)
- **PR**: Parallel Reasoning (128)
- **ME**: Method of Reasoning (118)

### Canonical Explanation Structure

```json
"canonical_explanation": {
  "analysis": "Detailed analysis of the argument...",
  "choices": {
    "A": "Why A is wrong/right...",
    "B": "Why B is wrong/right...",
    // ... etc
  }
}
```

### Argument Structure

The `structure` field contains parsed argument components:

```json
"structure": {
  "conclusion": "Main conclusion of the argument",
  "premises": [
    "First premise",
    "Second premise"
  ],
  "background": "Background context (if any)"
}
```

For inference questions without arguments:

```json
"structure": {
  "facts": [
    "Fact 1",
    "Fact 2"
  ],
  "note": "No Conclusion"
}
```

---

## RC Metadata (rc_metadata_scaled.json)

Contains Reading Comprehension passages with questions.

### Key Format

Keys follow: `"{PT}.{Section}.{Passage}"`

**Example**: `"J07.1.1"` (June 2007, Section 1, Passage 1)

### Structure

Each entry contains the full passage text and associated questions.

---

## Supporting Files

### canonical_drills.json

Contains drill templates and structures for practice sets.

### formal_logic_data.json

Formal logic patterns, symbols, and transformation rules.

### logic_sentences.json

Templates for constructing logical sentences and arguments.

### lsat_methodology_master.json

Pedagogical framework and teaching approach.

### negation_templates.json

Patterns for logical negation across different statement types.

### global_stats.json

Database statistics (question counts, coverage, etc.).

---

## Common Query Patterns

### By PrepTest

```python
# All questions from PT 101
pt_101 = {k: v for k, v in lr_data.items() if k.startswith("101.")}
```

### By Question Type

```python
# All Flaw questions
flaws = {k: v for k, v in lr_data.items() if v["detailed_task_code"] == "FL"}

# All Strengthen questions
strengthens = {k: v for k, v in lr_data.items() if v["detailed_task_code"] == "SR"}
```

### By Difficulty

```python
# All difficulty 5 questions
hard = {k: v for k, v in lr_data.items() if v["detailed_difficulty"] == 5}

# Difficulty 4 or 5
challenging = {k: v for k, v in lr_data.items() if v["detailed_difficulty"] >= 4}
```

### By Section and Question Range

```python
# PT 101, Section 2, Questions 1-10
section_questions = {
    k: v for k, v in lr_data.items() 
    if k.startswith("101.2.") and int(k.split(".")[2]) <= 10
}
```

### Combining Filters

```python
# Hard Flaw questions from PT 90+
hard_flaws_modern = {
    k: v for k, v in lr_data.items()
    if v["detailed_task_code"] == "FL"
    and v["detailed_difficulty"] >= 4
    and int(k.split(".")[0]) >= 90
}
```

---

## Important Notes for AI Agents

### Data Loading

Always use the helper functions from the package:

```python
from lsat_database import get_lr_questions
lr_data = get_lr_questions()
```

**Don't** try to construct file paths manually or use `json.load()` directly.

### Memory Considerations

The full LR dataset is **~24 MB** (152k questions). Loading it into memory is fine for most operations, but be mindful when:

- Creating multiple filtered copies
- Storing in variables that persist across operations
- Working with multiple datasets simultaneously

### Key Parsing

Keys encode important metadata. Parse them carefully:

```python
key = "101.2.1.LR.AG.(B)"
parts = key.split(".")
pt = int(parts[0])        # 101
section = int(parts[1])   # 2
question = int(parts[2])  # 1
# Rest is: "LR.AG.(B)"
```

### Missing Fields

Not all questions have all fields. Always use `.get()` with defaults:

```python
difficulty = question.get("detailed_difficulty", 3)  # Default to 3
```

### Explanation Quality

The `canonical_explanation` field contains comprehensive, human-written explanations. This is high-quality pedagogical content—use it when explaining questions to students.

---

## Example: Complete Question Object

```json
"101.2.1.LR.AG.(B)": {
  "task_code": "AG",
  "engine_code": "IN",
  "difficulty": 1,
  "reasoning": "The question asks to identify a weakness...",
  "canonical_explanation": {
    "analysis": "The argument in the press release commits...",
    "choices": {
      "A": "This choice attacks the methodology...",
      "B": "This is the correct answer...",
      "C": "This choice introduces...",
      "D": "The effects of 'other beverages'...",
      "E": "The premise specifically restricts..."
    }
  },
  "text": "Press release: A comprehensive review...",
  "stimulus": "Press release: A comprehensive review...",
  "stem": "Which one of the following points to a weakness...",
  "choices": {
    "A": "The review was only an evaluation of studies...",
    "B": "The health of the heart is not identical...",
    "C": "Coffee drinkers might choose to eat...",
    "D": "Other beverages besides coffee...",
    "E": "Drinking unusually large amounts..."
  },
  "answer": "B",
  "detailed_task_code": "FL",
  "detailed_difficulty": 2,
  "gemini_relabel": true,
  "structure": {
    "conclusion": "It is safe to drink coffee.",
    "premises": [
      "A comprehensive review... has found no reason to think..."
    ],
    "background": "coffee drinkers can relax and enjoy their beverage"
  }
}
```

---

## Quick Reference Card

**Loading data:**

```python
from lsat_database import get_lr_questions, get_rc_passages
```

**Common filters:**

- PT: `k.startswith("101.")`
- Type: `v["detailed_task_code"] == "FL"`
- Difficulty: `v["detailed_difficulty"] >= 4`

**Question type codes:**
FL, SR, WE, NA, SA, PR, PF, ME, MP, RO, PI, RP, IN, EV

**Always use `.get()` for optional fields!**
