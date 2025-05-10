"""Core LLM functions for the AI Content Assistant."""

import os
from typing import List
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, 
                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define prompt templates
SUMMARY_TEMPLATE = "You are an expert editor.\nSummarize the following passage in 1-2 crisp sentences:\n\n\"\"\"\n{text}\n\"\"\""

TITLES_TEMPLATE = "Generate {n} creative, catchy blog titles for the passage below.\nReturn them as plain text, one per line, without numbering.\n\n\"\"\"\n{text}\n\"\"\""

QA_TEMPLATE = "Answer the question using ONLY the passage.\nIf the answer is not found in the passage, say \"Not found.\"\n\nPassage:\n\"\"\"\n{text}\n\"\"\"\n\nQ: {question}\nA:"

RECS_TEMPLATE = "Give {n} actionable recommendations for a company looking to implement a wellness program,\nbased on this passage. Provide each recommendation on a new line without bullet points or numbering.\n\n\"\"\"\n{text}\n\"\"\""

# Hugging Face model initialization
def init_hf_pipeline():
    """Initialize a Hugging Face pipeline for text generation."""
    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
        import torch
        
        # Use a smaller model suitable for text generation tasks
        model_name = "google/flan-t5-base"  # Smaller model, faster loading
        
        logger.info(f"Loading Hugging Face model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, 
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512
        )
        
        hf_llm = HuggingFacePipeline(pipeline=pipe)
        return hf_llm
    
    except Exception as e:
        logger.error(f"Error initializing Hugging Face pipeline: {e}")
        return None

# Check if fallback is forced via environment variable
def should_use_fallback():
    return os.environ.get("FORCE_FALLBACK", "false").lower() == "true"

# Add a wrapper function for LLM calls with fallback
def call_llm_with_fallback(prompt_content: str, temperature: float = 0.7) -> str:
    """Call LLM with fallback mechanism."""
    if should_use_fallback():
        logger.info("Using Hugging Face model (forced)")
        hf_llm = init_hf_pipeline()
        if hf_llm:
            response = hf_llm.invoke(prompt_content)
            return response
        else:
            return "Error: Failed to initialize fallback model."
    
    try:
        llm = ChatOpenAI(temperature=temperature, model_name="gpt-3.5-turbo")
        response = llm.invoke([HumanMessage(content=prompt_content)])
        return response.content
    except Exception as e:
        logger.warning(f"OpenAI call failed: {e}")
        
        try:
            hf_llm = init_hf_pipeline()
            if hf_llm:
                response = hf_llm.invoke(prompt_content)
                return response
            else:
                return f"Error: Failed to initialize fallback model."
        except Exception as e:
            logger.error(f"Hugging Face fallback also failed: {e}")
            return f"Error: Both primary and fallback LLM calls failed. {str(e)}"

def summarize(text: str) -> str:
    """Summarize the given text in 1-2 sentences."""
    if not text or not text.strip():
        logger.warning("Empty text provided to summarize function")
        return "Error: No content provided for summarization."
    
    logger.info(f"Summarizing text with length: {len(text)}")
    
    prompt = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["text"])
    prompt_content = prompt.format(text=text)
    
    return call_llm_with_fallback(prompt_content, temperature=0.7)

def generate_titles(text: str, n: int = 3) -> List[str]:
    """Generate n creative titles based on the text."""
    if not text or not text.strip():
        logger.warning("Empty text provided to generate_titles function")
        return ["Error: No content provided for title generation."]
    
    logger.info(f"Generating titles for text with length: {len(text)}")
    
    prompt = PromptTemplate(template=TITLES_TEMPLATE, input_variables=["text", "n"])
    prompt_content = prompt.format(text=text, n=n)
    
    response = call_llm_with_fallback(prompt_content, temperature=0.8)
    
    titles = response.strip().split("\n")
    return [t.strip() for t in titles if t.strip()]

def answer_question(text: str, question: str) -> str:
    """Answer a specific question about the text."""
    if not text or not text.strip():
        logger.warning("Empty text provided to answer_question function")
        return "Error: No content provided to answer the question."
    
    logger.info(f"Answering question about text with length: {len(text)}")
    
    prompt = PromptTemplate(template=QA_TEMPLATE, input_variables=["text", "question"])
    prompt_content = prompt.format(text=text, question=question)
    
    return call_llm_with_fallback(prompt_content, temperature=0.3)

def recommendations(text: str, n: int = 2) -> List[str]:
    """Generate n recommendations based on the text."""
    if not text or not text.strip():
        logger.warning("Empty text provided to recommendations function")
        return ["Error: No content provided for generating recommendations."]
    
    logger.info(f"Generating recommendations for text with length: {len(text)}")
    
    prompt = PromptTemplate(template=RECS_TEMPLATE, input_variables=["text", "n"])
    prompt_content = prompt.format(text=text, n=n)
    
    response = call_llm_with_fallback(prompt_content, temperature=0.5)
    
    recs = response.strip().split("\n")
    return [r.strip() for r in recs if r.strip()]