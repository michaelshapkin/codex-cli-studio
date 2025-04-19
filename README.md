# 🧰 Codex CLI Studio

[![PyPI version](https://badge.fury.io/py/codex-cli-studio.svg)](https://badge.fury.io/py/codex-cli-studio)
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

**Current Modules (v0.1.0):**

*   ✅ `explain`: Explain code, shell commands, or file content. 
*   ✅ `script`: Generate scripts (Bash, Python, PowerShell) from natural language. 
*   ✅ `visualize`: Generate function call graphs for Python files (DOT/Image output).
*   ✅ `config explain`: Explain configuration files. 
*   🛠️ `config edit`: Modify configuration files *(Planned)*.

---

## 🔌 Installation

**Prerequisites:**
*   Python 3.9+
*   `pip`
*   [Graphviz](https://graphviz.org/download/) (specifically the `dot` command) - *Required only for rendering visualizations to image formats (png, svg, etc.) using the `visualize` command.*
*   An OpenAI API Key.

**Install using pip:**

```bash
pip install codex-cli-studio
```

**Set up your OpenAI API Key:**
The tool reads the API key from the OPENAI_API_KEY environment variable. 

You can set it:
* System-wide: Add export OPENAI_API_KEY='your_key_here' to your shell profile (.zshrc, .bashrc, etc.).
* Per session: Run export OPENAI_API_KEY='your_key_here' in your terminal before using cstudio.
* Using a .env file: Create a .env file in the directory where you run the cstudio command and add the line OPENAI_API_KEY='your_key_here'.

---

## ✨ Usage
After installation, use the `cstudio` command:

```bash
# General help
cstudio --help

# Explain a code snippet
cstudio explain 'import sys; print(sys.argv[1])' --lang en

# Explain a file in detail
cstudio explain path/to/your/code.py --detail detailed

# Generate a Python script
cstudio script "read lines from data.txt and print them numbered" -t python

# Generate a bash script (dry run only)
cstudio script "delete all *.tmp files in /tmp" --dry-run

# Visualize a Python file, saving as PNG
cstudio visualize path/to/visualize.py -f png -o visualize_graph.png

# Explain a YAML config file
cstudio config explain path/to/config.yaml
```

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

---

**→ Apply this to real-world workflows. Use AI like magic — right from your terminal.**