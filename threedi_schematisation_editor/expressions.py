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


def cross_section_table_values(cross_section_table, shape_value):
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


@qgsfunction(args="auto", group="3Di", helpText=CROSS_SECTION_MAX_HEIGHT_HELPTEXT)
def cross_section_max_height(feature, parent, shape, width, height, table):
    """
    Get maximum height of the cross-section.
    """
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.TABLE_SHAPES:
        return feature["cross_section_height"]
    table = feature["cross_section_table"]
    height_list, width_list = cross_section_table_values(table, shape_value)
    return max(height_list)


@qgsfunction(args="auto", group="3Di", helpText=CROSS_SECTION_MAX_WIDTH_HELPTEXT)
def cross_section_max_width(feature, parent, shape: int, width: float, table: str):
    """
    Get maximum width of the cross-section
    """
    if shape not in dm.TABLE_SHAPES:
        return width
    height_list, width_list = cross_section_table_values(table, shape)
    return max(width_list)


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


@qgsfunction(args="auto", group="3Di")
def diameter_label(feature, parent):
    """
    <p>Create a single line label describing the cross-section</p>
    <br>
    <p>
        Features must have the fields <i>cross_section_shape</i>, <i>cross_section_width</i>,
        <i>cross_section_height</i>, and <i>cross_section_table</i>.
    </p>
    <br>
    <p>
        If the shape value is invalid, an empty string is returned.
    </p>
    """
    label = ""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.ALL_SHAPES:
        return label
    width = feature["cross_section_width"]
    height = feature["cross_section_height"]
    if shape_value == en.CrossSectionShape.CLOSED_RECTANGLE.value:
        label += f"rect {width * 1000:.0f}x{height * 1000:.0f}"
    elif shape_value == en.CrossSectionShape.OPEN_RECTANGLE.value:
        label += f"rect {width * 1000:.0f}"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width*1000:.0f}"
    elif shape_value == en.CrossSectionShape.EGG.value:
        label += f"egg {width*1000:.0f}/{width * 1000 * 1.5:.3f}"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table, shape_value)
        max_height = max(height_list)
        max_width = max(width_list)
        label += "tab " if shape_value != en.CrossSectionShape.YZ.value else "yz "
        label += f"{max_width*1000:.0f}/{max_height*1000:.0f}"
    return label


@qgsfunction(args="auto", group="3Di", helpText=CROSS_SECTION_LABEL_HELPTEXT)
def cross_section_label(feature, parent, units: str, single_line: bool):
    """

    """
    label = ""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.ALL_SHAPES:
        return label
    width = feature["cross_section_width"]
    height = feature["cross_section_height"]
    if units == "m":
        width_text = f"{width:.2f}" if width else ""
        height_text = f"{height:.2f}" if height else ""
        height_text_egg = f"{1.5 * width:.2f}" if width else ""
    elif units == "mm":
        width_text = f"{width * 1000:.0f}" if width else ""
        height_text = f"{height * 1000:.0f}" if height else ""
        height_text_egg = f"{1.5 * width * 1000:.0f}" if width else ""
    if shape_value == en.CrossSectionShape.CLOSED_RECTANGLE.value:
        label += f"w x h: {width_text} x {height_text} {units} (closed rect)"
    elif shape_value == en.CrossSectionShape.OPEN_RECTANGLE.value:
        label += f"w: {width_text} {units} (open rect)"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width_text} {units} (circle)"
    elif shape_value == en.CrossSectionShape.EGG.value:
        label += f"w x h: {width_text} x {height_text_egg} {units} (egg)"
    elif shape_value == en.CrossSectionShape.INVERTED_EGG.value:
        label += f"w x h: {width_text} x {height_text_egg} {units} (inv egg)"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table, shape_value)
        max_height = max(height_list)
        max_width = max(width_list)
        label += "tab " if shape_value != en.CrossSectionShape.YZ.value else "yz "
        label += f"{max_width*1000:.0f}/{max_height*1000:.0f}"
    return label


@qgsfunction(args="auto", group="3Di")
def width_label(feature, parent):
    """Create label with width value."""
    label = ""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.ALL_SHAPES:
        return label
    width = feature["cross_section_width"]
    if shape_value in {en.CrossSectionShape.OPEN_RECTANGLE.value, en.CrossSectionShape.CLOSED_RECTANGLE.value}:
        label += f"w: {width:.2f} (rect)"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width:.2f}"
    elif shape_value in {en.CrossSectionShape.EGG.value, en.CrossSectionShape.INVERTED_EGG.value}:
        label += f"w: {width:.2f} (egg)"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table, shape_value)
        max_width = max(width_list)
        label += f"w: {max_width:.2f} "
        label += "(tab)" if shape_value != en.CrossSectionShape.YZ.value else "(yz)"
    return label

