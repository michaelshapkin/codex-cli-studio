# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
# Point Sphinx to the project root directory to find the source code
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Codex CLI Studio'
copyright = '2024, Michael Shapkin' # Update year if needed
author = 'Michael Shapkin'
release = '0.1.2' # The full version, including alpha/beta/rc tags

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add extensions here
extensions = [
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.napoleon', # Support Google and NumPy style docstrings
    'sphinx.ext.intersphinx', # Link to other projects' documentation
    'sphinx.ext.viewcode',  # Add links to source code
    'myst_parser',          # Parse Markdown files (.md)
    'sphinx_click',         
]

# Add patterns to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The master toctree document.
# Sphinx 5+ uses root_doc, older versions use master_doc
# Keep master_doc for compatibility if needed, otherwise root_doc is preferred
root_doc = 'index' # Default is 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
#
html_theme = 'furo' # Use the Furo theme

# Add paths for custom static files (css, images, etc.), relative to this directory.
# They are copied after the builtin static files, so file named "default.css"
# will overwrite the builtin "default.css".
# html_static_path = ['_static'] # Uncomment if you have custom static files

# -- Options for autodoc extension -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically document members (methods, attributes)
autodoc_member_order = 'bysource' # Order members by source code line number
# Default flags for automodule/autoclass, etc.
# autodoc_default_options = {
#     'members': True,
#     'undoc-members': True,
#     'private-members': False,
#     'show-inheritance': True,
# }

# -- Options for napoleon extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

# Example configuration for linking to the Python documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    #'typer': ('https://typer.tiangolo.com/en/latest/', None),
    'rich': ('https://rich.readthedocs.io/en/stable/', None),
    #'openai': ('https://platform.openai.com/docs/api-reference', None), # Check if OpenAI has objects.inv
}
intersphinx_timeout = 5 # seconds to wait for remote inventory
intersphinx_cache_limit = 5 # days to cache remote inventories

# -- Options for MyST parser extension ----------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html

# Allow parsing of .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# Optional: Enable specific MyST extensions if needed
# myst_enable_extensions = [
#     "colon_fence", # Allow ```{directive} syntax
#     # "amsmath",
#     # "deflist",
#     # "dollarmath",
#     # "html_admonition",
#     # "html_image",
#     # "linkify",
#     # "replacements",
#     # "smartquotes",
#     # "substitution",
#     # "tasklist",
# ]
# myst_url_schemes = ["http", "https", "mailto"] # Default