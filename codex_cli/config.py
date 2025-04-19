# codex_cli/config.py

import os
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path # Use Path for type hinting

# Import the utility for making OpenAI API calls
from .core.openai_utils import get_openai_response

# Initialize console for output
console = Console()

def explain_config(file_path: Path):
    """
    Reads a configuration file and asks an AI model to explain it.

    Args:
        file_path: Path object pointing to the configuration file.
    """
    console.print(f"Analyzing configuration file: [cyan]{file_path}[/cyan]")

    # --- Read File Content ---
    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.strip():
            console.print("[yellow]Warning: The configuration file is empty.[/yellow]")
            # Decide if we should proceed or return
            # Let's proceed for now, the model might still comment on the filename/type
            # return
    except Exception as e:
        console.print(f"[bold red]Error reading file {file_path}: {e}[/bold red]")
        return

    # --- Determine File Type (Simple version based on extension for the prompt) ---
    file_extension = file_path.suffix.lower()
    # Basic type guessing, can be expanded significantly
    if file_extension in ['.yaml', '.yml']:
        config_type = "YAML"
    elif file_extension == '.json':
        config_type = "JSON"
    elif file_extension == '.toml':
        config_type = "TOML"
    elif file_extension == '.ini':
        config_type = "INI"
    elif file_extension == '.conf':
        # Could be Nginx, Apache, or generic. Let's be vague.
        config_type = "CONF-style"
    elif file_extension == '.xml':
        config_type = "XML"
    else:
        config_type = f"'{file_extension}'" # Just use the extension if unknown
    # Note: This doesn't guarantee correctness, just helps the prompt.

    # --- Construct the Prompt ---
    prompt = f"""
    Act as an expert DevOps engineer and system administrator.
    Explain the following configuration file (likely {config_type} format).

    File Path: "{file_path.name}"

    Content:
    ```
    {content}
    ```

    Instructions:
    1.  Identify the primary purpose or technology this configuration file relates to (e.g., Nginx, Docker Compose, Kubernetes, application settings, etc.).
    2.  Explain the overall structure of the file.
    3.  Describe the meaning and purpose of the key sections, directives, or parameters found in the content.
    4.  If possible, mention any potential best practices or common pitfalls related to this type of configuration.
    5.  Respond clearly using Markdown formatting.
    """

    # --- Get Explanation from OpenAI ---
    explanation = get_openai_response(prompt, model="gpt-4o") # Using a capable model

    # --- Display the Explanation ---
    if explanation:
        if isinstance(explanation, str):
            console.print("\n✨ [bold green]Configuration File Explanation:[/bold green]")
            md = Markdown(explanation)
            console.print(md)
        else:
            # Handle unexpected non-string data
            console.print("\n[bold yellow]Warning: Received non-string data as explanation.[/bold yellow]")
            console.print(f"Raw data: {str(explanation)}")
    else:
        # Handle API call failure
        console.print("[bold red]Failed to get explanation from OpenAI.[/bold red]")