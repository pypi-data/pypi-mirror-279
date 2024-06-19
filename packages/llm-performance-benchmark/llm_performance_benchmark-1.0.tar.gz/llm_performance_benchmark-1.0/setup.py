from setuptools import setup, find_packages

setup(
    name="llm_performance_benchmark", 
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.14.1",
        "tiktoken>=0.6.0",
    ],
    python_requires=">=3.7.1",
    author="Artificial Analysis",
    author_email="hello@artificial.ai",
    description="Benchmark the performance (output speed, latency) of OpenAI compatible endpoints",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ArtificialAnalysis/LLM-Performance-Benchmark",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
