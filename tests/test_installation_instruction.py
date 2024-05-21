import pytest

from installation_instruction.installation_instruction import InstallationInstruction

@pytest.mark.parametrize("test_data_user_input", ["pytorch_invalid_data.txt", "pytorch_valid_data.txt"])
def test_validate_and_render_pytorch(test_data_user_input):
    test_data = test_data_user_input
    file_name = test_data[0]
    user_input = test_data[1]
    install = InstallationInstruction.from_file("examples/pytorch/pytorch-instruction.schema.yml.jinja")

    if "_valid_" in file_name:
        good_installation_instruction = install.validate_and_render(user_input)
        assert ('Windows does not support ROCm!', True) == good_installation_instruction
    elif "_invalid_" in file_name:
        with pytest.raises(Exception):
            install.validate_and_render(user_input)

@pytest.mark.parametrize("test_data_user_input", ["scikit_invalid_data.txt", "scikit_valid_data.txt"])
def test_validate_and_render_scikit(test_data_user_input):
    test_data = test_data_user_input
    file_name = test_data[0]
    user_input = test_data[1]

    install = InstallationInstruction.from_file("examples/scikit-learn/scikit-learn-instruction.schema.yml.jinja")

    if "_valid_" in file_name:
        good_installation_instruction = install.validate_and_render(user_input)
        assert ('pip install -U scikit-learn', False) == good_installation_instruction
    elif "_invalid_" in file_name:
        with pytest.raises(Exception):
            install.validate_and_render(user_input)

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
    assert ('pip install -U pip setuptools wheel pip install -U spacy', False) == good_installation_instruction

    with pytest.raises(Exception):
        install.validate_and_render(invalid_user_input)
