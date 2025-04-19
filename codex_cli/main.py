# codex_cli/main.py

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
from . import config as config_module

# Load environment variables from .env file
load_dotenv()

# Initialize the main Typer application
app = typer.Typer(
    name="cstudio", # Correct invocation name
    help="""🧰 Codex CLI Studio

    A powerful suite of CLI tools powered by OpenAI models.
    Supercharge productivity, learning, and automation.
    """,
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="markdown",
    # --- FIX: Corrected examples to use 'cstudio' ---
    epilog=("\n---"
            "\n**Examples:**"
            "\n\n  # Explain a Python file in detail"
            "\n  cstudio explain path/to/your/code.py --detail detailed"
            "\n\n  # Generate a bash script to list large files"
            "\n  cstudio script \"find all files larger than 100MB in /data\" --type bash"
            "\n\n  # Visualize function calls in a Python file as SVG"
            "\n  cstudio visualize src/main.py -f svg -o docs/main_calls.svg"
            "\n\n  # Explain a Docker Compose YAML file"
            "\n  cstudio config explain docker-compose.yml"
            "\n\n---"
            # --- FIX: Corrected help text ---
            "\nUse `cstudio [command] --help` for more information."
            )
)

console = Console()

# --- Explain Command ---
@app.command(
    name="explain",
    help="📖 Explain code, shell commands, or file content using AI.",
    # --- FIX: Corrected examples to use 'cstudio' ---
    epilog=("\n---"
            "\n**Examples:**"
            "\n\n  # Explain a code snippet (basic, English)"
            "\n  cstudio explain 'print(\"Hello\")'"
            "\n\n  # Explain a shell command (detailed, Russian)"
            "\n  cstudio explain 'grep -r \"TODO\" ./src' -d detailed -l ru"
            "\n\n  # Explain a file (basic, Spanish)"
            "\n  cstudio explain path/to/script.js --lang es"
            "\n---"
            )
)
def explain(
    ctx: typer.Context,
    input_str: str = typer.Argument(..., help="The code snippet, shell command, or file path to explain."),
    detail: str = typer.Option("basic", "--detail", "-d", help="Level of detail: 'basic' or 'detailed'.", case_sensitive=False),
    lang: str = typer.Option("en", "--lang", "-l", help="Language code for the explanation (e.g., 'en', 'ru', 'es', 'ja').", case_sensitive=False)
):
    """Process the explain command."""
    explain_module.explain_code(input_str, detail, lang)

# --- Script Command ---
@app.command(
    name="script",
    help="⚙️ Generate scripts (Bash, Python, etc.) from descriptions.",
     # --- FIX: Corrected examples to use 'cstudio' ---
    epilog=("\n---"
            "\n**Examples:**"
            "\n\n  # Generate default (bash) script"
            "\n  cstudio script \"list all .py files\""
            "\n\n  # Generate Python script"
            "\n  cstudio script \"read csv data.csv and print first column\" -t python"
            "\n\n  # Generate PowerShell script (dry run)"
            "\n  cstudio script \"get running processes\" --type powershell --dry-run"
            "\n---"
            )
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
    help="🧠 Generate a function call graph for a Python file (DOT/image).",
    # --- FIX: Corrected examples to use 'cstudio' ---
     epilog=("\n---"
             "\n**Examples:**"
             "\n\n  # Generate DOT file (default)"
             "\n  cstudio visualize path/to/module.py -o graph.gv"
             "\n\n  # Generate PNG image directly"
             "\n  cstudio visualize path/to/module.py -f png -o graph.png"
             "\n\n  # Generate SVG image"
             "\n  cstudio visualize path/to/module.py --format svg"
             "\n---"
             "\nRequires Graphviz 'dot' command for image formats."
             )
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
    name="config",
    help="🔧 Work with configuration files.",
    no_args_is_help=True,
    rich_markup_mode="markdown",
)
app.add_typer(config_app, name="config")

# --- Config Explain Subcommand ---
@config_app.command(
    "explain",
    help="📖 Explain a configuration file using an AI model.",
    # --- FIX: Corrected examples to use 'cstudio' ---
    epilog=("\n---"
            "\n**Examples:**"
            "\n\n  # Explain a standard docker-compose file"
            "\n  cstudio config explain docker-compose.yml"
            "\n\n  # Explain an nginx config"
            "\n  cstudio config explain /etc/nginx/nginx.conf"
            "\n\n  # Explain a TOML config"
            "\n  cstudio config explain pyproject.toml"
            "\n---"
            )
)
def config_explain(
    ctx: typer.Context,
    file_path: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="Path to the configuration file to explain."),
):
    """Process the config explain subcommand."""
    config_module.explain_config(file_path)

# --- Application Runner ---
def run():
    """Main entry point for the CLI application."""
    app()

if __name__ == "__main__":
    run()