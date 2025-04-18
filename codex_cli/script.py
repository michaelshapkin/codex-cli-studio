# codex_cli/script.py

import os
from rich.console import Console
from rich.syntax import Syntax # For syntax highlighting
from .core.openai_utils import get_openai_response

# Initialize console
console = Console()

# Define supported script types (can be expanded)
SUPPORTED_SCRIPT_TYPES = ["bash", "python", "powershell"]

def generate_script(task_description: str, output_type: str = "bash"):
    """
    Generates a script based on a natural language task description.

    Args:
        task_description: The description of the task for the script.
        output_type: The desired script type (e.g., "bash", "python"). Defaults to "bash".
    """
    # Validate output type
    output_type_lower = output_type.lower()
    if output_type_lower not in SUPPORTED_SCRIPT_TYPES:
        console.print(f"[bold red]Error: Unsupported script type '{output_type}'.[/bold red]")
        console.print(f"Supported types are: {', '.join(SUPPORTED_SCRIPT_TYPES)}")
        return # Exit if type is not supported

    console.print(f"Generating [bold yellow]{output_type_lower}[/bold yellow] script for task: '{task_description}'...")

    # --- Construct the Prompt ---
    # This prompt emphasizes clarity, comments, and safety.
    prompt = f"""
    You are an expert script generator. Your task is to generate a functional and safe script based on the user's request.

    User Request: "{task_description}"

    Desired Script Type: {output_type_lower}

    Instructions:
    1.  Generate a complete, runnable script that performs the requested task.
    2.  Prioritize clarity and readability.
    3.  Add comments to explain key parts of the script, especially complex logic.
    4.  If the task involves potentially destructive actions (e.g., deleting files, modifying system settings), include safety checks (e.g., user confirmation prompts, dry-run options if applicable) or at least warn the user in comments.
    5.  Ensure the script uses standard libraries and commands commonly available on most systems for the specified script type.
    6.  Output ONLY the raw script code, without any introductory text, explanations, or markdown formatting like ```script_type ... ```.

    Begin script:
    """

    # --- Get Script from OpenAI ---
    # Using a potentially more capable model like gpt-4o might be better for script generation
    generated_code = get_openai_response(prompt, model="gpt-4o") # Consider using gpt-4o

    # --- Display the Generated Script ---
    if generated_code and generated_code != "Model returned an empty response.":
        console.print("\n✨ [bold green]Generated Script:[/bold green]")

        # Use Rich's Syntax for highlighting
        # Map common types to lexer names used by Pygments (used by Rich)
        lexer_map = {
            "bash": "bash",
            "python": "python",
            "powershell": "powershell",
            # Add more mappings if needed
        }
        lexer_name = lexer_map.get(output_type_lower, "text") # Default to plain text if unknown

        syntax = Syntax(generated_code, lexer_name, theme="default", line_numbers=True)
        console.print(syntax)

        # Optional: Add a safety warning
        console.print("\n[bold yellow]⚠️ Warning:[/bold yellow] [yellow]Always review generated scripts carefully before executing them, especially if they involve file operations or system changes.[/yellow]")
    else:
        console.print(f"[bold red]Failed to generate the {output_type_lower} script.[/bold red]")
        if generated_code:
             console.print(f"[grey50]Model response: {generated_code}[/grey50]")