# LSAT Database Package

A centralized Python package containing the complete LSAT question database, shared across multiple LSAT preparation applications.

## Quick Start

### Installation

Install in editable mode (recommended for development):

```bash
pip install -e path/to/lsat_database
```

For example, from `lsat_gen`:

```bash
cd c:\Users\tonyc\Desktop\lsat_program\lsat_gen
.venv\Scripts\activate
pip install -e ..\lsat_database
```

### Basic Usage

```python
from lsat_database import get_lr_questions, get_rc_passages

# Load all Logical Reasoning questions
lr_data = get_lr_questions()
print(f"Loaded {len(lr_data)} LR questions")

# Access a specific question
question = lr_data["101.2.1.LR.AG.(B)"]
print(question['answer'])  # Outputs: 'B'

# Load Reading Comprehension passages
rc_data = get_rc_passages()
```

## Available Functions

| Function | Description | Returns |
|----------|-------------|---------|
| `get_lr_questions()` | All Logical Reasoning questions (~152k entries) | Dict |
| `get_rc_passages()` | All Reading Comprehension passages | Dict |
| `get_canonical_drills()` | Canonical drill definitions | Dict |
| `get_formal_logic_data()` | Formal logic patterns and templates | Dict |
| `get_logic_sentences()` | Logic sentence templates | Dict |
| `get_methodology()` | LSAT teaching methodology | Dict |
| `get_negation_templates()` | Logical negation patterns | Dict |
| `get_global_stats()` | Database statistics | Dict |
| `get_data_path(filename)` | Path to a specific data file | Path |

## Common Patterns

### Filter by PrepTest Number

```python
from lsat_database import get_lr_questions

lr_data = get_lr_questions()

# Get all questions from PT 101
pt_101 = {k: v for k, v in lr_data.items() if k.startswith("101.")}
```

### Filter by Question Type

```python
# Get all Flaw questions
flaw_questions = {
    k: v for k, v in lr_data.items() 
    if v.get("detailed_task_code") == "FL"
}

# Get all Strengthen questions
strengthen_questions = {
    k: v for k, v in lr_data.items() 
    if v.get("detailed_task_code") == "SR"
}
```

### Filter by Difficulty

```python
# Get all difficulty 5 questions
hard_questions = {
    k: v for k, v in lr_data.items() 
    if v.get("detailed_difficulty") == 5
}
```

## Database Structure

The package contains 8 JSON files totaling ~34 MB:

- **lr_metadata_enriched.json** (~23.7 MB): 151,951 LR questions with full explanations
- **rc_metadata_scaled.json** (~10.3 MB): Reading Comprehension passages
- **canonical_drills.json** (~75 KB): Drill templates and structures
- **formal_logic_data.json** (~6 KB): Formal logic patterns
- **logic_sentences.json** (~19 KB): Logic sentence templates
- **lsat_methodology_master.json** (~17 KB): Teaching methodology
- **negation_templates.json** (~4.5 KB): Negation patterns
- **global_stats.json** (~384 B): Database statistics

For detailed schema information, see [SCHEMA.md](SCHEMA.md).

## How Updates Work

Since the package is installed in **editable mode** (`-e` flag), any changes to the data files in the package are immediately visible to all apps that have it installed. No need to reinstall!

### Update Workflow

1. Make changes to data files in `lsat_database/src/lsat_database/data/`
2. Changes are immediately visible in all apps
3. That's it! No reinstall needed.

## Installation for Each App

### lsat_gen

```bash
cd c:\Users\tonyc\Desktop\lsat_program\lsat_gen
.venv\Scripts\activate
pip install -e ..\lsat_database
```

### lsat_textbook

```bash
cd c:\Users\tonyc\Desktop\lsat_program\lsat_textbook
.venv\Scripts\activate
pip install -e ..\lsat_database
```

### lsat_web_app

```bash
cd c:\Users\tonyc\Desktop\lsat_program\lsat_web_app
.venv\Scripts\activate
pip install -e ..\lsat_database
```

## For AI Agents

This package is designed to be self-documenting for AI assistants:

- **Schema documentation**: See [SCHEMA.md](SCHEMA.md) for complete field descriptions
- **Example queries**: See [examples/common_queries.py](src/lsat_database/examples/common_queries.py)
- **Inline documentation**: All functions have comprehensive docstrings

The database schema is complex. When working with it:

1. Read [SCHEMA.md](SCHEMA.md) first
2. Check the examples in `common_queries.py`
3. Use the helper functions rather than direct file access

## Package Structure

```
lsat_database/
├── pyproject.toml              # Package configuration
├── README.md                   # This file
├── SCHEMA.md                   # Detailed schema documentation
└── src/
    └── lsat_database/
        ├── __init__.py         # Main module with helper functions
        ├── data/               # JSON database files
        │   ├── lr_metadata_enriched.json
        │   ├── rc_metadata_scaled.json
        │   └── ... (6 more files)
        └── examples/
            └── common_queries.py
```

## Version

Current version: 0.1.0

## License

Internal use for LSAT preparation applications.
