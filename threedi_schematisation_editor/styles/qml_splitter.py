import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from style_config import StyleConfig, get_style_configurations


def split_qml_by_category(
    qml_file: Path | str,
    output_dir: Path | str,
    style_configs: List[StyleConfig],
):
    # Convert qml_file and output_dir to Path objects
    qml_file = Path(qml_file)
    output_dir_pth = Path(output_dir)
    # Get the relative path of the input file (without the file extension)
    file_name_without_ext = qml_file.with_suffix("").name  # e.g. "weir"

    # Create a new folder in the output_dir based on the input file's relative path
    output_dir_pth.mkdir(parents=True, exist_ok=True)  # Create the directory, including parents

    # Parse the QML file
    try:
        tree = ET.parse(qml_file)
        root = tree.getroot()
    except ET.ParseError:
        print(f"Parsing failed for {qml_file}")
        return

    # Extract and save each category as a separate QML file
    style_config = style_configs[file_name_without_ext]
    for style_category, relative_path in style_config.styles["default"].items():
        try:
            elements = root.findall(".//" + style_category)
            if elements:
                new_tree = ET.ElementTree(ET.Element("qgis"))
                new_root = new_tree.getroot()

                # Append found elements to new root
                for elem in elements:
                    new_root.append(elem)

                # Save each category as its own QML file
                output_file = output_dir_pth / relative_path  # e.g. "/weir/labeling/default.qml"
                output_file.parent.mkdir(parents=True, exist_ok=True)  # Create the directory, including parents
                new_tree.write(output_file, encoding="utf-8", xml_declaration=True)
                print(f"Saved to {output_file}")
            else:
                # print(f"No elements found for category: {category}")
                pass
        except Exception:
            print(f"Exception while parsing {style_category} in {qml_file}")
            raise


if __name__ == "__main__":
    # Example usage
    styling_dir = Path(r"C:\Users\leendert.vanwolfswin\Documents\migration_checker\style 300\auto-saved from qgis")
    assert styling_dir.exists()

    styling_configs = get_style_configurations()

    output_dir_path = styling_dir.parent / "split"
    for file in styling_dir.rglob("aggregation_settings.qml"):  # Recursively find all QML files
        # for file in styling_dir.rglob('surface_parameters.qml'):  # Find specific qml file
        print(file)
        split_qml_by_category(qml_file=file, output_dir=output_dir_path, style_configs=styling_configs)
