from qgis.utils import qgsfunction
import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en


CROSS_SECTION_MAX_WIDTH_HELPTEXT = """
    <p>Get maximum width of the cross-section.</p>
    <br>
    <p>Features must have the fields <i>cross_section_shape</i>, <i>cross_section_width</i>, and
    <i>cross_section_table</i>.</p>
    <br>
    <p>The value returned depends on <i>cross_section_shape</i>:
    <ul>
        <li>
            <i>cross_section_width</i> for <i>"Open rectangle"</i>, <i>"Closed rectangle"</i>, <i>"Circle"</i>,
            <i>"Egg"</i> and "Inverted egg"</i>
        </li>
        <li>
            the maximum width value in <i>cross_section_table</i> for "Tabulated trapezium" and "Tabulated rectangle"
        </li>
        <li>
            the maximum Y value in the <i>cross_section_table</i> for "YZ"
        </li>
    </ul>
"""
CROSS_SECTION_MAX_HEIGHT_HELPTEXT = """
    <p>Get maximum height of the cross-section.</p>
    <br>
    <p>Features must have the fields <i>cross_section_shape</i>, <i>cross_section_height</i>, and
    <i>cross_section_table</i>.</p>
    <br>
    <p>The value returned depends on <i>cross_section_shape</i>:
    <ul>
        <li><i>None</i> for "Open rectangle"</li>
        <li><i>cross_section_height</i> for "Closed rectangle"</li>
        <li><i>cross_section_width</i> for "Circle"</li>
        <li>1.5 * <i>cross_section_width</i> for "Egg" and "Inverted egg"</li>
        <li>the maximum height value in <i>cross_section_table</i> for "Tabulated trapezium" and "Tabulated rectangle"</li>
        <li>the maximum Z value in the <i>cross_section_table</i> for "YZ"</li>
    </ul>
"""

CROSS_SECTION_LABEL_HELPTEXT = """
    <p>Create a label describing the cross-section</p>
    <br>
    <p>
        Features must have the fields <i>cross_section_shape</i>, <i>cross_section_width</i>,
        <i>cross_section_height</i>, and <i>cross_section_table</i>.
    </p>
    <br>
    <p>
        If the shape value is invalid, an empty string is returned.
    </p>
    <h4>Syntax</h4>
    <p>cross_section_label_single_line(units)</p>
    <h4>Arguments</h4>
    <p>units: 'mm' for millimeters or 'm' for meters</p>
    <p>single_line: True for single-line label or False for multi-line label</p>
"""


def cross_section_table_values(cross_section_table: str, shape_value: int):
    """Get height and width values."""
    height_list, width_list = [], []
    for row in cross_section_table.split("\n"):
        height_str, width_str = row.split(",")
        height = float(height_str)
        width = float(width_str)
        height_list.append(height)
        width_list.append(width)
    if shape_value == en.CrossSectionShape.YZ.value:
        height_list, width_list = width_list, height_list
    return height_list, width_list


def _cross_section_max_height(shape: int, width: float, height: float, table: str):
    """
    Get maximum height of the cross-section
    """
    if shape not in dm.ALL_SHAPES:
        raise ValueError("Invalid value for 'shape'")
    if shape in [dm.CrossSectionShape.EGG.value, dm.CrossSectionShape.INVERTED_EGG.value]:
        return 1.5 * width
    if shape in dm.TABLE_SHAPES:
        height_list, width_list = cross_section_table_values(table, shape)
        return max(height_list)
    if shape == dm.CrossSectionShape.OPEN_RECTANGLE.value:
        return None
    return height


@qgsfunction(args="auto", group="3Di", handlesnull=True, helpText=CROSS_SECTION_MAX_HEIGHT_HELPTEXT)
def cross_section_max_height(shape: int, width: float, height: float, table: str, feature, parent):
    """
    Get maximum height of the cross-section
    """
    return _cross_section_max_height(shape, width, height, table)


def _cross_section_max_width(shape: int, width: float, table: str):
    """
    Get maximum width of the cross-section
    """
    if shape not in dm.TABLE_SHAPES:
        return width
    height_list, width_list = cross_section_table_values(table, shape)
    return max(width_list)


@qgsfunction(args="auto", group="3Di", handlesnull=True, helpText=CROSS_SECTION_MAX_WIDTH_HELPTEXT)
def cross_section_max_width(shape: int, width: float, table: str, feature, parent):
    """
    Get maximum width of the cross-section
    """
    return _cross_section_max_width(shape, width, table)


def cross_section_label_multiline(feature, parent):
    """
    Create a multi-line label with the cross-section shape, max height and max width of the cross-section
    """
    label = ""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.ALL_SHAPES:
        return label
    shape_name = en.CrossSectionShape(shape_value).name.replace("_", " ")
    if shape_value != en.CrossSectionShape.YZ.value:
        shape_name = shape_name.capitalize()
    shape_value_and_name = f"{shape_value}: {shape_name}\n"
    label += shape_value_and_name
    width = feature["cross_section_width"]
    height = feature["cross_section_height"]
    if shape_value == en.CrossSectionShape.CLOSED_RECTANGLE.value:
        label += f"w: {width:.2f}\nh: {height:.2f}"
    elif shape_value == en.CrossSectionShape.OPEN_RECTANGLE.value:
        label += f"w: {width:.2f}"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width:.2f}"
    elif shape_value in {en.CrossSectionShape.EGG.value, en.CrossSectionShape.INVERTED_EGG.value}:
        label += f"w: {width:.2f}\nh: {width*1.5:.2f}"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table, shape_value)
        max_height = max(height_list)
        max_width = max(width_list)
        label += f"w: {max_width:.2f}\nh: {max_height:.2f}"
    return label


# @qgsfunction(args="auto", group="3Di")
# def diameter_label(feature, parent):
#     """
#     <p>Create a single line label describing the cross-section</p>
#     <br>
#     <p>
#         Features must have the fields <i>cross_section_shape</i>, <i>cross_section_width</i>,
#         <i>cross_section_height</i>, and <i>cross_section_table</i>.
#     </p>
#     <br>
#     <p>
#         If the shape value is invalid, an empty string is returned.
#     </p>
#     """
#     label = ""
#     shape_value = feature["cross_section_shape"]
#     if shape_value not in dm.ALL_SHAPES:
#         return label
#     width = feature["cross_section_width"]
#     height = feature["cross_section_height"]
#     if shape_value == en.CrossSectionShape.CLOSED_RECTANGLE.value:
#         label += f"rect {width * 1000:.0f}x{height * 1000:.0f}"
#     elif shape_value == en.CrossSectionShape.OPEN_RECTANGLE.value:
#         label += f"rect {width * 1000:.0f}"
#     elif shape_value == en.CrossSectionShape.CIRCLE.value:
#         label += f"Ø{width*1000:.0f}"
#     elif shape_value == en.CrossSectionShape.EGG.value:
#         label += f"egg {width*1000:.0f}/{width * 1000 * 1.5:.3f}"
#     elif shape_value in dm.TABLE_SHAPES:
#         table = feature["cross_section_table"]
#         height_list, width_list = cross_section_table_values(table, shape_value)
#         max_height = max(height_list)
#         max_width = max(width_list)
#         label += "tab " if shape_value != en.CrossSectionShape.YZ.value else "yz "
#         label += f"{max_width*1000:.0f}/{max_height*1000:.0f}"
#     return label


@qgsfunction(args="auto", group="3Di", handlesnull=True, helpText=CROSS_SECTION_LABEL_HELPTEXT)
def cross_section_label(
        shape: int,
        width: float,
        height: float,
        table: str,
        units: str,
        single_line: bool,
        feature,
        parent
):
    """

    """
    if shape not in dm.ALL_SHAPES:
        print("shape not in dm.ALL_SHAPES")
        return ""
    max_width = _cross_section_max_width(shape, width, table)
    max_height = _cross_section_max_height(shape, width, height, table)
    format_args = {"units": units}
    if units == "m":
        format_args.update(
            {
                "width_text": f"{max_width:.2f}" if max_width else "",
                "height_text": f"{max_height:.2f}" if max_height else ""
            }
        )
    elif units == "mm":
        format_args.update(
            {
                "width_text": f"{max_width * 1000:.0f}" if max_width else "",
                "height_text": f"{max_height * 1000:.0f}" if max_height else ""
            }
        )
    print(f"format_args: {format_args}")
    if single_line:
        label_templates = {
            en.CrossSectionShape.CLOSED_RECTANGLE.value: "w x h: {width_text} x {height_text} {units} (closed rect)",
            en.CrossSectionShape.OPEN_RECTANGLE.value: "w: {width_text} {units} (open rect)",
            en.CrossSectionShape.CIRCLE.value: "Ø: {width_text} {units} (circle)",
            en.CrossSectionShape.EGG.value: "w x h: {width_text} x {height_text} {units} (egg)",
            en.CrossSectionShape.INVERTED_EGG.value: "w x h: {width_text} x {height_text} {units} (inv egg)",
            en.CrossSectionShape.TABULATED_RECTANGLE.value: "w x h: {width_text} x {height_text} {units} (tab rect)",
            en.CrossSectionShape.TABULATED_TRAPEZIUM.value: "w x h: {width_text} x {height_text} {units} (tab trap)",
            en.CrossSectionShape.YZ.value: "w x h: {width_text} x {height_text} {units} (yz)",
        }
    else:
        label_templates = {
            en.CrossSectionShape.CLOSED_RECTANGLE.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
            en.CrossSectionShape.OPEN_RECTANGLE.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}",
            en.CrossSectionShape.CIRCLE.value:
                "{shape_value}: {shape_name}\n"
                "Ø: {width_text} {units}",
            en.CrossSectionShape.EGG.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
            en.CrossSectionShape.INVERTED_EGG.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
            en.CrossSectionShape.TABULATED_RECTANGLE.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
            en.CrossSectionShape.TABULATED_TRAPEZIUM.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
            en.CrossSectionShape.YZ.value:
                "{shape_value}: {shape_name}\n"
                "w: {width_text} {units}\n"
                "h: {height_text} {units}",
        }
        shape_name = en.CrossSectionShape(shape).name.replace("_", " ")
        if shape != en.CrossSectionShape.YZ.value:
            shape_name = shape_name.capitalize()
        format_args.update(
            {
                "shape_value": shape,
                "shape_name": shape_name,
            }
        )
    print(f"format_args: {format_args}")
    print(f"label_templates[shape]: {label_templates[shape]}")
    label = label_templates[shape].format(**format_args)
    print(f"label: {label}")
    return label

# @qgsfunction(args="auto", group="3Di")
# def width_label(feature, parent):
#     """Create label with width value."""
#     label = ""
#     shape_value = feature["cross_section_shape"]
#     if shape_value not in dm.ALL_SHAPES:
#         return label
#     width = feature["cross_section_width"]
#     if shape_value in {en.CrossSectionShape.OPEN_RECTANGLE.value, en.CrossSectionShape.CLOSED_RECTANGLE.value}:
#         label += f"w: {width:.2f} (rect)"
#     elif shape_value == en.CrossSectionShape.CIRCLE.value:
#         label += f"Ø{width:.2f}"
#     elif shape_value in {en.CrossSectionShape.EGG.value, en.CrossSectionShape.INVERTED_EGG.value}:
#         label += f"w: {width:.2f} (egg)"
#     elif shape_value in dm.TABLE_SHAPES:
#         table = feature["cross_section_table"]
#         height_list, width_list = cross_section_table_values(table, shape_value)
#         max_width = max(width_list)
#         label += f"w: {max_width:.2f} "
#         label += "(tab)" if shape_value != en.CrossSectionShape.YZ.value else "(yz)"
#     return label
#
