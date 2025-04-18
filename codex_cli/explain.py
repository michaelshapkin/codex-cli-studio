# codex_cli/explain.py

import os
from rich.console import Console
from rich.markdown import Markdown
from .core.openai_utils import get_openai_response # Импортируем нашу функцию

console = Console()

def explain_code(input_str: str):
    """
    Explains a code snippet, shell command, or the content of a file.

    Args:
        input_str: The code/command string or a file path.
    """
    content_to_explain = ""
    input_type = "text" # Default type

    # Check if input_str is a file path
    if os.path.isfile(input_str):
        try:
            with open(input_str, 'r') as f:
                content_to_explain = f.read()
            input_type = "file"
            console.print(f"Explaining content from file: [cyan]{input_str}[/cyan]")
        except Exception as e:
            console.print(f"[bold red]Error reading file {input_str}: {e}[/bold red]")
            return # Exit if file reading fails
    else:
        # Assume it's a code snippet or command string
        content_to_explain = input_str
        console.print("Explaining provided text snippet.")

    if not content_to_explain:
        console.print("[bold red]No content provided to explain.[/bold red]")
        return

    # --- Construct the Prompt ---
    # You can refine this prompt for better results
    prompt = f"""
    Please explain the following {'code snippet' if input_type == 'text' else 'content from a file'} or shell command.
    Be clear, concise, and explain its purpose and key parts. Use Markdown for formatting.

    ```
    {content_to_explain}
    ```
    """

    # --- Get Explanation from OpenAI ---
    explanation = get_openai_response(prompt)

    # --- Display the Explanation ---
    if explanation:
        console.print("\n✨ [bold green]Explanation:[/bold green]")
        # Use Rich's Markdown renderer for nice formatting
        md = Markdown(explanation)
        console.print(md)
    else:
        console.print("[bold red]Failed to get explanation from OpenAI.[/bold red]")