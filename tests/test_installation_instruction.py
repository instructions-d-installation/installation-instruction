import pytest

from installation_instruction.installation_instruction import InstallationInstruction


def test_validate_and_render(user_input_tests):

    install = InstallationInstruction.from_file(user_input_tests.get("schema_path"))
    expected_output = user_input_tests.get("expected_output")

    if expected_output is None:
        with pytest.raises(Exception):
            install.validate_and_render(user_input_tests.get("input"))
    else:
        good_installation_instruction = install.validate_and_render(user_input_tests.get("input"))
        expected = expected_output.split("\n")
    
        expected_command = expected[0] if len(expected) > 0 else ""
        expected_flag = expected[1] == "True" if len(expected) > 1 else False

        assert (expected_command, expected_flag) == good_installation_instruction
        
def test_parse_schema(test_data_flags_options_config_string_with_empty_template):
    config = test_data_flags_options_config_string_with_empty_template
    install = InstallationInstruction(config)
    schema = install.parse_schema()
    
    assert schema["properties"]["packager"] == {
        "title": "Packager",
        "description": "The package manager of your choosing.",
        "default": "pip",
        "type": "enum",
        "key": "packager",
        "enum": [
            {
                "title": "pip",
                "key": "pip",
                "description": ""
            },
            {
                "title": "conda",
                "key": "conda",
                "description": ""
            }
        ]
    }

    assert schema["properties"]["compute_platform"] == {
        "title": "Compute Platform",
        "description": "Should your gpu or your cpu handle the task?",
        "key": "compute_platform",
        "enum": [
            {
                "title": "CUDA 11.8",
                "key": "cu118",
                "description": ""
            },
            {
                "title": "CUDA 12.1",
                "key": "cu121",
                "description": "CUDA 12.1 is the latest version of CUDA."
            }
        ],
        "default": "cu118",
        "type": "enum"
    }

    assert schema["title"] == "Scikit-learn installation schema"
    assert schema["description"] == "This is a Schema to construct installation instructions for the python package scikit-learn by Timo Ege."

    assert schema["properties"]["virtualenv"] == {
        "title": "Use pip virtualenv",
        "description": "Choose if you want to use a virtual environment to install the package.",
        "default": False,
        "type": "boolean",
        "key": "virtualenv"
    }

    assert schema["properties"]["verbose"]["description"] == "Activate verbose output."