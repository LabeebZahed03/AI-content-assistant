"""Orchestration functions for the AI Content Assistant."""

from typing import Dict, Any, List
from .core import summarize, generate_titles, answer_question, recommendations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_all(text: str, question: str = "What are the benefits of wellness programs for companies?") -> Dict[str, Any]:
    """Process text with all available functions."""
    results = {}
    
    logger.info(f"Processing text with length: {len(text)}")
    logger.info(f"First 50 chars: '{text[:50]}...'")
    
    logger.info("Running summarize function")
    results["summary"] = summarize(text)
    
    logger.info("Running generate_titles function")
    results["titles"] = generate_titles(text, n=3)
    
    logger.info(f"Running answer_question function with question: {question}")
    results["answer"] = answer_question(text, question)
    
    logger.info("Running recommendations function")
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
    
    logger.info(f"Selectively processing text with length: {len(text)}")
    logger.info(f"First 50 chars: '{text[:50]}...'")
    
    if do_summary:
        logger.info("Running summarize function")
        results["summary"] = summarize(text)
    
    if do_titles:
        logger.info("Running generate_titles function")
        results["titles"] = generate_titles(text, n=3)
    
    if question:
        logger.info(f"Running answer_question function with question: {question}")
        results["answer"] = answer_question(text, question)
    
    if do_recommendations:
        logger.info("Running recommendations function")
        results["recommendations"] = recommendations(text, n=2)
    
    return results
