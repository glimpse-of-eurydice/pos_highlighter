# Part-of-Speech (POS) Highlighter

This project is a command-line tool that processes a Markdown file and highlights workds of a specific part of speech (POS) using SpaCy's POS tagging functionality.
By default, this program underlines all nouns in Markdown format, but users can specify other POS tags.

## Features
- Processes a Markdown file and highlights words of a specific POS.
- By default, only nouns are underlined.
- Supports an optional flag
`--pos <tag>` to highlight different part-of-speech (e.g. verbs, adjectives, adverbs, etc.).
- Uses a `config.json` file for customizable setting.

## Installation
This project uses Poetry for dependency management.
(https://python-poetry.org/)

## Set up
1. Clone this repository:
```
git clone <repository-url>
cd pos_highlighter
```
2. Install dependencies using Poetry:
```
poetry install
```
3. Activate the virtual enviroment:
```
poetry shell
```
4. Ensure you have the required spaCy model installed:
```
poetry run python -m spacy download en_core_web_sm
```

## Usage
### Running the program
To process a Markdown file and underline nouns as default behavior:
```
python pos_highlighter/highlighter.py example.md
```

To specify a different part of speech:
```
poetry run python pos_highlighter/highlighter.py example.md --pos VERB
```

### Example Output
Input(`example.md`):
```
Introduction
These exercises are intended to stimulate discussion, and some might be set as term projects.
Alternatively, preliminary attempts can be made now, and these attempts can be reviewed after the completion of the book.
```

Output(`output.md`):
```
_Introduction_
These _exercises_ are intended to stimulate _discussion_, and some might be set as _term_ _projects_.
Alternatively, preliminary _attempts_ can be made now, and these _attempts_ can be reviewed after the _completion_ of the _book_.
```

## Running Tests
Run the unit tests using `pytest`
```
pytest tests/test.py
```

## Configuration
The `config.json` file allows customization of settings such as the default POS tag and output file location:
```
{
    "default_pos": "NOUN",
    "output_file": "output.md",
    "spacy_model": "en_core_web_sm",
    "error_handling":{
        "strict_mode": false,
        "log_warnings": true
    }
}
```
