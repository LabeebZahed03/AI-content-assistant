"""Orchestration functions for the AI Content Assistant."""

from typing import Dict, Any, List
from .core import summarize, generate_titles, answer_question, recommendations

def process_all(text: str, question: str = "What are the benefits of wellness programs for companies?") -> Dict[str, Any]:
    """Process text with all available functions."""
    results = {}
    
    # Run all functions
    results["summary"] = summarize(text)
    results["titles"] = generate_titles(text, n=3)
    results["answer"] = answer_question(text, question)
    results["recommendations"] = recommendations(text, n=2)
    
    return results

def process_selected(
    text: str,
    do_summary: bool = False,
    do_titles: bool = False,
    question: str = None,
    do_recommendations: bool = False
) -> Dict[str, Any]:
    """Process text with selected functions only."""
    results = {}
    
    if do_summary:
        results["summary"] = summarize(text)
    
    if do_titles:
        results["titles"] = generate_titles(text, n=3)
    
    if question:
        results["answer"] = answer_question(text, question)
    
    if do_recommendations:
        results["recommendations"] = recommendations(text, n=2)
    
    return results
