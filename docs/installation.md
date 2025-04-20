# 🔌 Installation

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
