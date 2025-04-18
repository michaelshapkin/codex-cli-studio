# codex_cli/main.py

import typer
from rich.console import Console
import os
from dotenv import load_dotenv

# Import placeholder functions from modules
from . import explain as explain_module
from . import script as script_module
# Future imports:
# from . import visualize as visualize_module
# from . import config as config_module

# Load environment variables from .env file (e.g., API key)
# Needs to be done before accessing os.getenv('OPENAI_API_KEY')
load_dotenv()

# Initialize the Typer application
app = typer.Typer(
    name="codex-cli-studio",
    help="🧰 A powerful suite of CLI tools powered by OpenAI Codex.",
    add_completion=False, # Disable shell completion by default for simplicity
)

# Initialize Rich Console for pretty printing
console = Console()

# --- Command Registration ---

@app.command()
def explain(
    ctx: typer.Context, # Typer context, useful for passing global options
    input_str: str = typer.Argument(..., help="The code snippet, shell command, or file path to explain."),
    # Options can be added later:
    # detail: str = typer.Option("basic", "--detail", "-d", help="Level of detail: 'basic' or 'detailed'."),
    # lang: str = typer.Option("en", "--lang", "-l", help="Language for the explanation (e.g., 'en', 'ru').")
):
    """
    📖 Explain a piece of code or a shell command.
    """
    console.print(f"Executing Explain command for: [bold cyan]{input_str}[/bold cyan]")
    # Placeholder for the actual logic call
    # result = explain_module.explain_code(input_str, detail, lang)
    # console.print(result)
    explain_module.explain_code(input_str)

@app.command()
def script(
    ctx: typer.Context,
    task_description: str = typer.Argument(..., help="The task description in natural language."),
    # Options can be added later:
    # output_type: str = typer.Option("bash", "--type", "-t", help="Output script type: 'bash', 'python', 'powershell'."),
    # dry_run: bool = typer.Option(False, "--dry-run", help="Only show the generated script, don't execute."),
):
    """
    ⚙️ Generate a script (Bash, Python, etc.) from a description.
    """
    # console.print(f"Executing Script command for task: [bold magenta]{task_description}[/bold magenta]")
    # Placeholder for the actual logic call
    # result = script_module.generate_script(task_description, output_type)
    # console.print(result)
    # if not dry_run:
    #     # (Caution!) Potentially execute the script
    #     pass
    script_module.generate_script(task_description, output_type)

# --- Application Entry Point ---

def run():
    """Entry point for package installation (e.g., via Poetry/pip)."""
    app()

if __name__ == "__main__":
    # Allows running the script directly via python codex_cli/main.py
    run()