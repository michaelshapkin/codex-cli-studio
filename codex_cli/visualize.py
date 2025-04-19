# codex_cli/visualize.py

import ast
import os
import subprocess # For calling 'dot' command
import shutil # For checking if 'dot' exists
from rich.console import Console
import graphviz # type: ignore # graphviz lib might not have type stubs

console = Console()

class CallGraphVisitor(ast.NodeVisitor):
    """
    Visits AST nodes to build a function call graph within a module.
    Stores calls as a dictionary: {caller_function_name: {callee_function_name, ...}}
    """
    def __init__(self):
        self.call_graph: dict[str, set[str]] = {}
        self.current_function: str | None = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit a function definition node."""
        self.current_function = node.name
        self.call_graph.setdefault(self.current_function, set())
        self.generic_visit(node) # Continue descent into function body
        self.current_function = None # Reset context after leaving function

    def visit_Call(self, node: ast.Call):
        """Visit a function call node."""
        if self.current_function: # Only record calls made from within a known function
            callee_name = None
            if isinstance(node.func, ast.Name): # e.g., func()
                callee_name = node.func.id
            elif isinstance(node.func, ast.Attribute): # e.g., obj.method()
                callee_name = node.func.attr # Store method name

            if callee_name:
                # Add the callee to the set for the current caller function
                self.call_graph.setdefault(self.current_function, set()).add(callee_name)
        self.generic_visit(node) # Visit arguments of the call etc.

def generate_call_graph_dot(call_graph: dict[str, set[str]], graph_name: str = "CallGraph") -> graphviz.Digraph:
    """
    Generates a graphviz.Digraph object representing the call graph.

    Args:
        call_graph: Dictionary mapping caller function names to sets of callee names.
        graph_name: Name attribute for the generated graph.

    Returns:
        A graphviz.Digraph object.
    """
    dot = graphviz.Digraph(graph_name, comment='Function Call Graph')
    dot.attr(rankdir='LR') # Layout direction: Left to Right
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica') # Node appearance
    dot.attr('edge', fontname='Helvetica') # Edge appearance

    # Collect all unique function names involved (callers and callees)
    all_nodes = set(call_graph.keys()) | set(c for callees in call_graph.values() for c in callees)

    # Add nodes to the graph
    for func_name in all_nodes:
        dot.node(func_name, label=func_name) # Use function name as node ID and label

    # Add edges (calls) to the graph
    for caller, callees in call_graph.items():
        for callee in callees:
            if callee in all_nodes: # Ensure the callee is a function defined in the scope we analyzed
                dot.edge(caller, callee)

    return dot

def is_tool_available(name: str) -> bool:
    """Check whether `name` command is available in the system's PATH."""
    return shutil.which(name) is not None

def generate_visualization(
    file_path: str,
    output_dot_or_image_file: str | None = None,
    output_format: str | None = None
):
    """
    Parses a Python file, builds a call graph, and saves it as a DOT file
    or renders it to an image format using the Graphviz 'dot' command.

    Args:
        file_path: Path to the Python file (.py) to analyze.
        output_dot_or_image_file: Path to save the output (DOT or image).
                                  If None, name is based on input file.
        output_format: The desired output format (e.g., png, svg, pdf, dot, gv).
                       Format is inferred from output_file extension if not specified,
                       defaulting to 'gv' (DOT).
    """
    # Basic input validation
    if not os.path.isfile(file_path):
        console.print(f"[bold red]Error: File not found at '{file_path}'[/bold red]")
        return
    if not file_path.endswith(".py"):
        console.print(f"[bold red]Error: Input file must be a Python file (.py)[/bold red]")
        return

    console.print(f"Analyzing Python file: [cyan]{file_path}[/cyan]")

    # Determine effective output format and path
    input_filename_base = os.path.splitext(os.path.basename(file_path))[0]
    default_format = "gv"
    effective_format = default_format

    if output_format:
        effective_format = output_format.lower().replace("dot", "gv")
    elif output_dot_or_image_file:
        ext = os.path.splitext(output_dot_or_image_file)[1].lower()
        if ext and ext != ".": # Check if there is an extension
            inferred_format = ext[1:]
            if inferred_format in ["png", "svg", "pdf", "jpg", "jpeg", "gif", "gv", "dot"]:
                 effective_format = inferred_format.replace("dot", "gv")

    # Determine final output file path
    if output_dot_or_image_file is None:
        final_output_path = f"{input_filename_base}.{effective_format}"
    else:
        # Ensure the provided path has the correct extension based on the effective format
        path_base, path_ext = os.path.splitext(output_dot_or_image_file)
        expected_ext = f".{effective_format}"
        if path_ext.lower() != expected_ext:
            final_output_path = path_base + expected_ext
            console.print(f"[yellow]Warning: Output file extension mismatch. Saving as '{final_output_path}' based on format '{effective_format}'.[/yellow]")
        else:
            final_output_path = output_dot_or_image_file

    # --- Parse AST ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f: # Specify encoding
            source_code = f.read()
        tree = ast.parse(source_code, filename=file_path)
    except Exception as e:
        console.print(f"[bold red]Error reading or parsing file: {e}[/bold red]")
        return

    # --- Build Call Graph ---
    visitor = CallGraphVisitor()
    visitor.visit(tree)
    call_graph_data = visitor.call_graph
    if not call_graph_data:
        console.print("[yellow]No function definitions or calls found within the file.[/yellow]")
        return

    # --- Generate Graphviz Object ---
    graph_name = input_filename_base + "_CallGraph"
    dot_object = generate_call_graph_dot(call_graph_data, graph_name=graph_name)

    # --- Output Generation ---
    is_rendering_format = effective_format != "gv"

    try:
        output_dir = os.path.dirname(final_output_path)
        output_filename_base_for_render = os.path.basename(final_output_path)
        output_filename_noext = os.path.splitext(output_filename_base_for_render)[0]

        # Ensure output directory exists
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        if is_rendering_format:
            # Check availability of 'dot' command from Graphviz
            if not is_tool_available("dot"):
                console.print("[bold red]Error: 'dot' command from Graphviz not found.[/bold red]")
                console.print("Please install Graphviz (https://graphviz.org/download/) and ensure 'dot' is in your system's PATH.")
                # Attempt to save the .gv file as a fallback
                gv_fallback_path = os.path.splitext(final_output_path)[0] + ".gv"
                try:
                    dot_object.save(gv_fallback_path)
                    console.print(f"[yellow]Saved DOT source to '{gv_fallback_path}' instead.[/yellow]")
                except Exception as e_save:
                    console.print(f"[bold red]Could not save fallback DOT file: {e_save}[/bold red]")
                return # Exit after fallback attempt

            # Render the image using the 'render' method
            console.print(f"Rendering graph to [bold yellow]{effective_format.upper()}[/bold yellow] format...")
            rendered_path = dot_object.render(
                filename=output_filename_noext, # Pass name without ext
                directory=output_dir if output_dir else ".", # Pass directory or current '.'
                format=effective_format,
                cleanup=True, # Remove intermediate .gv file after rendering
                view=False # Do not open the file automatically
            )
            # render() returns the actual path created
            final_output_path = rendered_path # Update with the actual path

            # --- FIX: Assume success if render didn't raise exception ---
            # No need to check os.path.exists here, trust render() or catch its exception
            console.print(f"\n✨ [bold green]Call graph saved as {effective_format.upper()} to:[/bold green] [cyan]{final_output_path}[/cyan]")

        else: # Save as DOT/GV file
            # Save the DOT source to the specified .gv file
            dot_object.save(final_output_path)
            console.print(f"\n✨ [bold green]Call graph saved in DOT format to:[/bold green] [cyan]{final_output_path}[/cyan]")
            console.print(f"To render manually: dot -Tpng {final_output_path} -o <output.png>")

    except (subprocess.CalledProcessError, FileNotFoundError, Exception) as e:
        # Catch potential errors during rendering or saving
        console.print(f"[bold red]Error during output generation: {e}[/bold red]")
        if isinstance(e, subprocess.CalledProcessError) and e.stderr:
            stderr_output = e.stderr.decode('utf-8', errors='ignore')
            console.print(f"Stderr from dot:\n{stderr_output}")
    # --- END UPDATED BLOCK ---