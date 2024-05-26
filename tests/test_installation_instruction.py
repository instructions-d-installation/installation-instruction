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


