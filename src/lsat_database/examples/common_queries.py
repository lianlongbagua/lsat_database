"""
Common LSAT Database Queries

This module demonstrates common patterns for querying the LSAT database.
AI agents: Read this file to understand how to work with the database effectively.
"""

from lsat_database import get_lr_questions, get_rc_passages


def get_questions_by_pt(pt_number):
    """
    Get all questions from a specific PrepTest.
    
    Args:
        pt_number: PrepTest number (e.g., 101)
    
    Returns:
        Dictionary of questions from that PT
    
    Example:
        >>> pt_101 = get_questions_by_pt(101)
        >>> print(f"PT 101 has {len(pt_101)} questions")
    """
    lr_data = get_lr_questions()
    return {k: v for k, v in lr_data.items() if k.startswith(f"{pt_number}.")}


def get_questions_by_type(task_code):
    """
    Get all questions of a specific type.
    
    Args:
        task_code: Question type code (e.g., 'FL', 'SR', 'WE', 'NA')
    
    Returns:
        Dictionary of questions matching that type
    
    Common task codes:
        - FL: Flaw
        - SR: Strengthen
        - WE: Weaken
        - NA: Necessary Assumption
        - SA: Sufficient Assumption
        - PR: Parallel Reasoning
        - PF: Parallel Flaw
        - MP: Main Point
        - IN: Inference
    
    Example:
        >>> flaw_questions = get_questions_by_type('FL')
        >>> print(f"Found {len(flaw_questions)} flaw questions")
    """
    lr_data = get_lr_questions()
    return {k: v for k, v in lr_data.items() 
            if v.get("detailed_task_code") == task_code}


def get_questions_by_difficulty(min_difficulty=1, max_difficulty=5):
    """
    Get questions within a difficulty range.
    
    Args:
        min_difficulty: Minimum difficulty (1-5)
        max_difficulty: Maximum difficulty (1-5)
    
    Returns:
        Dictionary of questions in that difficulty range
    
    Example:
        >>> hard_questions = get_questions_by_difficulty(4, 5)
        >>> print(f"Found {len(hard_questions)} hard questions")
    """
    lr_data = get_lr_questions()
    return {k: v for k, v in lr_data.items() 
            if min_difficulty <= v.get("detailed_difficulty", 3) <= max_difficulty}


def get_questions_by_section(pt_number, section_number):
    """
    Get all questions from a specific PT section.
    
    Args:
        pt_number: PrepTest number (e.g., 101)
        section_number: Section number (typically 1-4)
    
    Returns:
        Dictionary of questions from that section
    
    Example:
        >>> section = get_questions_by_section(101, 2)
        >>> print(f"PT 101, Section 2 has {len(section)} questions")
    """
    lr_data = get_lr_questions()
    prefix = f"{pt_number}.{section_number}."
    return {k: v for k, v in lr_data.items() if k.startswith(prefix)}


def filter_questions(task_codes=None, min_difficulty=None, max_difficulty=None, 
                     pt_min=None, pt_max=None):
    """
    Flexible filter for combining multiple criteria.
    
    Args:
        task_codes: List of task codes to include (e.g., ['FL', 'SR'])
        min_difficulty: Minimum difficulty
        max_difficulty: Maximum difficulty
        pt_min: Minimum PrepTest number
        pt_max: Maximum PrepTest number
    
    Returns:
        Dictionary of questions matching all criteria
    
    Example:
        >>> # Hard modern flaw questions
        >>> questions = filter_questions(
        ...     task_codes=['FL'],
        ...     min_difficulty=4,
        ...     pt_min=90
        ... )
    """
    lr_data = get_lr_questions()
    results = {}
    
    for key, question in lr_data.items():
        # Check task code
        if task_codes and question.get("detailed_task_code") not in task_codes:
            continue
        
        # Check difficulty
        difficulty = question.get("detailed_difficulty", 3)
        if min_difficulty and difficulty < min_difficulty:
            continue
        if max_difficulty and difficulty > max_difficulty:
            continue
        
        # Check PT range
        try:
            pt_num = int(key.split(".")[0])
            if pt_min and pt_num < pt_min:
                continue
            if pt_max and pt_num > pt_max:
                continue
        except (ValueError, IndexError):
            continue
        
        results[key] = question
    
    return results


def get_question_stats():
    """
    Get basic statistics about the database.
    
    Returns:
        Dictionary with database statistics
    
    Example:
        >>> stats = get_question_stats()
        >>> print(stats['total_questions'])
        >>> print(stats['question_types'])
    """
    lr_data = get_lr_questions()
    
    # Count by type
    type_counts = {}
    difficulty_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for question in lr_data.values():
        # Count by detailed task code
        task_code = question.get("detailed_task_code", "UNKNOWN")
        type_counts[task_code] = type_counts.get(task_code, 0) + 1
        
        # Count by difficulty
        difficulty = question.get("detailed_difficulty", 3)
        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1
    
    return {
        'total_questions': len(lr_data),
        'question_types': type_counts,
        'difficulty_distribution': difficulty_counts,
    }


def sample_questions(task_code, count=10, difficulty=None):
    """
    Get a sample of questions for practice or testing.
    
    Args:
        task_code: Question type
        count: Number of questions to return
        difficulty: Optional specific difficulty level
    
    Returns:
        Dictionary of sampled questions
    
    Example:
        >>> # Get 10 medium-difficulty flaw questions
        >>> sample = sample_questions('FL', count=10, difficulty=3)
    """
    questions = get_questions_by_type(task_code)
    
    if difficulty:
        questions = {k: v for k, v in questions.items() 
                    if v.get("detailed_difficulty") == difficulty}
    
    # Convert to list and take first 'count' items
    items = list(questions.items())[:count]
    return dict(items)


# Example usage for AI agents
if __name__ == "__main__":
    # Example 1: Get PT 101 questions
    pt_101 = get_questions_by_pt(101)
    print(f"PT 101 has {len(pt_101)} questions")
    
    # Example 2: Get all flaw questions
    flaws = get_questions_by_type('FL')
    print(f"Database contains {len(flaws)} flaw questions")
    
    # Example 3: Get hard questions
    hard = get_questions_by_difficulty(4, 5)
    print(f"Found {len(hard)} hard questions")
    
    # Example 4: Complex filter
    modern_hard_flaws = filter_questions(
        task_codes=['FL'],
        min_difficulty=4,
        pt_min=90
    )
    print(f"Found {len(modern_hard_flaws)} modern hard flaw questions")
    
    # Example 5: Database statistics
    stats = get_question_stats()
    print(f"\nDatabase Statistics:")
    print(f"Total questions: {stats['total_questions']}")
    print(f"Top 5 question types:")
    sorted_types = sorted(stats['question_types'].items(), 
                         key=lambda x: x[1], reverse=True)
    for task_code, count in sorted_types[:5]:
        print(f"  {task_code}: {count}")
