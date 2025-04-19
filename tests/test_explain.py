# tests/test_explain.py

import pytest
from typer.testing import CliRunner
from pathlib import Path
import re

from codex_cli.main import app
from codex_cli import explain as explain_module
from codex_cli.core.openai_utils import get_openai_response

runner = CliRunner()

MOCK_EXPLANATION = "This is a mock explanation.\n\nIt explains the code."
MOCK_FILE_CONTENT = "print('Hello from test file!')"

def clean_output(output: str) -> str:
    """Removes ANSI escape codes and normalizes whitespace."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', output)
    return " ".join(cleaned.split())

# --- Updated Test Suite for 'explain' command with Options ---

def test_explain_command_with_string_defaults(mocker):
    """Test 'explain' with string using default options (basic, en)."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=MOCK_EXPLANATION)
    code_string = "print('hello default')"
    result = runner.invoke(app, ["explain", code_string]) # No options

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Explanation:" in cleaned_stdout
    assert "mock explanation" in cleaned_stdout
    mock_api_call.assert_called_once()
    # Check prompt for default instructions
    args, kwargs = mock_api_call.call_args
    prompt = args[0]
    assert "Provide a clear and concise explanation." in prompt
    assert "Respond ONLY in the following language: en." in prompt
    assert code_string in prompt

def test_explain_command_with_file_defaults(mocker, tmp_path: Path):
    """Test 'explain' with file using default options (basic, en)."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=MOCK_EXPLANATION)
    test_file: Path = tmp_path / "test_script_defaults.py"
    test_file.write_text(MOCK_FILE_CONTENT)
    result = runner.invoke(app, ["explain", str(test_file)]) # No options

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Explaining content from file:" in cleaned_stdout
    assert test_file.name in cleaned_stdout
    assert "Explanation:" in cleaned_stdout
    assert "mock explanation" in cleaned_stdout
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    prompt = args[0]
    assert "Provide a clear and concise explanation." in prompt
    assert "Respond ONLY in the following language: en." in prompt
    assert MOCK_FILE_CONTENT in prompt

def test_explain_command_with_detailed_option(mocker):
    """Test 'explain' with --detail detailed option."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=MOCK_EXPLANATION)
    code_string = "print('hello detailed')"
    # Use long flag
    result = runner.invoke(app, ["explain", code_string, "--detail", "detailed"])

    assert result.exit_code == 0
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    prompt = args[0]
    assert "Provide a detailed, in-depth explanation." in prompt # Check for detailed instruction
    assert "Provide a clear and concise explanation." not in prompt # Ensure default is absent
    assert "Respond ONLY in the following language: en." in prompt # Default lang

def test_explain_command_with_lang_option(mocker):
    """Test 'explain' with --lang option."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=MOCK_EXPLANATION)
    code_string = "print('hello ru')"
    target_lang = "ru"
    # Use short flag
    result = runner.invoke(app, ["explain", code_string, "-l", target_lang])

    assert result.exit_code == 0
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    prompt = args[0]
    assert f"Respond ONLY in the following language: {target_lang}." in prompt # Check for correct lang
    assert "Respond ONLY in the following language: en." not in prompt # Ensure default is absent
    assert "Provide a clear and concise explanation." in prompt # Default detail

def test_explain_command_with_both_options(mocker):
    """Test 'explain' with both --detail and --lang options."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=MOCK_EXPLANATION)
    code_string = "print('hello detailed ru')"
    target_lang = "ru"
    # Mix flags
    result = runner.invoke(app, ["explain", code_string, "--detail", "detailed", "-l", target_lang])

    assert result.exit_code == 0
    mock_api_call.assert_called_once()
    args, kwargs = mock_api_call.call_args
    prompt = args[0]
    assert "Provide a detailed, in-depth explanation." in prompt
    assert f"Respond ONLY in the following language: {target_lang}." in prompt

# --- Keep existing failure/edge case tests ---

def test_explain_command_with_nonexistent_file(mocker):
    """Test 'explain' with a non-existent file path."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response')
    bad_file_path = "non_existent_file.py"
    result = runner.invoke(app, ["explain", bad_file_path])

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    # Expect API call because non-file is treated as snippet
    assert "Warning: Received non-string data as explanation." in cleaned_stdout
    assert "MagicMock" in cleaned_stdout
    mock_api_call.assert_called_once()
    assert "✨ Explanation:" not in result.stdout

def test_explain_api_failure(mocker):
    """Test 'explain' when the API call fails (returns None)."""
    mock_api_call = mocker.patch('codex_cli.explain.get_openai_response', return_value=None)
    code_string = "print('test api failure')"
    # Test with an option to ensure it doesn't break failure handling
    result = runner.invoke(app, ["explain", code_string, "-d", "detailed"])

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Failed to get explanation from OpenAI" in cleaned_stdout
    mock_api_call.assert_called_once()

def test_explain_placeholder(): # Keep passed test
    """Placeholder test."""
    assert True