import typer
from rich.console import Console
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Import command handlers
from . import explain as explain_module
from . import script as script_module
from . import visualize as visualize_module
from . import config as config_module # Make sure this is imported

# Load environment variables from .env file
load_dotenv()

# Initialize the main Typer application
app = typer.Typer(
    name="codex", # Shorter invocation name
    help="""🧰 Codex CLI Studio

    A powerful suite of CLI tools powered by OpenAI models.
    Supercharge productivity, learning, and automation.
    """,
    add_completion=False, # Disable shell completion for simplicity
    no_args_is_help=True, # Show help if no command is provided
    rich_markup_mode="markdown", # Enable markdown in help/epilog
    epilog="""

---
**Examples:**

```bash
# Explain a Python file in detail
codex explain path/to/your/code.py --detail detailed

# Generate a bash script to list large files
codex script "find all files larger than 100MB in /data" --type bash

# Visualize function calls in a Python file as SVG
codex visualize src/main.py -f svg -o docs/main_calls.svg

# Explain a Docker Compose YAML file
codex config explain docker-compose.yml

# Use codex [command] --help for more information on a specific command.

"""
)


# Initialize Rich Console for formatted output
console = Console()

# --- Explain Command ---
# --- Explain Command ---
@app.command(
    name="explain", # Explicit command name
    help="📖 Explain code, shell commands, or file content using AI.", # Short help
    epilog="""

---
**Examples:**

```bash
# Explain a code snippet (basic, English)
codex explain 'print("Hello")'

# Explain a shell command (detailed, Russian)
codex explain 'grep -r "TODO" ./src' -d detailed -l ru

# Explain a file (basic, Spanish)
codex explain path/to/script.js --lang es
"""
)
def explain(
    ctx: typer.Context,
    input_str: str = typer.Argument(..., help="The code snippet, shell command, or file path to explain."),
    detail: str = typer.Option("basic", "--detail", "-d", help="Level of detail: 'basic' or 'detailed'.", case_sensitive=False),
    lang: str = typer.Option("en", "--lang", "-l", help="Language code for the explanation (e.g., 'en', 'ru', 'es', 'ja').", case_sensitive=False)
):
    """📖 Explain a piece of code or a shell command using an AI model."""
    explain_module.explain_code(input_str, detail, lang)



# --- Script Command ---
@app.command(
    name="script",
    help="⚙️ Generate a script (Bash, Python, etc.) from a natural language description.",
    epilog="""

---
**Examples:**

```bash
# Generate default (bash) script
codex script "list all .py files"

# Generate Python script
codex script "read csv data.csv and print first column" -t python

# Generate PowerShell script (dry run)
codex script "get running processes" --type powershell --dry-run

"""
)

def script(
    ctx: typer.Context,
    task_description: str = typer.Argument(..., help="The task description in natural language."),
    output_type: str = typer.Option("bash", "--type", "-t", help=f"Output script type. Supported: {', '.join(script_module.SUPPORTED_SCRIPT_TYPES)}.", case_sensitive=False),
    dry_run: bool = typer.Option(False, "--dry-run", help="Only generate and display the script.", is_flag=True)
):
    """Process the script command."""
    script_module.generate_script(task_description, output_type, dry_run)



# --- Visualize Command ---
@app.command(
    name="visualize",
    help="🧠 Generate a function call graph visualization for a Python file.",
     epilog="""

---
**Examples:**

```bash
# Generate DOT file (default)
codex visualize path/to/module.py -o graph.gv

# Generate PNG image directly
codex visualize path/to/module.py -f png -o graph.png

# Generate SVG image
codex visualize path/to/module.py --format svg
"""
)
def visualize(
    ctx: typer.Context,
    file_path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="Path to the Python file (.py) to visualize."),
    output_file: Path = typer.Option(None, "--output", "-o", help="Path to save the output graph file (e.g., graph.gv, graph.png).", writable=True, resolve_path=True),
    output_format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format (e.g., png, svg, pdf, dot/gv).", case_sensitive=False)
):
    """Process the visualize command."""
    final_output_path: Optional[str] = str(output_file) if output_file else None
    visualize_module.generate_visualization(str(file_path), output_dot_or_image_file=final_output_path, output_format=output_format)


# --- Config Command Group ---
config_app = typer.Typer(
    name="config", # Subcommand group name
    help="🔧 Work with configuration files.",
    no_args_is_help=True, # Show help for 'config' if no subcommand is given
    rich_markup_mode="markdown" # Enable markdown for this group's help/epilogs
)
# Register the subcommand group with the main app
app.add_typer(config_app, name="config")

# --- Config Explain Subcommand ---
@config_app.command(
    "explain", # Name of the subcommand within the 'config' group
    help="📖 Explain a configuration file using an AI model.",
    epilog="""

---
**Examples:**

```bash
# Explain a standard docker-compose file
codex config explain docker-compose.yml

# Explain an nginx config
codex config explain /etc/nginx/nginx.conf

# Explain a TOML config
codex config explain pyproject.toml
"""
)

def config_explain(
    ctx: typer.Context,
    file_path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="Path to the configuration file to explain."),
):
    """Process the config explain subcommand."""
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