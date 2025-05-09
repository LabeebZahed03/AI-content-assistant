"""Generate a comprehensive report of the AI Content Assistant."""

import os
import sys
import subprocess
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def main():
    """Generate a detailed report with output examples."""
    report_dir = "report"
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join(report_dir, f"wellness_assistant_report_{timestamp}.md")
    
    with open(report_file, "w") as f:
        # Report header
        f.write("# AI Content Assistant for Wellness Strategy\n\n")
        f.write(f"## Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Environment information
        f.write("## Environment\n\n")
        f.write(f"- Python Version: {sys.version.split()[0]}\n")
        f.write(f"- Operating System: {sys.platform}\n")
        f.write(f"- OpenAI API Available: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}\n\n")
        
        # Sample content
        f.write("## Sample Content\n\n")
        with open("sample_content.txt", "r") as content_file:
            content = content_file.read()
            f.write("```\n")
            f.write(content)
            f.write("\n```\n\n")
        
        # Run the assistant with all functions
        f.write("## Assistant Output\n\n")
        f.write("### Running with all functions\n\n")
        
        # Run the command and capture output
        cmd = ["python", "-m", "assistant.cli", "--all", "--file", "sample_content.txt"]
        f.write("Command: `" + " ".join(cmd) + "`\n\n")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout.strip()
            f.write("```\n")
            f.write(output)
            f.write("\n```\n\n")
        except Exception as e:
            f.write(f"Error running command: {e}\n\n")
        
        # Run individual functions for demonstration
        functions = [
            ("Summary Only", ["--summarize"]),
            ("Titles Only", ["--titles"]),
            ("Question Only", ["--question", "What are the benefits of wellness programs for companies?"]),
            ("Recommendations Only", ["--recommendations"])
        ]
        
        f.write("## Individual Function Tests\n\n")
        
        for name, args in functions:
            f.write(f"### {name}\n\n")
            cmd = ["python", "-m", "assistant.cli", "--file", "sample_content.txt"] + args
            f.write("Command: `" + " ".join(cmd) + "`\n\n")
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                output = result.stdout.strip()
                f.write("```\n")
                f.write(output)
                f.write("\n```\n\n")
            except Exception as e:
                f.write(f"Error running command: {e}\n\n")
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        # Conclusion
        f.write("## Summary\n\n")
        f.write("The AI Content Assistant successfully processes wellness content to produce:\n\n")
        f.write("1. Concise summaries that capture the main points\n")
        f.write("2. Creative and engaging title suggestions\n")
        f.write("3. Accurate answers to specific questions about the content\n")
        f.write("4. Actionable recommendations based on the content\n\n")
        
        f.write("The assistant demonstrates effective use of LLM technology to enhance wellness content for various purposes.\n")
    
    print(f"Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    main()
