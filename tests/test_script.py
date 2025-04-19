# tests/test_script.py

import pytest
from typer.testing import CliRunner

# Import the main app and script module specifics
from codex_cli.main import app
from codex_cli import script as script_module
from codex_cli.script import clean_generated_code # Import specific function to test

# Runner for invoking CLI commands
runner = CliRunner()

# Mocked script responses from OpenAI
MOCK_BASH_SCRIPT = "#!/bin/bash\nls -la # Mock bash script"
MOCK_PYTHON_SCRIPT = "#!/usr/bin/env python\nprint('Hello') # Mock python script"
MOCK_SCRIPT_WITH_FENCES_RAW = """```python
#!/usr/bin/env python
print("This code has fences")
```"""
MOCK_SCRIPT_WITH_FENCES_CLEANED = """#!/usr/bin/env python
print("This code has fences")"""

# --- Test Suite for 'script' command ---

@pytest.mark.parametrize(
    "script_type, mock_response",
    [
        ("bash", MOCK_BASH_SCRIPT),
        ("python", MOCK_PYTHON_SCRIPT),
        ("powershell", "# Mock PowerShell script"), # Simple mock for powershell
    ]
)
def test_script_command_success(mocker, script_type, mock_response):
    """Test successful script generation for various types."""
    mock_api_call = mocker.patch('codex_cli.script.get_openai_response', return_value=mock_response)
    task = f"generate a {script_type} script"
    result = runner.invoke(app, ["script", task, "--type", script_type])

    # Assertions
    assert result.exit_code == 0
    # --- FIX: More robust check for mock response in output ---
    # Check if the *first* line of the mock response is present, handles single/multi-line
    assert mock_response.splitlines()[0] in result.stdout
    assert "Generated Script:" in result.stdout
    assert "⚠️ Warning:" in result.stdout
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    assert f"Desired Script Type: {script_type}" in args[0]


def test_script_command_default_type(mocker):
    """Test that the default script type is bash when --type is omitted."""
    mock_api_call = mocker.patch('codex_cli.script.get_openai_response', return_value=MOCK_BASH_SCRIPT)
    task = "default to bash"

    result = runner.invoke(app, ["script", task]) # No --type flag

    assert result.exit_code == 0
    assert MOCK_BASH_SCRIPT.splitlines()[1] in result.stdout # Check for bash script content
    assert "Generated Script:" in result.stdout
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    # Check that 'bash' was implicitly requested in the prompt
    assert "Desired Script Type: bash" in args[0]

def test_script_command_unsupported_type(mocker):
    """Test behavior with an unsupported script type."""
    # Mock API call (shouldn't be called)
    mock_api_call = mocker.patch('codex_cli.script.get_openai_response')
    task = "unsupported type test"
    unsupported_type = "cobol"

    result = runner.invoke(app, ["script", task, "--type", unsupported_type])

    # Assertions
    assert result.exit_code == 0 # Command should exit gracefully
    assert f"Error: Unsupported script type '{unsupported_type}'" in result.stdout
    assert "Generated Script:" not in result.stdout # No script should be generated
    mock_api_call.assert_not_called() # API should not be called

def test_script_command_api_failure(mocker):
    """Test behavior when the OpenAI API call fails."""
    # Mock API call to return None
    mock_api_call = mocker.patch('codex_cli.script.get_openai_response', return_value=None)
    task = "api failure test"
    script_type = "python"

    result = runner.invoke(app, ["script", task, "--type", script_type])

    # Assertions
    assert result.exit_code == 0
    assert f"Failed to generate the {script_type} script" in result.stdout
    assert "Generated Script:" not in result.stdout
    mock_api_call.assert_called_once()

# --- Tests for the clean_generated_code utility function ---

@pytest.mark.parametrize(
    "raw_code, language, expected_cleaned_code",
    [
        # Code without fences
        (MOCK_BASH_SCRIPT, "bash", MOCK_BASH_SCRIPT),
        # Code with python fences
        (MOCK_SCRIPT_WITH_FENCES_RAW, "python", MOCK_SCRIPT_WITH_FENCES_CLEANED),
        # Code with generic fences (no language specified)
        ("```\ngeneric code\n```", "python", "generic code"),
        # Code with fences and extra whitespace/newlines
        ("  ```python\n  padded code\n  ```  \n", "python", "padded code"),
        # Code that only contains fences
        ("```python\n```", "python", ""),
        # Empty input
        ("", "bash", ""),
        # Input that is just whitespace
        ("   \n  ", "python", ""),
        # Code with triple backticks inside (should not be removed)
        ("echo '``` Mismatched backticks ```'", "bash", "echo '``` Mismatched backticks ```'"),
    ]
)
def test_clean_generated_code(raw_code, language, expected_cleaned_code):
    """Test the clean_generated_code function with various inputs."""
    cleaned = clean_generated_code(raw_code, language)
    assert cleaned == expected_cleaned_code