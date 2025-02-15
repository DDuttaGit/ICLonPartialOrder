#!/bin/bash

sudo apt install curl
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull gemma2
ollama pull llama3
ollama pull mathstral
ollama pull qwen2-math:7b
ollama pull phi3:14b

pip install ollama simpletransformers openai tenacity tqdm

sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super
