"""Command-line interface for the AI Content Assistant."""

import argparse
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .pipelines import process_all, process_selected

console = Console()

def read_from_file(file_path: str) -> str:
    """Read content from a file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        sys.exit(1)

def display_results(results):
    """Display results in a nicely formatted way."""
    if "summary" in results:
        console.print(Panel(results["summary"], title="Summary", border_style="green"))
    
    if "titles" in results:
        title_table = Table(title="Generated Titles")
        title_table.add_column("Title")
        
        for i, title in enumerate(results["titles"], 1):
            title_table.add_row(f"{i}. {title}")
        
        console.print(title_table)
    
    if "answer" in results:
        console.print(Panel(results["answer"], title="Q&A", border_style="blue"))
    
    if "recommendations" in results:
        rec_table = Table(title="Recommendations")
        rec_table.add_column("Recommendation")
        
        for i, rec in enumerate(results["recommendations"], 1):
            rec_table.add_row(f"• {rec}")
        
        console.print(rec_table)

def check_api_key():
    """Check if OpenAI API key is set."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and not os.environ.get("FORCE_FALLBACK", "false").lower() == "true":
        console.print("[yellow]Warning: OPENAI_API_KEY environment variable not set.[/yellow]")
        console.print("[yellow]Set it in the .env file or use the fallback model with FORCE_FALLBACK=true.[/yellow]")

def main():
    """Main entry point for the CLI."""
    # Check API key
    check_api_key()
    
    parser = argparse.ArgumentParser(description="AI Content Assistant for Wellness Strategy")
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", "-f", type=str, help="Path to content file")
    input_group.add_argument("--text", "-t", type=str, help="Direct text input")
    
    # Processing options
    parser.add_argument("--summarize", "-s", action="store_true", help="Summarize content")
    parser.add_argument("--titles", "-l", action="store_true", help="Generate titles")
    parser.add_argument("--question", "-q", type=str, help="Ask a question about the content")
    parser.add_argument("--recommendations", "-r", action="store_true", help="Generate recommendations")
    parser.add_argument("--all", "-a", action="store_true", help="Run all functions")
    parser.add_argument("--force-fallback", action="store_true", help="Force using the fallback model")
    
    args = parser.parse_args()
    
    # Handle force fallback flag
    if args.force_fallback:
        os.environ["FORCE_FALLBACK"] = "true"
        console.print("[yellow]Forcing use of fallback model[/yellow]")
    
    # Get content
    if args.file:
        content = read_from_file(args.file)
    else:
        content = args.text
    
    if not content:
        console.print("[bold red]Error: Empty content provided[/bold red]")
        sys.exit(1)
    
    # Process content
    console.print("[bold]Processing content...[/bold]")
    
    if args.all:
        default_question = "What are the benefits of wellness programs for companies?"
        results = process_all(content, question=default_question)
    else:
        results = process_selected(
            content,
            do_summary=args.summarize,
            do_titles=args.titles,
            question=args.question,
            do_recommendations=args.recommendations
        )
    
    if not results:
        console.print("[yellow]No processing options selected. Use --help to see available options.[/yellow]")
        return
    
    # Display results
    console.print("[bold]Results:[/bold]")
    display_results(results)

if __name__ == "__main__":
    main()
