# Contributing to Codex CLI Studio

First off, thank you for considering contributing! We're excited to build this AI-augmented open-source ecosystem together. Whether it's a bug report, a new feature idea, documentation, or code, your help is valuable.

## How Can I Contribute?

*   **Reporting Bugs:** If you find a bug, please open an issue using the "Bug report" template. Provide as much detail as possible.
*   **Suggesting Enhancements:** Have an idea for a new feature or an improvement? Open an issue using the "Feature request" template or start a discussion in the "Ideas" category.
*   **Discussions:** Join the conversation in our [GitHub Discussions](https://github.com/michaelshapkin/codex-cli-studio/discussions)! Ask questions, share how you use the tool, or brainstorm new possibilities.
*   **Improving Documentation:** Found a typo or think something could be clearer? Feel free to open an issue or a Pull Request.
*   **Writing Code:** If you'd like to contribute code (fix a bug, implement a feature):
    1.  Look for existing issues, especially those tagged `good first issue` or `help wanted`.
    2.  Discuss your plan in the issue or start a new discussion before significant work.
    3.  Follow the development workflow below.

## Development Workflow

1.  **Fork & Clone:** Fork the repository and clone your fork locally.
2.  **Setup:** Follow the installation steps in the [README](installation.md), making sure to install development dependencies (`pip install -e .[dev]` or `pip install pytest pytest-mock`).
3.  **Create Branch:** Create a new branch for your changes (`git checkout -b feature/YourFeature` or `fix/BugDescription`).
4.  **Code:** Make your changes. Follow existing code style.
5.  **Test:** Add tests for your changes and ensure *all* tests pass (`python -m pytest -v`).
6.  **Commit:** Write clear, concise commit messages.
7.  **Push:** Push your branch to your fork (`git push origin feature/YourFeature`).
8.  **Open Pull Request:** Create a PR from your fork's branch to the `main` branch of the original repository. Fill in the PR template, explaining your changes.

## Code Review & AI Assistance

*   **CI Checks:** All Pull Requests will automatically run tests via GitHub Actions. Please ensure these pass.
*   **AI Explain (Experimental):** We may use `cstudio explain` or other AI tools to help understand the proposed code changes and facilitate review.
*   **Maintainer Review:** The project maintainer ([@michaelshapkin](https://github.com/michaelshapkin)) will review the PR conceptually and based on test/AI feedback. We value collaboration and will provide constructive feedback.

## Joining the Team

We're building an open community! Active and helpful contributors may be invited to become core members or maintainers as the project grows. The best way to get involved is to start contributing via issues, discussions, and pull requests.

Let's build the future of AI-assisted development together! 🚀