"""
LSAT Database Package

A centralized database of LSAT questions and materials for use across
multiple LSAT preparation applications.

Quick Start:
    >>> from lsat_database import get_lr_questions, get_rc_passages
    >>> lr_data = get_lr_questions()
    >>> print(f"Loaded {len(lr_data)} LR questions")
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

__version__ = "0.1.0"

# Get the package's data directory
_DATA_DIR = Path(__file__).parent / "data"


def get_data_path(filename: str) -> Path:
    """
    Get the absolute path to a data file in the package.
    
    Args:
        filename: Name of the JSON file (e.g., 'lr_metadata_enriched.json')
    
    Returns:
        Path object pointing to the data file
    
    Example:
        >>> path = get_data_path('lr_metadata_enriched.json')
        >>> print(path.exists())
        True
    """
    return _DATA_DIR / filename


def _load_json(filename: str) -> Dict[str, Any]:
    """Internal helper to load a JSON file from the data directory."""
    path = get_data_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_lr_questions() -> Dict[str, Any]:
    """
    Load all Logical Reasoning (LR) questions.
    
    Returns:
        Dictionary with question IDs as keys and question data as values.
        Key format: "{PT}.{Section}.{Question}.LR.{TaskCode}.({Answer})"
        Example: "101.2.1.LR.AG.(B)"
    
    Example:
        >>> lr_data = get_lr_questions()
        >>> question = lr_data["101.2.1.LR.AG.(B)"]
        >>> print(question['answer'])
        'B'
    """
    return _load_json('lr_metadata_enriched.json')


def get_rc_passages() -> Dict[str, Any]:
    """
    Load all Reading Comprehension (RC) passages.
    
    Returns:
        Dictionary with passage IDs as keys and passage data as values.
    
    Example:
        >>> rc_data = get_rc_passages()
        >>> print(f"Loaded {len(rc_data)} RC passages")
    """
    return _load_json('rc_metadata_scaled.json')


def get_canonical_drills() -> Dict[str, Any]:
    """
    Load canonical drill definitions.
    
    Returns:
        Dictionary containing drill structures and metadata.
    """
    return _load_json('canonical_drills.json')


def get_formal_logic_data() -> Dict[str, Any]:
    """
    Load formal logic data and templates.
    
    Returns:
        Dictionary containing formal logic patterns and examples.
    """
    return _load_json('formal_logic_data.json')


def get_logic_sentences() -> Dict[str, Any]:
    """
    Load logic sentence templates and examples.
    
    Returns:
        Dictionary containing sentence patterns.
    """
    return _load_json('logic_sentences.json')


def get_methodology() -> Dict[str, Any]:
    """
    Load LSAT methodology and pedagogical framework.
    
    Returns:
        Dictionary containing teaching methodology and approach.
    """
    return _load_json('lsat_methodology_master.json')


def get_negation_templates() -> Dict[str, Any]:
    """
    Load negation templates for logical reasoning.
    
    Returns:
        Dictionary containing negation patterns.
    """
    return _load_json('negation_templates.json')


def get_global_stats() -> Dict[str, Any]:
    """
    Load global statistics about the database.
    
    Returns:
        Dictionary containing database statistics.
    """
    return _load_json('global_stats.json')


# Convenience exports
__all__ = [
    'get_lr_questions',
    'get_rc_passages',
    'get_canonical_drills',
    'get_formal_logic_data',
    'get_logic_sentences',
    'get_methodology',
    'get_negation_templates',
    'get_global_stats',
    'get_data_path',
    '__version__',
]
