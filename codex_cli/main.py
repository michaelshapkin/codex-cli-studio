# codex_cli/main.py

import typer
from rich.console import Console
import os
from dotenv import load_dotenv

# Import command handlers from respective modules
from . import explain as explain_module
from . import script as script_module
# Future command modules:
# from . import visualize as visualize_module
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
    
    detail: str = typer.Option(
        "basic", # Default value if option not provided
        "--detail",
        "-d",
        help="Level of detail for the explanation: 'basic' or 'detailed'.",
        case_sensitive=False, # Allow 'Basic', 'Detailed', etc.
    ),
    lang: str = typer.Option(
        "en", # Default language code
        "--lang",
        "-l",
        help="Language code for the explanation (e.g., 'en', 'ru', 'es', 'ja').",
        case_sensitive=False, # Allow 'EN', 'ru', etc.
    )
    
):
    """
    📖 Explain a piece of code or a shell command using an AI model.
    """
    # --- UPDATED CALL: Pass options to the handler ---
    explain_module.explain_code(input_str, detail, lang)



@app.command()
def script(
    ctx: typer.Context, # Typer context
    task_description: str = typer.Argument(..., help="The task description in natural language."),
    # Option to specify the desired script type
    output_type: str = typer.Option(
        "bash", # Default script type
        "--type",
        "-t",
        # Help text dynamically lists supported types from the script module
        help=f"Output script type. Supported: {', '.join(script_module.SUPPORTED_SCRIPT_TYPES)}.",
        case_sensitive=False # Allow case-insensitive input like 'Python', 'bash'
        ),
    # --- Future options ---
    # dry_run: bool = typer.Option(False, "--dry-run", help="Only show the generated script, don't execute."),
):
    """
    ⚙️ Generate a script (Bash, Python, etc.) from a natural language description.
    """
    # Call the script generation handler, passing the task and desired type
    script_module.generate_script(task_description, output_type)

# --- Add other commands here in the future ---
# @app.command()
# def visualize(...):
#     visualize_module.generate_visualization(...)

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