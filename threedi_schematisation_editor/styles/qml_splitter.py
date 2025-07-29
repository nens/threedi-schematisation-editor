import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List


def split_qml(qml_file: Path | str, output_dir: Path | str, tags: List[str] = None):
    # Convert qml_file and output_dir to Path objects
    qml_file = Path(qml_file)
    output_dir = Path(output_dir)

    # Create a new folder in the output_dir based on the input file's relative path
    output_dir.mkdir(
        parents=True, exist_ok=True
    )  # Create the directory, including parents

    # Parse the QML file
    try:
        tree = ET.parse(qml_file)
        root = tree.getroot()
    except ET.ParseError:
        print(f"Parsing failed for {qml_file}")
        return

    # Extract and save each category as a separate QML file
    for elem in root:
        if tags:
            if elem.tag not in tags:
                continue
        new_tree = ET.ElementTree(ET.Element("qgis"))
        new_root = new_tree.getroot()
        new_root.append(elem)
        output_file = output_dir / f"{elem.tag}.qml"
        output_file.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create the directory, including parents
        new_tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Saved to {output_file}")


if __name__ == "__main__":
    # Example usage
    base_dir = Path(r"path\to\directory\with\qml\files")
    output_base_dir = Path(r"path\to\directory\to\store\output\qml\files")
    for qml_file in base_dir.rglob("*.qml"):
        split_qml(
            qml_file=qml_file, output_dir=output_base_dir / qml_file.with_suffix("")
        )
