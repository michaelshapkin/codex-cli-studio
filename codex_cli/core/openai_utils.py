# codex_cli/core/openai_utils.py

import os
from openai import OpenAI, OpenAIError # Импортируем обработку ошибок
from rich.console import Console

console = Console()

# Инициализируем клиента OpenAI
# Ключ API будет автоматически подхвачен из переменной окружения OPENAI_API_KEY
try:
    client = OpenAI()
except OpenAIError as e:
    console.print(f"[bold red]Error initializing OpenAI client: {e}[/bold red]")
    console.print("Please make sure your OPENAI_API_KEY is set correctly in the .env file.")
    client = None # Устанавливаем в None, чтобы проверить позже

def get_openai_response(prompt: str, model: str = "gpt-4o") -> str | None:
    """
    Sends a prompt to the specified OpenAI model and returns the response.

    Args:
        prompt: The prompt to send to the model.
        model: The model to use (default: "gpt-4o").

    Returns:
        The model's response as a string, or None if an error occurs or client is not initialized.
    """
    if not client:
        console.print("[bold red]OpenAI client is not initialized. Cannot make API calls.[/bold red]")
        return None

    try:
        console.print(f"[grey50]Sending request to OpenAI model: {model}...[/grey50]", end='\r')
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant expert in explaining code and shell commands clearly and concisely."},
                {"role": "user", "content": prompt}
            ]
        )
        console.print(" " * 50, end='\r') # Clear the sending message
        response = completion.choices[0].message.content
        return response.strip() if response else "Model returned an empty response."

    except OpenAIError as e:
        console.print(" " * 50, end='\r') # Clear the sending message
        console.print(f"[bold red]Error calling OpenAI API: {e}[/bold red]")
        return None
    except Exception as e:
        console.print(" " * 50, end='\r') # Clear the sending message
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
        return None