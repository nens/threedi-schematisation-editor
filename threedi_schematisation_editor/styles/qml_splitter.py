import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from style_config import get_style_configurations, StyleConfig


def split_qml(
        qml_file: Path | str,
        output_dir: Path | str,
        tags: List[str] = None
):
    # Convert qml_file and output_dir to Path objects
    qml_file = Path(qml_file)
    output_dir = Path(output_dir)

    # Create a new folder in the output_dir based on the input file's relative path
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory, including parents

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
        new_tree = ET.ElementTree(ET.Element('qgis'))
        new_root = new_tree.getroot()
        new_root.append(elem)
        output_file = output_dir / f"{elem.tag}.qml"
        output_file.parent.mkdir(parents=True, exist_ok=True)  # Create the directory, including parents
        new_tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Saved to {output_file}")


def split_qml_using_style_config(
        qml_file: Path | str,
        output_dir: Path | str,
        style_config: StyleConfig,
):
    # Convert qml_file and output_dir to Path objects
    qml_file = Path(qml_file)
    output_dir = Path(output_dir)

    # Create a new folder in the output_dir based on the input file's relative path
    output_dir.mkdir(parents=True, exist_ok=True)  # Create the directory, including parents

    # Parse the QML file
    try:
        tree = ET.parse(qml_file)
        root = tree.getroot()
    except ET.ParseError:
        print(f"Parsing failed for {qml_file}")
        return

    # Extract and save each category as a separate QML file
    for style_category, relative_path in style_config.styles["default"].items():
        try:
            elements = root.findall(".//" + style_category)
            if elements:
                new_tree = ET.ElementTree(ET.Element('qgis'))
                new_root = new_tree.getroot()

                # Append found elements to new root
                for elem in elements:
                    new_root.append(elem)

                # Save each category as its own QML file
                output_file = output_dir / relative_path  # e.g. "/weir/labeling/default.qml"
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
    # # Example usage
    # stylings_dir = Path(
    #     r"C:\Users\leendert.vanwolfswin\Documents\migration_checker\style 300\auto-saved from qgis"
    # )
    # assert stylings_dir.exists()
    #
    # style_configs = get_style_configurations()
    #
    # output_dir = stylings_dir.parent / "split"
    # for file in stylings_dir.rglob('*.qml'):  # Recursively find all QML files
    # # for file in stylings_dir.rglob('surface_parameters.qml'):  # Find specific qml file
    #     print(file)
    #
    #     # Assumes that layer name == file name
    #     file_name_without_ext = file.with_suffix('').name  # e.g. "weir"
    #     style_config = style_configs[file_name_without_ext]
    #     split_qml_using_style_config(qml_file=file, output_dir=output_dir, style_configs=style_configs)

    base_dir = Path(r"C:\Users\leendert.vanwolfswin\Documents\migration_checker\style 300\stylings rob\new schema")
    # qml_file = base_dir / "channel_exchange type.qml"
    # for qml_file in base_dir.rglob('*.qml'):
    for qml_file in base_dir.rglob('cross section location_cross section LVW.qml'):
        split_qml(
            qml_file=qml_file,
            output_dir=Path(r"C:\Users\leendert.vanwolfswin\Downloads\test2") / qml_file.with_suffix(""),
            # tags=["renderer-v2", "labeling"]
        )
