# 🧰 Codex CLI Studio - Development Cheatsheet

Quick reference for common commands used during development.

## ⚙️ Initial Project Setup

1.  **Clone:**
    ```bash
    git clone https://github.com/michaelshapkin/codex-cli-studio.git
    cd codex-cli-studio
    ```
2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate Virtual Environment:**
    *   macOS/Linux: `source venv/bin/activate`
    *   Windows: `venv\Scripts\activate`
4.  **Install Dependencies (using pyproject.toml):**
    ```bash
    pip install -e .[dev]
    # Or if you keep requirements.txt:
    # pip install -r requirements.txt
    # pip install pytest pytest-mock # For tests if not in requirements
    ```
    *(Note: Add `[project.optional-dependencies]` with `dev = ["pytest", "pytest-mock"]` to `pyproject.toml` for `pip install -e .[dev]`)*
5.  **Install Build Tools:**
    ```bash
    pip install --upgrade build twine
    ```
6.  **Install Runtime Dependencies (for visualize):**
    *   macOS: `brew install graphviz`
    *   Debian/Ubuntu: `sudo apt install graphviz`
    *   Windows: [Download from graphviz.org](https://graphviz.org/download/) and add to PATH.
7.  **Setup API Key:**
    *   Create `.env` file in the project root.
    *   Add line: `OPENAI_API_KEY='your_key_here'`
    *   *(Make sure `.env` is in `.gitignore`)*

## 💻 Running & Testing Locally

*   **Run Commands:**
    ```bash
    python -m codex_cli.main --help
    python -m codex_cli.main explain "..." [options]
    python -m codex_cli.main script "..." [options]
    python -m codex_cli.main visualize <file> [options]
    python -m codex_cli.main config explain <file> [options]
    ```
*   **Run All Tests:**
    ```bash
    python -m pytest -v
    ```
*   **Run Specific Test File:**
    ```bash
    python -m pytest -v tests/test_explain.py
    ```
*   **Run Specific Test Function:**
    ```bash
    python -m pytest -v tests/test_script.py::test_script_command_success
    ```

## 📦 Building & Publishing (PyPI)

1.  **Increment Version:** Update `version = "..."` in `pyproject.toml`.
2.  **Clean Old Builds:**
    ```bash
    rm -rf dist/ build/ *.egg-info
    ```
3.  **Build Package:**
    ```bash
    python -m build
    ```
4.  **Upload to TestPyPI (Recommended First):**
    *   Get API token from [TestPyPI](https://test.pypi.org/).
    *   ```bash
        export TWINE_USERNAME=__token__
        export TWINE_PASSWORD='<PASTE_YOUR_TESTPYPI_TOKEN_HERE>'
        twine upload --repository testpypi dist/*
        ```
    *   Test install: `pip install -i https://test.pypi.org/simple/ codex-cli-studio==<new_version>`
5.  **Upload to Real PyPI:**
    *   Get API token from [PyPI](https://pypi.org/).
    *   ```bash
        export TWINE_USERNAME=__token__
        export TWINE_PASSWORD='<PASTE_YOUR_PYPI_TOKEN_HERE>'
        twine upload dist/*
        ```

## ✨ Git Workflow

*   **Check Status:** `git status`
*   **Add Changes:**
    *   Specific files: `git add path/to/file1 path/to/file2`
    *   All tracked modified/new files: `git add .` (Use carefully)
*   **Commit:** `git commit -m "Feat/Fix/Docs/Refactor/Test: Describe changes"`
*   **Push:** `git push origin main`
*   **Amend Last Commit (Fix message or add files):**
    *   `git add <forgotten_files>`
    *   `git commit --amend --no-edit` (Keep message) or `git commit --amend` (Change message)
    *   `git push origin main --force-with-lease` (**Use force push with caution!**)
*   **View Log:** `git log -n 5` (Show last 5 commits)

---

*Remember to keep your `venv` activated during development!*