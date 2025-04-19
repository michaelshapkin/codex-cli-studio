# tests/test_visualize.py

import pytest
from typer.testing import CliRunner
from pathlib import Path
import os
import graphviz # For mocking methods
import re # For cleaning output

from codex_cli.main import app
from codex_cli import visualize as visualize_module
from codex_cli.core.openai_utils import get_openai_response # Keep if needed elsewhere

runner = CliRunner()

SAMPLE_PYTHON_CODE = """
def func_a():
    print("A")
    func_b()

def func_b():
    len("B") # Built-in call
    func_c(1)

def func_c(x):
    if x > 0:
        func_a() # Recursive/Cyclic call
"""

EXPECTED_DOT_NODE_A = 'func_a [label=func_a]'
EXPECTED_DOT_NODE_B = 'func_b [label=func_b]'
EXPECTED_DOT_NODE_C = 'func_c [label=func_c]'
EXPECTED_DOT_NODE_PRINT = 'print [label=print]'
EXPECTED_DOT_EDGE_AB = 'func_a -> func_b'
EXPECTED_DOT_EDGE_BC = 'func_b -> func_c'
EXPECTED_DOT_EDGE_CA = 'func_c -> func_a'
EXPECTED_DOT_EDGE_AP = 'func_a -> print'

def clean_output(output: str) -> str:
    """Removes ANSI escape codes and normalizes whitespace."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', output)
    return " ".join(cleaned.split()) # Normalize whitespace

# --- Test Suite for 'visualize' command ---

def test_visualize_creates_gv_file(mocker, tmp_path: Path):
    """Test successful generation of a .gv (DOT) file."""
    mock_save = mocker.patch.object(graphviz.Digraph, "save", return_value=None)
    input_file: Path = tmp_path / "test_code.py"
    input_file.write_text(SAMPLE_PYTHON_CODE)
    output_file: Path = tmp_path / "output_graph.gv"
    result = runner.invoke(app, ["visualize", str(input_file), "-o", str(output_file)])

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Call graph saved in DOT format to:" in cleaned_stdout
    # --- FIX: Check only filename in output ---
    assert output_file.name in cleaned_stdout
    mock_save.assert_called_once()

def test_visualize_dot_content(tmp_path: Path):
    """Test the content of the generated DOT file."""
    input_file: Path = tmp_path / "test_code_content.py"
    input_file.write_text(SAMPLE_PYTHON_CODE)
    output_file: Path = tmp_path / "content_test.gv"
    result = runner.invoke(app, ["visualize", str(input_file), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()
    dot_content = output_file.read_text()

    assert EXPECTED_DOT_NODE_A in dot_content
    assert EXPECTED_DOT_NODE_B in dot_content
    assert EXPECTED_DOT_NODE_C in dot_content
    assert EXPECTED_DOT_NODE_PRINT in dot_content
    assert EXPECTED_DOT_EDGE_AB in dot_content
    assert EXPECTED_DOT_EDGE_BC in dot_content
    assert EXPECTED_DOT_EDGE_CA in dot_content
    assert EXPECTED_DOT_EDGE_AP in dot_content



def test_visualize_renders_image(mocker, tmp_path: Path):
    """Test successful rendering of an image format (e.g., png)."""
    output_filename = "render_test.png"
    expected_output_path = tmp_path / output_filename
    # Mock render to return the expected path
    mock_render = mocker.patch.object(graphviz.Digraph, "render", return_value=str(expected_output_path))
    mocker.patch('codex_cli.visualize.is_tool_available', return_value=True)
    input_file: Path = tmp_path / "test_render.py"
    input_file.write_text(SAMPLE_PYTHON_CODE)
    result = runner.invoke(app, ["visualize", str(input_file), "-o", str(expected_output_path), "-f", "png"])

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    # --- FIX: Check only the start of the success message ---
    # The exact path check in stdout is too brittle due to cleaning/wrapping
    assert "Call graph saved as PNG to:" in cleaned_stdout
    # We rely on the mock return value and mock call args checks below

    # Check mock calls
    mock_render.assert_called_once()
    args, kwargs = mock_render.call_args
    assert kwargs.get('filename') == "render_test" # Name without extension
    assert kwargs.get('directory') == str(tmp_path)
    assert kwargs.get('format') == "png"


def test_visualize_render_dot_not_found(mocker, tmp_path: Path):
    """Test rendering fails if 'dot' command is not found."""
    mock_render = mocker.patch.object(graphviz.Digraph, "render")
    mock_is_available = mocker.patch('codex_cli.visualize.is_tool_available', return_value=False)
    mock_save = mocker.patch.object(graphviz.Digraph, "save")
    input_file: Path = tmp_path / "test_dot_fail.py"
    input_file.write_text(SAMPLE_PYTHON_CODE)
    output_file_png: Path = tmp_path / "dot_fail.png"
    output_file_gv: Path = tmp_path / "dot_fail.gv"
    result = runner.invoke(app, ["visualize", str(input_file), "-o", str(output_file_png), "-f", "png"])

    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Error: 'dot' command from Graphviz not found." in cleaned_stdout
    assert "Saved DOT source to" in cleaned_stdout
    # --- FIX: Check only filename in output ---
    assert output_file_gv.name in cleaned_stdout
    assert "instead." in cleaned_stdout
    mock_is_available.assert_called_once_with("dot")
    mock_render.assert_not_called()
    mock_save.assert_called_once_with(str(output_file_gv))

def test_visualize_file_not_found():
    """Test command exits if input file doesn't exist."""
    result = runner.invoke(app, ["visualize", "nonexistent/file.py"])
    assert result.exit_code != 0
    assert "Invalid value for 'FILE_PATH'" in result.stdout
    assert "'nonexistent/file.py' does not exist" in result.stdout

def test_visualize_not_python_file(tmp_path: Path):
    """Test command exits if input file is not a .py file."""
    input_file: Path = tmp_path / "test_not_py.txt"
    input_file.write_text("print('hello')")
    result = runner.invoke(app, ["visualize", str(input_file)])
    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Error: Input file must be a Python file (.py)" in cleaned_stdout

def test_visualize_syntax_error(tmp_path: Path):
    """Test command handles Python syntax errors gracefully."""
    input_file: Path = tmp_path / "test_syntax_error.py"
    input_file.write_text("def func_a():\n  print('A'\n") # Missing closing parenthesis
    result = runner.invoke(app, ["visualize", str(input_file)])
    assert result.exit_code == 0
    cleaned_stdout = clean_output(result.stdout)
    assert "Error reading or parsing file" in cleaned_stdout
    # --- FIX: Check for part of the actual error message from AST ---
    assert "was never closed" in cleaned_stdout # Part of the specific syntax error