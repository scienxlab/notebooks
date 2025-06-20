import sys
import nbformat
import yaml

def extract_yaml_metadata(nb):
    """Extract YAML block from the first raw cell, if present."""
    if not nb.cells:
        return None

    first_cell = nb.cells[0]
    if first_cell.cell_type != "raw":
        return None

    src = first_cell.source.strip()
    if not (src.startswith('---') and src.count('---') >= 2):
        return None

    try:
        yaml_block = src.split('---', 2)[1]
        return yaml.safe_load(yaml_block)
    except Exception as e:
        print(f"Error parsing YAML metadata: {e}")
        return None

def update_notebook_metadata(nb_path):
    nb = nbformat.read(nb_path, as_version=4)
    metadata_from_yaml = extract_yaml_metadata(nb)

    if metadata_from_yaml:
        # Update notebook-level metadata with parsed YAML
        nb.metadata.update(metadata_from_yaml)
        nbformat.write(nb, nb_path)
        print(f"Updated metadata in: {nb_path}")
    else:
        print(f"No valid YAML metadata block found in: {nb_path}")

if __name__ == "__main__":
    for path in sys.argv[1:]:
        if path.endswith(".ipynb"):
            update_notebook_metadata(path)

