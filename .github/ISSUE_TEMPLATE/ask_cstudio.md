---
name: 🤖 Ask cstudio explain
about: Request an explanation for a code snippet or config using our AI Action
title: "Explain: [Brief description of what to explain]"
labels: ask-cstudio-explain # This label triggers the GitHub Action!
assignees: ''

---

**Please provide the code or configuration snippet you want explained below.**

Make sure to enclose your code/config within a fenced code block (using three backticks ```).

**Example for Python:**
```text
```python
# Paste your Python code here
import os
print(os.getcwd())
```

**Example for YAML:**
```text
```yaml
# Paste your YAML here
service: my-app
port: 80
```


**Example for Shell:**
```text
```bash
# Paste your shell command here
grep -r "ERROR" /var/log/*.log | sort | uniq -c
```


**(Delete the examples above and paste your actual code/config inside a new fenced code block below)**

--- PASTE YOUR CODE/CONFIG BLOCK BELOW ---


--- END CODE/CONFIG BLOCK ---

**Optional: Any specific questions?**
Is there anything specific you'd like the explanation to focus on? (e.g., "What does the `-r` flag do?", "Is this YAML valid?")

*(Please note: The AI will explain the **first** code block found in this issue description after you add the `ask-cstudio-explain` label.)*