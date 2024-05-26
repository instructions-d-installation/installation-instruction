import pytest

from installation_instruction.installation_instruction import InstallationInstruction


def test_validate_and_render(user_input_tests):
    valid_input = user_input_tests[1]
    invalid_input = user_input_tests[2]
    expected_output = user_input_tests[3]
    install = InstallationInstruction.from_file(user_input_tests[0])
    
    good_installation_instruction = install.validate_and_render(valid_input)
    assert expected_output == good_installation_instruction
    
    with pytest.raises(Exception):
        install.validate_and_render(invalid_input)

def test_validate_and_render_spacy():
    valid_user_input = {
        "os": "windows",
        "platform": "x86",
        "package": "pip",
        "hardware": "cpu"
    }

    invalid_user_input = {
        "os": "windows",
        "platform": "arm",
        "package": "forge",
        "hardware": "cpu"
    }

    install = InstallationInstruction.from_file("examples/spacy/spacy-instruction.schema.yml.jinja")

    good_installation_instruction = install.validate_and_render(valid_user_input)
    assert ('pip install -U pip setuptools wheel && pip install -U spacy', False) == good_installation_instruction

    with pytest.raises(Exception):
        install.validate_and_render(invalid_user_input)
