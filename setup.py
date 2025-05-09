from setuptools import setup, find_packages

setup(
    name="ai-content-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.0.335",
        "langchain-community>=0.0.16",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "rich>=13.4.2",
        "transformers>=4.33.1",
        "torch>=2.0.1",
    ],
    entry_points={
        "console_scripts": [
            "wellness-assistant=assistant.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="AI Content Assistant for Wellness Strategy",
    keywords="ai, content, wellness, assistant",
    python_requires=">=3.8",
)
