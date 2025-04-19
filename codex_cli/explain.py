# codex_cli/explain.py

import os
from rich.console import Console
from rich.markdown import Markdown
from .core.openai_utils import get_openai_response

console = Console()

# --- UPDATED SIGNATURE: Added detail and lang ---
def explain_code(input_str: str, detail: str = "basic", lang: str = "en"):
    """Explains a code snippet, shell command, or the content of a file."""
    content_to_explain = ""
    is_file = False
    read_error = False

    if os.path.isfile(input_str):
        is_file = True
        try:
            with open(input_str, 'r') as f:
                content_to_explain = f.read()
            console.print(f"Explaining content from file: {input_str}")
        except Exception as e:
            console.print(f"[bold red]Error reading file {input_str}: {e}[/bold red]")
            read_error = True
            return
    else:
        content_to_explain = input_str

    if read_error: return # Exit if reading failed
    if not content_to_explain:
        console.print("[bold red]Cannot explain empty content.[/bold red]")
        return

    # --- UPDATED PROMPT CONSTRUCTION ---
    prompt_type = "content from a file" if is_file else "code snippet or shell command"
    # Determine detail level instruction based on the option
    detail_instruction = "Provide a detailed, in-depth explanation." if detail.lower() == "detailed" else "Provide a clear and concise explanation."
    # Specify the desired language
    language_instruction = f"Respond ONLY in the following language: {lang}."

    prompt = f"""
    Your task is to explain the following {prompt_type}.
    {detail_instruction}
    Explain its purpose and key parts. Use Markdown for formatting.
    Make sure your entire response is {language_instruction}

    ```
    {content_to_explain}
    ```
    """
    # --- END UPDATED PROMPT ---

    explanation = get_openai_response(prompt)

    if explanation:
        if isinstance(explanation, str):
            console.print("\n✨ [bold green]Explanation:[/bold green]")
            md = Markdown(explanation)
            console.print(md)
        else:
            console.print("\n[bold yellow]Warning: Received non-string data as explanation.[/bold yellow]")
            console.print(f"Raw data: {str(explanation)}")
    else:
        console.print("[bold red]Failed to get explanation from OpenAI.[/bold red]")