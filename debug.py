"""Script to debug content processing."""

import os
import sys
from dotenv import load_dotenv
from assistant.core import summarize, generate_titles, answer_question, recommendations

load_dotenv()

def main():
    """Run direct test of core functions."""
    sample_path = "sample_content.txt"
    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading sample content: {e}")
        sys.exit(1)

    print(f"Read {len(content)} characters from {sample_path}")
    print("Content:")
    print("-" * 50)
    print(content)
    print("-" * 50)

    # Test each function directly
    print("\nTesting summarize function:")
    summary = summarize(content)
    print(f"Summary result: {summary}")

    print("\nTesting generate_titles function:")
    titles = generate_titles(content, n=3)
    print("Titles result:")
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")

    print("\nTesting answer_question function:")
    question = "What are the benefits of wellness programs for companies?"
    answer = answer_question(content, question)
    print(f"Answer result: {answer}")

    print("\nTesting recommendations function:")
    recs = recommendations(content, n=2)
    print("Recommendations result:")
    for i, rec in enumerate(recs, 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    main()
