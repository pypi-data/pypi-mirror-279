"""
A simple documentation generator built using ChatGPT for personal purpose.
"""

import inspect
import importlib.util
import os
import sys


def load_module(module_path):
    """
    Dynamically loads a module from a given file path.

    Args:
        module_path (str): The file path to the module.

    Returns:
        Module: The loaded module.
    """
    module_name = os.path.basename(module_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_markdown_doc(module, class_name):
    """
    Generates Markdown documentation for a specified class within a module with enhanced styling.

    Args:
        module (Module): The module containing the class.
        class_name (str): The name of the class to document.

    Returns:
        str: The generated Markdown documentation with enhanced styling.
    """
    cls = getattr(module, class_name, None)

    if cls is None:
        return "Class not found."

    # Class docstring
    markdown = f"# {class_name}\n\n"
    markdown += f"{inspect.getdoc(cls)}\n\n" if inspect.getdoc(cls) else "_No class docstring._\n\n"

    # Class methods docstring
    markdown += "## Methods\n\n"
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        docstring = inspect.getdoc(method) or "_No method docstring._"
        # Enhance docstring formatting
        enhanced_docstring = enhance_docstring_formatting(docstring)
        markdown += f"### {name}\n\n{enhanced_docstring}\n\n"

    return markdown


def enhance_docstring_formatting(docstring):
    """
    Enhances the formatting of a docstring for Markdown output, specifically
    formatting sections like parameters and returns with bullet points and
    proper spacing.

    Args:
        docstring (str): The original docstring.

    Returns:
        str: The enhanced docstring with Markdown formatting.
    """
    enhanced_lines = []
    lines = docstring.split('\n')
    processing_list_section = False  # Flag to indicate if we're processing a list section

    for line in lines:
        stripped_line = line.strip()

        if stripped_line in ["Parameters:", "Returns:", "Raises:", "Methods:", "Attributes:"]:
            # Start of a new list section
            processing_list_section = True
            enhanced_lines.append(f"\n\n**{stripped_line}**\n")  # Add extra lines before the section header
        elif processing_list_section and stripped_line:
            # We're in a list section and the line is not empty, format it as a list item
            # Assuming parameter lines are indented; adjust the condition if your format differs
            if line.startswith("    "):  # Checks for indentation, adjust if your style differs
                enhanced_lines.append(f"- {line.strip()}")
            else:
                # Line not indented: content directly related to the last list item
                enhanced_lines.append(f"\n{line}")
                processing_list_section = False  # No longer in a list section
        else:
            # Not processing a list section, or an empty line signaling the end of a list section
            enhanced_lines.append(line)

    return '\n'.join(enhanced_lines)


def write_to_file(markdown_doc, output_file):
    """
    Writes the generated Markdown documentation to a file.

    Args:
        markdown_doc (str): The generated Markdown documentation.
        output_file (str): The filename to write to.
    """
    with open(output_file, 'w') as file:
        file.write(markdown_doc)
    print(f"Documentation written to {output_file}")


if __name__ == "__main__":
    # Command-line argument parsing
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Usage: python mkdocs.py <filename> <classname> [-o <output_filename>]")
        sys.exit(1)

    filename = sys.argv[1]
    classname = sys.argv[2]
    output_file = None

    # Check for the -o option for output filename
    if '-o' in sys.argv:
        o_index = sys.argv.index('-o')
        if o_index + 1 < len(sys.argv):
            output_file = sys.argv[o_index + 1]
        else:
            print("Error: No output filename provided after -o option.")
            sys.exit(1)

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    module = load_module(filename)
    markdown_doc = generate_markdown_doc(module, classname)

    # Output to file if requested, otherwise print to standard output
    if output_file:
        write_to_file(markdown_doc, output_file)
    else:
        print(markdown_doc)