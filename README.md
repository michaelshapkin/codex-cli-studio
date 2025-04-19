# 🧰 Codex CLI Studio

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A powerful suite of command-line tools powered by OpenAI models, built to supercharge productivity, learning, and automation for developers, DevOps, and students alike.

---

## 👀 Demo

See `Codex CLI Studio` in action! This animation shows basic usage of the `explain`, `script`, and `visualize` commands.

![Codex CLI Studio Demo](codex-cli-studio-demo.svg)
*(Generated using asciinema and termtosvg)*

---


## 🚀 Overview & Status
Codex CLI Studio is a modular set of CLI tools leveraging OpenAI's API.

**Current Modules:**

*   ✅ `explain`: Explain code, shell commands, or file content. *(Implemented)*
*   ✅ `script`: Generate scripts (Bash, Python, PowerShell) from natural language. *(Implemented)*
*   ✅ `visualize`: Generate function call graphs for Python files (DOT/Image output). *(Implemented)*
*   ✅ `config explain`: Explain configuration files. *(Implemented)*
*   🛠️ `config edit`: Modify configuration files (Planned).

---

## 🔌 Installation (from source)

Currently, installation is available directly from the source code. Publishing to PyPI (`pip install codex-cli-studio`) is planned.

**Prerequisites:**
*   Python 3.9+
*   `pip` and `venv` (recommended)
*   [Graphviz](https://graphviz.org/download/) (specifically the `dot` command) - *Required only for rendering visualizations to image formats (png, svg, etc.) within the `visualize` command.*


**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/michaelshapkin/codex-cli-studio.git
    cd codex-cli-studio
    ```
2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your OpenAI API Key:**
    *   Create a file named `.env` in the project root (`codex-cli-studio/`).
    *   Add your API key to the `.env` file:
        ```
        OPENAI_API_KEY='your_openai_api_key_here'
        ```
    *   *(This file is already in `.gitignore` and should NOT be committed.)*

---

## ✨ Usage

Once installed from source and with the virtual environment activated, run commands using `python -m codex_cli.main` followed by the command name and arguments:

```bash
# General help
python -m codex_cli.main --help

# Explain a code snippet
python -m codex_cli.main explain 'import sys; print(sys.argv[1])' --lang en

# Explain a file in detail
python -m codex_cli.main explain ./codex_cli/main.py --detail detailed

# Generate a Python script
python -m codex_cli.main script "read lines from data.txt and print them numbered" -t python

# Generate a bash script (dry run only)
python -m codex_cli.main script "delete all *.tmp files in /tmp" --dry-run

# Visualize a Python file, saving as PNG
python -m codex_cli.main visualize ./codex_cli/visualize.py -f png -o visualize_graph.png

# Explain a YAML config file
python -m codex_cli.main config explain examples/test.yaml
```

*(Note: The invocation name might change to just `codex` after publishing to PyPI).*

*(Note: The invocation name might change to just `codex` after publishing to PyPI).*

---

## 🛠️ Module Details

### `explain` ✅
Explains code snippets, shell commands, or file content.
*   Supports various languages (auto-detected by AI).
*   Options: `--detail basic|detailed`, `--lang <language_code>`.

### `script` ✅
Generates executable scripts from natural language tasks.
*   Supports: Bash, Python, PowerShell.
*   Options: `--type <bash|python|powershell>`, `--dry-run` (only displays script).

### `visualize` ✅
Generates function call graphs for Python files.
*   Input: Python file (`.py`).
*   Output: Graphviz DOT (`.gv`, `.dot`) or rendered image (`.png`, `.svg`, `.pdf`, etc.).
*   Requires Graphviz (`dot` command) for image rendering.
*   Options: `--output <path>`, `--format <format>`.

### `config explain` ✅
Explains various configuration files (YAML, INI, Dockerfile, etc.).
*   Input: Path to configuration file.

### `config edit` 🛠️ *(Planned)*
Modify configuration files using natural language instructions.

---

## 🌍 Why It Matters
*   ✅ **Educational:** Quickly understand unfamiliar code, commands, or configs.
*   ⚡ **Productive:** Automate script generation and explanations, reducing boilerplate and search time.
*   🔧 **Extensible:** Modular design allows for adding new commands and capabilities.
*   🌱 **Open Source:** Community contributions are welcome!

---

## 📦 Built With
*   Python 3.9+
*   OpenAI API (gpt-4o or other models)
*   [Typer](https://typer.tiangolo.com/) - for building the CLI interface.
*   [Rich](https://rich.readthedocs.io/en/latest/) - for beautiful terminal output.
*   [python-dotenv](https://pypi.org/project/python-dotenv/) - for managing environment variables.
*   [Graphviz (Python library)](https://graphviz.readthedocs.io/en/stable/) - for generating DOT graph descriptions.
*   Standard Python libraries (`ast`, `subprocess`, `shutil`, etc.)

---
## 🔮 Roadmap / Coming Soon
*   **Testing:** Increase test coverage, especially for edge cases and options.
*   **Error Handling:** Improve robustness and user feedback on errors.
*   **`config edit`:** Implement the configuration editing functionality.
*   **`visualize` Enhancements:** Options to exclude nodes (builtins), different layouts.
*   **More Modules?** `test` generation, `translate` code? (Open to ideas!)
*   **Configuration:** Centralized config file (e.g., `~/.config/codex-cli-studio/config.toml`).
*   **PyPI Release:** Package and publish for easy `pip install`.
*   **IDE Integration:** VS Code plugin?

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/michaelshapkin/codex-cli-studio/issues).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` file for more information.
*(You should add a LICENSE file to the repository)*

---

**→ Apply this to real-world workflows. Use AI like magic — right from your terminal.**