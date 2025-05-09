# AI Content Assistant for Wellness Strategy

## Project Submission

This submission addresses the requirements of creating a Python script that uses an LLM to process and enhance wellness-related content.

### Tasks Implemented:

1. **Content Summarization**
   - The assistant successfully condenses the wellness content into 1-2 concise sentences
   - Example: "Wellness is a comprehensive approach to achieving overall health through practices like mindfulness, nutrition, and exercise. Prioritizing wellness can lead to better professional performance and companies benefit from investing in employee wellness programs through increased productivity and a positive workplace culture."

2. **Title Generation**
   - The assistant generates three creative, attention-grabbing titles
   - Examples:
     - "Unlocking the Power of Wellness: A Holistic Approach to Health"
     - "Enhancing Performance and Satisfaction: The Impact of Wellness"
     - "Investing in Wellness: The Key to a Healthy and Productive Workplace"

3. **Question Answering**
   - The assistant accurately answers the specific question about wellness programs
   - Question: "What are the benefits of wellness programs for companies?"
   - Answer: "increased productivity, reduced absenteeism, and a positive workplace culture."

4. **Recommendation Generation**
   - The assistant provides actionable recommendations for implementing wellness programs
   - Examples:
     - "Offer a variety of wellness activities and resources to cater to different interests and needs of employees..."
     - "Provide incentives or rewards for employees who actively participate in the wellness program..."

### Technical Implementation:

- **Modular Design**: Separate functions for each task (summarize, generate_titles, answer_question, recommendations)
- **CLI Interface**: Easy-to-use command-line interface with clear options
- **Fallback Mechanism**: Automatic fallback to Hugging Face models if OpenAI is unavailable
- **Error Handling**: Robust validation and error reporting throughout the application

### Usage:

```bash
# Process all functions at once
python -m assistant.cli --all --file sample_content.txt

# Run specific functions
python -m assistant.cli --file sample_content.txt --summarize
python -m assistant.cli --file sample_content.txt --titles
python -m assistant.cli --file sample_content.txt --question "What are the benefits of wellness programs for companies?"
python -m assistant.cli --file sample_content.txt --recommendations
```

### Sample Output:

See the `sample_output.txt` file for complete output from the application.

### Repository:

The complete codebase is available at: [GitHub Repository URL]
