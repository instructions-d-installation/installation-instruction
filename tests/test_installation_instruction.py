import pytest

from installation_instruction.installation_instruction import InstallationInstruction


def test_validate_and_render(user_input_tests):

    install = InstallationInstruction.from_file(user_input_tests.get("example_file_path"))
    
    good_installation_instruction = install.validate_and_render(user_input_tests.get("valid_data"))
    assert user_input_tests.get("expected_data") == good_installation_instruction
    
    with pytest.raises(Exception):
        install.validate_and_render(user_input_tests.get("invalid_data"))


