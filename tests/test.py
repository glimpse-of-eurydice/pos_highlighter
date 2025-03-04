import pytest
import json
import spacy
import os
from pos_highlighter.highlighter import highlight_pos_word, load_config, write_into_file  # Replace 'your_script' with the actual filename

@pytest.fixture
def sample_nlp():
    return spacy.load("en_core_web_sm")

# test highlight_pos_word function
def test_highlight_pos_word(sample_nlp):
    text = "The quick brown fox jumps over the lazy dog."
    pos = "ADJ"
    expected_output = "The _quick_ _brown_ fox jumps over the _lazy_ dog."
    assert highlight_pos_word(text, pos, sample_nlp) == expected_output

    pos = "NOUN"
    expected_output = "The quick brown _fox_ jumps over the lazy _dog_."
    assert highlight_pos_word(text, pos, sample_nlp) == expected_output

# test load_config function
def test_load_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_data = {
        "default_pos": "NOUN",
        "output_file": "output.md",
        "spacy_model": "en_core_web_sm",
        "error_handling": {"strict_mode": False, "log_warnings": True}
    }
    
    with open(config_path, "w") as file:
        json.dump(config_data, file)
    
    # Simulate loading from the temp config file
    os.environ["CONFIG_PATH"] = str(config_path) 
    config = load_config()
    
    assert config["default_pos"] == "NOUN"
    assert config["output_file"] == "output.md"
    assert config["spacy_model"] == "en_core_web_sm"
    assert config["error_handling"]["strict_mode"] is False
    assert config["error_handling"]["log_warnings"] is True

# test write_into_file function
def test_write_into_file(tmp_path):
    output_file = tmp_path / "test_output.md"
    content = "This is a test output."
    
    write_into_file(content, output_file)
    
    assert output_file.exists()
    with open(output_file, "r") as file:
        assert file.read().strip() == content
