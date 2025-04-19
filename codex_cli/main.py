# codex_cli/main.py

import typer
from rich.console import Console
import os
from pathlib import Path # Import Path for type hinting
from dotenv import load_dotenv

# Import command handlers from respective modules
from . import explain as explain_module
from . import script as script_module
from . import visualize as visualize_module # Added visualize module import
# Future command modules:
# from . import config as config_module

# Load environment variables from .env file at the start
load_dotenv()

# Initialize the main Typer application
app = typer.Typer(
    name="codex-cli-studio",
    help="🧰 A powerful suite of CLI tools powered by OpenAI models.",
    add_completion=False, # Disable shell completion by default
)

# Initialize Rich Console for formatted output
console = Console()

# --- Command Definitions ---

@app.command()
def explain(
    ctx: typer.Context, # Typer context
    input_str: str = typer.Argument(..., help="The code snippet, shell command, or file path to explain."),
    # Options for explain command
    detail: str = typer.Option(
        "basic", "--detail", "-d",
        help="Level of detail for the explanation: 'basic' or 'detailed'.",
        case_sensitive=False,
    ),
    lang: str = typer.Option(
        "en", "--lang", "-l",
        help="Language code for the explanation (e.g., 'en', 'ru', 'es', 'ja').",
        case_sensitive=False,
    )
):
    """
    📖 Explain a piece of code or a shell command using an AI model.
    """
    explain_module.explain_code(input_str, detail, lang)

@app.command()
def script(
    ctx: typer.Context, # Typer context
    task_description: str = typer.Argument(..., help="The task description in natural language."),
    # Option for script type
    output_type: str = typer.Option(
        "bash", "--type", "-t",
        help=f"Output script type. Supported: {', '.join(script_module.SUPPORTED_SCRIPT_TYPES)}.",
        case_sensitive=False
    ),
    # Option for dry run
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Only generate and display the script, do not execute (execution not implemented yet).",
        is_flag=True # Use bool annotation instead in future Typer versions
    )
):
    """
    ⚙️ Generate a script (Bash, Python, etc.) from a natural language description.
    """
    script_module.generate_script(task_description, output_type, dry_run)

# --- NEW COMMAND: visualize ---
@app.command()
def visualize(
    ctx: typer.Context,
    file_path: Path = typer.Argument(
        ..., # Required argument
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True, # Converts to absolute path
        help="Path to the Python file (.py) to visualize."
    ),
    output_file: Path = typer.Option(
        None, # Default is None (auto-filename)
        "--output",
        "-o",
        help="Path to save the output DOT graph file (e.g., graph.gv). Defaults to <input_file_name>.gv.",
        writable=True, # Check if directory is writable
        resolve_path=True, # Converts to absolute path
    )
):
    """
    🧠 Generate a function call graph visualization (as a DOT file) for a Python file.
    """
    # Pass paths as strings to the handler function
    visualize_module.generate_visualization(str(file_path), str(output_file) if output_file else None)

# --- Add other commands here in the future ---
# @app.command()
# def config(...):
#     config_module.handle_config(...)


# --- Application Runner ---

def run():
    """Main entry point for the CLI application."""
    app()

if __name__ == "__main__":
    # Allows the script to be run directly using `python -m codex_cli.main`
    run()