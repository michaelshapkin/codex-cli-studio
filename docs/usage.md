# ✨ Usage
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

