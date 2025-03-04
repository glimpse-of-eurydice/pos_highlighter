import json
import spacy
import argparse
import sys
import os

def load_config():
    """Load the configuration file safely."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get project root
    config_path = os.path.join(base_dir, "config.json")  
    
    default_config = {
        "default_pos": "NOUN",
        "output_file": "output.md",
        "spacy_model": "en_core_web_sm",
        "error_handling": {
            "strict_mode": False,
            "log_warnings": True
        }
    }
    
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config

    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}. Using defaults.")
        return {"default_pos": "NOUN", "output_file": "output.md"}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json.")
        sys.exit(1)
    

def load_spacy_model(config):
    """
    Load the English SpaCy model.
    """
    model_name = config.get("spacy_model", "en_core_web_sm")
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Error: Unable to load SpaCy model '{model_name}'.")
        sys.exit(1)
    
def highlight_pos_word(text: str, pos: str, nlp) -> str:
    """This function detect word of specific part of speech and add underscore to it.
    
    Supported POS tags:
    - NOUN (nouns)
    - VERB (verbs)
    - ADJ (adjectives)
    - ADV (adverbs)
    - ADP, AUX, CCONJ, DET. INTJ, NUM, etc.
    
    
    Args:
        text (str): The input text
        pos (str): The part of speech to highlight
        
    Returns:
        str: The modified text with underlined words
    """
    
    highlighted_text = []
    doc = nlp(text)
   
    for token in doc:
        if token.pos_ == pos.upper():
            highlighted_text.append(f"_{token.text}_")
        else:
            highlighted_text.append(token.text)
        
    return "".join([word + token.whitespace_ for token, word in zip(doc, highlighted_text)])

def write_into_file(highlighted_text: str, output_path):
    """Write the highlighted text into a markdown file."""
    with open(output_path, "w") as file:
        file.write(highlighted_text + "\n")
    
def main():
    
    """
    
    The main function of the program. 
    It loads the configs, process POS highlighting, and save the output
    It reads the text from a markdown file, use spacy to parse it.
    The file path is provided as a command-line argument. 
    If the file is not found or is not a markdown file, the program prints an error message exits.
    
    """
    
    config = load_config()
    print("Loading the configs...")
    
    parser = argparse.ArgumentParser(description="Highlight POS in a markdown file.")
    parser.add_argument("input_file", type=str, help="Path to the markdown file.")
    
    parser.add_argument("--pos", type=str, default=config.get("default_pos", "NOUN"),
                        help="Part of speech to highlight (default: NOUN).\n Supports: NOUN, VERB, ADJ, ADV, etc.")
    args = parser.parse_args()
    print("Configs parsed successfully.")
    
    print(f"Reading the input file {args.input_file}...")
    # check if the file is a markdown file
    if not args.input_file.endswith(".md"):
        print("Error: Please provide a Markdown file (.md).")
        sys.exit(1)
    
    nlp = load_spacy_model(config)
    
    try:
        with open(args.input_file, "r") as file:
            highlighted_lines = []
            print(f"Start highlighting words of POS {args.pos}...\nThis may take a while...")
            for line in file:
                highlighted_lines.append(highlight_pos_word(line.strip(), args.pos, nlp))
        
            print("Writing to the highlighted text to the output file...")
        
            # Join lines into a single string and write to output file
            highlighted_text = "\n".join(highlighted_lines)
            output_path = config.get("output_file", "output.md")
            write_into_file(highlighted_text, output_path)
            print(f"Highlighted text has been saved to {output_path}")
                
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    

if __name__ == "__main__":
    main()