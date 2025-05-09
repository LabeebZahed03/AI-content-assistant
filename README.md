## Demo Output

Here's a sample of the AI Content Assistant processing the wellness content:

```
Read 476 characters from sample_content.txt
Processing content...
Results:
╭─────────────────────────────────────────────────────────────────────── Summary ────────────────────────────────────────────────────────────────────────╮
│ Wellness is a comprehensive approach to achieving overall health through practices like mindfulness, nutrition, and exercise. Prioritizing wellness    │
│ can lead to better professional performance and companies benefit from investing in employee wellness programs through increased productivity and a    │
│ positive workplace culture.                                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                             Generated Titles                              
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Title                                                                   ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. Unlocking the Power of Wellness: A Holistic Approach to Health       │
│ 2. Enhancing Performance and Satisfaction: The Impact of Wellness       │
│ 3. Investing in Wellness: The Key to a Healthy and Productive Workplace │
└─────────────────────────────────────────────────────────────────────────┘
╭───────────────────────────────────────────────────────────────────────── Q&A ──────────────────────────────────────────────────────────────────────────╮
│ increased productivity, reduced absenteeism, and a positive workplace culture.                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                     Recommendations                                                                      
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Recommendation                                                                                                                                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ • Offer a variety of wellness activities and resources to cater to different interests and needs of employees, such as yoga classes, nutrition         │
│ workshops, mental health resources, and fitness challenges.                                                                                            │
│ • Provide incentives or rewards for employees who actively participate in the wellness program, such as gift cards, extra time off, or discounts on    │
│ health-related services. This can help motivate employees to engage in the program and reap the benefits of improved health and well-being.            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The assistant successfully processes the wellness content to provide:
1. A concise summary
2. Creative title suggestions
3. Answers to specific questions
4. Actionable recommendations# AI Content Assistant for Wellness Strategy

A Python-based tool that uses LLM technology to process and enhance wellness-related content.

## Features

- **Summarization**: Condense content into 1-2 concise sentences
- **Title Generation**: Create engaging, attention-grabbing titles
- **Question Answering**: Extract specific information from content
- **Recommendation Generation**: Generate actionable insights
- **Robust Fallback**: Automatic fallback to Hugging Face model if OpenAI is unavailable

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/ai-content-assistant.git
   cd ai-content-assistant
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment
   - Windows: `venv\Scripts\activate`
   - MacOS/Linux: `source venv/bin/activate`

4. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file to add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Process all functions at once

```bash
python -m assistant.cli --all --file sample_content.txt
```

### Run specific functions

```bash
# Generate summary only
python -m assistant.cli --file sample_content.txt --summarize

# Generate titles only
python -m assistant.cli --file sample_content.txt --titles

# Answer a specific question
python -m assistant.cli --file sample_content.txt --question "What are the benefits of wellness programs?"

# Generate recommendations
python -m assistant.cli --file sample_content.txt --recommendations
```

### Use direct text input

```bash
python -m assistant.cli --text "Your wellness content here" --all
```

### Force using the fallback model

If you want to test without an OpenAI API key or in an offline environment:

```bash
python -m assistant.cli --all --file sample_content.txt --force-fallback
```

## Fallback Mechanism

This application includes a robust fallback mechanism:

1. **Primary LLM**: Uses OpenAI's GPT models for optimal quality
2. **Fallback LLM**: Automatically switches to a Hugging Face model (google/flan-t5-large) if OpenAI is unavailable

Benefits of this approach:
- Increased reliability and uptime
- Works in environments without internet access or API keys
- Reduces dependency on external services

The fallback model is initialized only when needed to ensure efficient resource usage.

## Architecture

This project uses LangChain to interface with LLM models (OpenAI and Hugging Face). The architecture consists of:

1. **Core Module**: Contains the fundamental LLM interaction functions with fallback capability
2. **Pipeline Module**: Orchestrates the execution of multiple functions
3. **CLI Module**: Provides a user-friendly command-line interface

## Design Decisions

- **LangChain Integration**: Provides flexibility to switch models if needed
- **Fallback Mechanism**: Ensures the application works even when OpenAI API is unavailable
- **Modular Architecture**: Each function is self-contained for easier testing and maintenance
- **Rich CLI Output**: Enhanced readability in terminal environment
- **Error Handling**: Graceful handling of API failures and input issues

## Future Enhancements

- Web UI using Streamlit
- Support for additional LLM providers
- Enhanced caching for performance optimization
- RAG (Retrieval Augmented Generation) capabilities

## License

MIT