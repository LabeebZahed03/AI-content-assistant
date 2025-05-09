"""Core LLM functions for the AI Content Assistant."""

import os
from typing import List, Optional, Any, Union, Dict
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
import openai
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define prompt templates
SUMMARY_TEMPLATE = """You are an expert editor.
Summarize the following passage in 1-2 crisp sentences:

\"\"\"{{text}}\"\"\""""

TITLES_TEMPLATE = """Generate {{n}} creative, catchy blog titles for the passage below.
Return as a numbered list.

\"\"\"{{text}}\"\"\""""

QA_TEMPLATE = """Answer the question using ONLY the passage.
If not in passage, say "Not found."

Passage:
\"\"\"{{text}}\"\"\"

Q: {{question}}
A:"""

RECS_TEMPLATE = """Give {{n}} actionable recommendations for a company starting a wellness program,
based on this passage. Reply as bullet points.

\"\"\"{{text}}\"\"\""""

# Hugging Face model initialization
def init_hf_pipeline():
    """Initialize a Hugging Face pipeline for text generation."""
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        import torch
        
        # Use a smaller model suitable for text generation tasks
        model_name = "google/flan-t5-large"  # A good balance of quality and speed
        
        logger.info(f"Loading Hugging Face model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            torch_dtype=torch.float16,  # Use half precision for efficiency
            device_map="auto"  # Automatically use GPU if available
        )
        
        # Create a text generation pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512
        )
        
        # Wrap the pipeline in LangChain's HuggingFacePipeline
        hf_llm = HuggingFacePipeline(pipeline=pipe)
        return hf_llm
    
    except Exception as e:
        logger.error(f"Error initializing Hugging Face pipeline: {e}")
        return None

# Check if fallback is forced via environment variable
def should_use_fallback():
    return os.environ.get("FORCE_FALLBACK", "false").lower() == "true"

# LLM with fallback mechanism
def get_llm(temperature=0.7):
    """Get an LLM instance, trying OpenAI first with HF fallback."""
    # Check if fallback is forced
    if should_use_fallback():
        logger.info("Fallback forced by environment variable")
        return init_hf_pipeline()
        
    try:
        # Try OpenAI first
        logger.info("Initializing OpenAI LLM")
        return ChatOpenAI(
            temperature=temperature,
            model_name="gpt-3.5-turbo"
        )
    except Exception as e:
        logger.warning(f"OpenAI initialization failed: {e}")
        
        # Fall back to Hugging Face
        logger.info("Falling back to Hugging Face model")
        hf_llm = init_hf_pipeline()
        if hf_llm:
            return hf_llm
        else:
            logger.error("Both OpenAI and Hugging Face fallback failed")
            return None

# Add a wrapper function for LLM calls with fallback
def call_llm_with_fallback(prompt_content: str, temperature: float = 0.7) -> str:
    """Call LLM with fallback mechanism."""
    # Check if fallback is forced
    if should_use_fallback():
        logger.info("Using Hugging Face model (forced)")
        hf_llm = init_hf_pipeline()
        if hf_llm:
            response = hf_llm(prompt_content)
            return response
        else:
            return "Error: Failed to initialize fallback model."
    
    # Try OpenAI first
    try:
        llm = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo")
        response = llm([HumanMessage(content=prompt_content)])
        return response.content
    except Exception as e:
        logger.warning(f"OpenAI call failed: {e}")
        
        # Fall back to Hugging Face
        try:
            hf_llm = init_hf_pipeline()
            if hf_llm:
                response = hf_llm(prompt_content)
                return response
            else:
                return f"Error: Failed to initialize fallback model."
        except Exception as e:
            logger.error(f"Hugging Face fallback also failed: {e}")
            return f"Error: Both primary and fallback LLM calls failed. {str(e)}"

def summarize(text: str) -> str:
    """Summarize the given text in 1-2 sentences."""
    prompt = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["text"])
    prompt_content = prompt.format(text=text)
    return call_llm_with_fallback(prompt_content, temperature=0.7)

def generate_titles(text: str, n: int = 3) -> List[str]:
    """Generate n creative titles based on the text."""
    prompt = PromptTemplate(template=TITLES_TEMPLATE, input_variables=["text", "n"])
    prompt_content = prompt.format(text=text, n=n)
    
    response = call_llm_with_fallback(prompt_content, temperature=0.8)
    
    # Parse the response to extract individual titles
    titles = response.strip().split("\n")
    return [t.strip() for t in titles if t.strip()]

def answer_question(text: str, question: str) -> str:
    """Answer a specific question about the text."""
    prompt = PromptTemplate(template=QA_TEMPLATE, input_variables=["text", "question"])
    prompt_content = prompt.format(text=text, question=question)
    
    return call_llm_with_fallback(prompt_content, temperature=0.3)

def recommendations(text: str, n: int = 2) -> List[str]:
    """Generate n recommendations based on the text."""
    prompt = PromptTemplate(template=RECS_TEMPLATE, input_variables=["text", "n"])
    prompt_content = prompt.format(text=text, n=n)
    
    response = call_llm_with_fallback(prompt_content, temperature=0.5)
    
    # Parse the response to extract individual recommendations
    recs = response.strip().split("\n")
    return [r.strip() for r in recs if r.strip()]
