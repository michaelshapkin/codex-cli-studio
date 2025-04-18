# codex_cli/core/openai_utils.py

import os
from openai import OpenAI, OpenAIError
from rich.console import Console
from dotenv import load_dotenv

# Initialize console for output
console = Console()

# Load environment variables from .env file
# This ensures API keys etc. are available when the module loads
load_dotenv()

def get_openai_client() -> OpenAI | None:
    """
    Initializes and returns the OpenAI client.

    Reads the API key from the OPENAI_API_KEY environment variable.

    Returns:
        An initialized OpenAI client instance or None if initialization fails.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[bold red]Error: OPENAI_API_KEY environment variable not found.[/bold red]")
        return None
    try:
        client = OpenAI(api_key=api_key)
        # Optional: Perform a simple API call to verify connectivity
        # client.models.list()
        return client
    except OpenAIError as e:
        console.print(f"[bold red]Error initializing OpenAI client: {e}[/bold red]")
        return None
    except Exception as e: # Catch any other unexpected initialization errors
        console.print(f"[bold red]An unexpected error occurred during client initialization: {e}[/bold red]")
        return None

def get_openai_response(prompt: str, model: str = "gpt-4o") -> str | None:
    """
    Sends a prompt to the specified OpenAI model and returns the response.

    Args:
        prompt: The prompt string to send to the model.
        model: The OpenAI model identifier (e.g., "gpt-4o").

    Returns:
        The model's response content as a string, or None if an error occurs.
    """
    client = get_openai_client() # Get the client instance
    if not client:
        # Error message already printed by get_openai_client
        return None

    try:
        # Indicate API call start
        console.print(f"[grey50]Sending request to OpenAI model: {model}...[/grey50]", end='\r')
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant expert in explaining code and shell commands clearly and concisely."},
                {"role": "user", "content": prompt}
            ]
        )
        # Clear the "Sending request" message
        console.print(" " * 50, end='\r')
        response = completion.choices[0].message.content
        # Return stripped content or a default message if empty
        return response.strip() if response else "Model returned an empty response."

    except OpenAIError as e:
        console.print(" " * 50, end='\r') # Clear the sending message
        console.print(f"[bold red]Error calling OpenAI API: {e}[/bold red]")
        return None
    except Exception as e: # Catch any other unexpected errors during API call
        console.print(" " * 50, end='\r') # Clear the sending message
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        return None