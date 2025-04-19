# codex_cli/main.py

import typer
from rich.console import Console
import os
from pathlib import Path # Import Path for type hinting
from typing import Optional # Import Optional for type hinting
from dotenv import load_dotenv

# Import command handlers from respective modules
from . import explain as explain_module
from . import script as script_module
from . import visualize as visualize_module
from . import config as config_module # Import config module

# Load environment variables from .env file at the start
load_dotenv()

# Initialize the main Typer application
app = typer.Typer(
    name="codex-cli-studio",
    help="🧰 A powerful suite of CLI tools powered by OpenAI models.",
    add_completion=False, # Disable shell completion by default
    no_args_is_help=True, # Show help if no command is provided
)

# Initialize Rich Console for formatted output
console = Console()

# --- Explain Command ---
@app.command()
def explain(
    ctx: typer.Context,
    input_str: str = typer.Argument(..., help="The code snippet, shell command, or file path to explain."),
    detail: str = typer.Option("basic", "--detail", "-d", help="Level of detail: 'basic' or 'detailed'.", case_sensitive=False),
    lang: str = typer.Option("en", "--lang", "-l", help="Language code for the explanation (e.g., 'en', 'ru', 'es', 'ja').", case_sensitive=False)
):
    """📖 Explain a piece of code or a shell command using an AI model."""
    explain_module.explain_code(input_str, detail, lang)

# --- Script Command ---
@app.command()
def script(
    ctx: typer.Context,
    task_description: str = typer.Argument(..., help="The task description in natural language."),
    output_type: str = typer.Option("bash", "--type", "-t", help=f"Output script type. Supported: {', '.join(script_module.SUPPORTED_SCRIPT_TYPES)}.", case_sensitive=False),
    dry_run: bool = typer.Option(False, "--dry-run", help="Only generate and display the script.", is_flag=True)
):
    """⚙️ Generate a script (Bash, Python, etc.) from a natural language description."""
    script_module.generate_script(task_description, output_type, dry_run)

# --- Visualize Command ---
@app.command()
def visualize(
    ctx: typer.Context,
    file_path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="Path to the Python file (.py) to visualize."),
    output_file: Path = typer.Option(None, "--output", "-o", help="Path to save the output graph file (e.g., graph.gv, graph.png).", writable=True, resolve_path=True),
    output_format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format (e.g., png, svg, pdf, dot/gv). Requires Graphviz 'dot' command.", case_sensitive=False)
):
    """🧠 Generate a function call graph visualization for a Python file."""
    final_output_path: Optional[str] = str(output_file) if output_file else None
    visualize_module.generate_visualization(str(file_path), output_dot_or_image_file=final_output_path, output_format=output_format)

# --- Config Command Group ---
# Create a separate Typer app for the 'config' subcommand group
config_app = typer.Typer(
    name="config",
    help="🔧 Work with configuration files.",
    no_args_is_help=True # Show help for 'config' if no subcommand is given
)
# Add the 'config' group to the main application
app.add_typer(config_app, name="config")

# Define the 'explain' subcommand within the 'config' group
@config_app.command("explain")
def config_explain(
    ctx: typer.Context,
    file_path: Path = typer.Argument(
        ..., # Required argument
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path to the configuration file to explain."
    ),
):
    """📖 Explain a configuration file using an AI model."""
    config_module.explain_config(file_path)

# --- Placeholder for future 'config' subcommands ---
# @config_app.command("edit")
# def config_edit(...):
#     console.print("Config edit command not implemented yet.")


# --- Application Runner ---
def run():
    """Main entry point for the CLI application."""
    app()

if __name__ == "__main__":
    # Allows the script to be run directly using `python -m codex_cli.main`
    run()