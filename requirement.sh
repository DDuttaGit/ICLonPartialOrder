#!/bin/bash

sudo apt install curl
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull gemma2
ollama pull llama3
ollama pull mathstral

pip install ollama simpletransformers

sudo apt-get install dvipng texlive-latex-extra texlive-fonts-recommended cm-super
