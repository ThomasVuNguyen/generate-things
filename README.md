# Generate Things

Generate OpenSCAD code for fruits using Ollama.

## Usage

```bash
python generate.py apple
python generate.py orange orange.scad
```

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start Ollama: `ollama serve`
3. Pull model: `ollama pull llama3.2`
4. Change model in `config.json` if needed