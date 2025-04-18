# codex_cli/explain.py

import os
from rich.console import Console
from rich.markdown import Markdown
from .core.openai_utils import get_openai_response

console = Console()

def explain_code(input_str: str):
    """Explains a code snippet, shell command, or the content of a file."""
    content_to_explain = ""
    is_file = False
    read_error = False # Flag to track if file reading failed

    if os.path.isfile(input_str):
        is_file = True
        try:
            with open(input_str, 'r') as f:
                content_to_explain = f.read()
            # --- FIX: Print the message without [cyan] for easier testing ---
            console.print(f"Explaining content from file: {input_str}")
        except Exception as e:
            console.print(f"[bold red]Error reading file {input_str}: {e}[/bold red]")
            read_error = True # Set flag on read error
            # We might still want to return here, or let it proceed to check content_to_explain
            return # Let's return here for clarity
    else:
        # Treat as snippet/command
        content_to_explain = input_str

    # Exit if reading failed (already handled by return above, but defensive)
    if read_error:
        return

    # Exit if content is empty (e.g., empty file provided)
    if not content_to_explain:
        console.print("[bold red]Cannot explain empty content.[/bold red]")
        return

    # --- Optional: Add logic here later to *not* call API for simple non-existent paths ---
    # if not is_file and looks_like_just_a_bad_path(input_str):
    #     console.print(f"[yellow]Input '{input_str}' does not appear to be a valid file or code snippet.[/yellow]")
    #     return

    # Construct the prompt
    prompt_type = "content from a file" if is_file else "code snippet or shell command"
    prompt = f"""
    Please explain the following {prompt_type}.
    Be clear, concise, and explain its purpose and key parts. Use Markdown for formatting.

    ```
    {content_to_explain}
    ```
    """

    explanation = get_openai_response(prompt)

    # --- Display the Explanation ---
    if explanation:
        # --- FIX: Move title inside the type check ---
        if isinstance(explanation, str):
            console.print("\n✨ [bold green]Explanation:[/bold green]") # Moved title here
            md = Markdown(explanation)
            console.print(md)
        else:
            # Handle unexpected non-string explanation (e.g., MagicMock in tests)
            console.print("\n[bold yellow]Warning: Received non-string data as explanation.[/bold yellow]")
            console.print(f"Raw data: {str(explanation)}") # Print raw representation
    else:
        # Failed to get explanation from API (returned None or empty)
        console.print("[bold red]Failed to get explanation from OpenAI.[/bold red]")