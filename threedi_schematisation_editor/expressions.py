from qgis.utils import qgsfunction
import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en


CROSS_SECTION_MAX_WIDTH_HELPTEXT = """
    <p>Get maximum width of the cross-section.</p>
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
    <h4>Syntax</h4>
    <p>cross_section_max_width(shape, width, table)</p>
    <h4>Arguments</h4>
    <p>shape: cross section shape type (integer)</p>
    <p>width: cross section width (float)</p>
    <p>table: cross section table describing tabulated and YZ cross sections (string) </p>
    <h4>Examples</h4>
    <p>cross_section_max_width(cross_section_shape, cross_section_width, cross_section_table)  &#8594;  4.32</p> 
"""


CROSS_SECTION_MAX_HEIGHT_HELPTEXT = """
    <p>Get maximum height of the cross-section.</p>
    <p>The value returned depends on <i>cross_section_shape</i>:
    <ul>
        <li><i>None</i> for "Open rectangle"</li>
        <li><i>cross_section_height</i> for "Closed rectangle"</li>
        <li><i>cross_section_width</i> for "Circle"</li>
        <li>1.5 * <i>cross_section_width</i> for "Egg" and "Inverted egg"</li>
        <li>the maximum height value in <i>cross_section_table</i> for "Tabulated trapezium" and "Tabulated rectangle"</li>
        <li>the maximum Z value in the <i>cross_section_table</i> for "YZ"</li>
    </ul>
    <h4>Syntax</h4>
    <p>cross_section_max_height(shape, width, height, table)</p>
    <h4>Arguments</h4>
    <p>shape: cross section shape type (integer)</p>
    <p>width: cross section width (float)</p>
    <p>height: cross section height (float)</p>
    <p>table: cross section table describing tabulated and YZ cross sections (string) </p>
    <h4>Examples</h4>
    <p>
        cross_section_max_height(cross_section_shape, cross_section_width, cross_section_height, cross_section_table)  
        &#8594; 4.32
    </p> 
"""


CROSS_SECTION_LABEL_HELPTEXT = """
    <p>Create a label describing the cross-section</p>
    <p>
        Features must have the fields <i>cross_section_shape</i>, <i>cross_section_width</i>,
        <i>cross_section_height</i>, and <i>cross_section_table</i>.
    </p>
    <p>
        If the shape value is invalid, an empty string is returned.
    </p>
    <h4>Syntax</h4>
    <p>cross_section_label(shape, width, height, table, units, single_line)</p>
    <h4>Arguments</h4>
    <p>shape: cross section shape type (integer)</p>
    <p>width: cross section width (float)</p>
    <p>height: cross section height (float)</p>
    <p>table: cross section table describing tabulated and YZ cross sections (string) </p>
    <p>units: 'mm' for millimeters, 'm' for meters (string) </p>
    <p>single_line: True for single-line label or False for multi-line label (boolean)</p>
    <h4>Examples</h4>
    <p>cross_section_label(cross_section_shape, cross_section_width, cross_section_height, cross_section_table, 'mm', 
    True) &#8594; <pre>
    'Ø 400 mm (circle)'
    </pre>
    </p>
    <p>cross_section_label(cross_section_shape, cross_section_width, cross_section_height, cross_section_table, 'm', 
    False) &#8594; <pre>
    '2: Circle
    Ø: 0.40 m'
    </pre>
    </p>
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
) -> str:
    """
    Get a string describing the cross-section, that can be used as a label in QGIS
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
            en.CrossSectionShape.CIRCLE.value: "Ø: {width_text} {units}",
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
