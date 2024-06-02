import pytest

from installation_instruction.installation_instruction import InstallationInstruction


def test_validate_and_render(user_input_tests):

    install = InstallationInstruction.from_file(user_input_tests.get("example_file_path"))
    
    good_installation_instruction = install.validate_and_render(user_input_tests.get("valid_data"))
    assert user_input_tests.get("expected_data") == good_installation_instruction
    
    with pytest.raises(Exception):
        install.validate_and_render(user_input_tests.get("invalid_data"))



def test_parse_schema(test_data_flags_options):
    from .conftest import example_schemas
    install = InstallationInstruction.from_file(example_schemas.get("pytorch"))
    install.schema = test_data_flags_options
    schema = install.parse_schema()
    print(schema)
    
    assert schema["packager"] == {
        "title": "Packager",
        "description": "The package manager of your choosing.",
        "default": "pip",
        "type": "enum",
        "enum": [
            {
                "title": "pip",
                "value": "pip",
                "description": ""
            },
            {
                "title": "conda",
                "value": "conda",
                "description": ""
            }
        ]
    }

    assert schema["compute_platform"] == {
        "title": "Compute Platform",
        "description": "Should your gpu or your cpu handle the task?",
        "enum": [
            {
                "title": "CUDA 11.8",
                "value": "cu118",
                "description": ""
            },
            {
                "title": "CUDA 12.1",
                "value": "cu121",
                "description": "CUDA 12.1 is the latest version of CUDA."
            }
        ],
        "default": "cu118",
        "type": "enum"
    }

    assert schema["title"] == "Scikit-learn installation schema"
    assert schema["description"] == "This is a Schema to construct installation instructions for the python package scikit-learn by Timo Ege."