from pathlib import Path
from types import MappingProxyType

DEFAULT_STYLE_CATEGORIES = {  # Names should be the same as keys in the QML file
    "aliases",
    "attributetableconfig",
    "constraints",
    "fieldConfiguration",
}

DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY = DEFAULT_STYLE_CATEGORIES | {
    "labeling",
    "previewExpression",  # display name
    "renderer-v2",  # symbology
}


class StyleConfig:
    def __init__(self):
        self.style_categories = set()
        self.styles = dict()

    def is_valid(self, style_dir: Path):
        """
        Returns True if all styles contain all style_categories as keys
        and all referenced qml files exist
        """
        valid = True
        for style_name, style_data in self.styles.items():
            missing = self.style_categories - set(style_data.keys())
            if missing:
                print(f"Some required style categories are missing: {missing}")
                valid = False
            missing = set(style_data.keys()) - self.style_categories
            if missing:
                print(
                    f"Some style categories are included but are not in the list of required style categories: {missing}"
                )
                valid = False
            for qml_path in style_data.values():
                if not (style_dir / qml_path).is_file():
                    print(f"File not found: {(style_dir / qml_path)}")
                    valid = False
        return valid


style_config_data = MappingProxyType(
    {
        "aggregation_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("aggregation_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("aggregation_settings") / "attributetableconfig" / "default.qml",
                    "constraints": Path("aggregation_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("aggregation_settings") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "boundary_condition_1d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("boundary_condition_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("boundary_condition_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("boundary_condition_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("boundary_condition_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_1d") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "boundary_condition_2d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("boundary_condition_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("boundary_condition_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("boundary_condition_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("boundary_condition_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("boundary_condition_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("boundary_condition_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("boundary_condition_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("boundary_condition_2d") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "channel": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("channel") / "aliases" / "default.qml",
                    "attributetableconfig": Path("channel") / "attributetableconfig" / "default.qml",
                    "constraints": Path("channel") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("channel") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("channel") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("channel") / "aliases" / "default.qml",
                    "attributetableconfig": Path("channel") / "attributetableconfig" / "default.qml",
                    "constraints": Path("channel") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("channel") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("channel") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("channel") / "aliases" / "default.qml",
                    "attributetableconfig": Path("channel") / "attributetableconfig" / "default.qml",
                    "constraints": Path("channel") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("channel") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("channel") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("channel") / "aliases" / "default.qml",
                    "attributetableconfig": Path("channel") / "attributetableconfig" / "default.qml",
                    "constraints": Path("channel") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("channel") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("channel") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "connection_node": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("connection_node") / "aliases" / "default.qml",
                    "attributetableconfig": Path("connection_node") / "attributetableconfig" / "default.qml",
                    "constraints": Path("connection_node") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("connection_node") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("connection_node") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("connection_node") / "aliases" / "default.qml",
                    "attributetableconfig": Path("connection_node") / "attributetableconfig" / "default.qml",
                    "constraints": Path("connection_node") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("connection_node") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("connection_node") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("connection_node") / "aliases" / "default.qml",
                    "attributetableconfig": Path("connection_node") / "attributetableconfig" / "default.qml",
                    "constraints": Path("connection_node") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("connection_node") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("connection_node") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("connection_node") / "aliases" / "default.qml",
                    "attributetableconfig": Path("connection_node") / "attributetableconfig" / "default.qml",
                    "constraints": Path("connection_node") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("connection_node") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("connection_node") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "cross_section_location": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("cross_section_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("cross_section_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("cross_section_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("cross_section_location") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("cross_section_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("cross_section_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("cross_section_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("cross_section_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("cross_section_location") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("cross_section_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("cross_section_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("cross_section_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("cross_section_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("cross_section_location") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("cross_section_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("cross_section_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("cross_section_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("cross_section_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("cross_section_location") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("cross_section_location") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "culvert": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("culvert") / "aliases" / "default.qml",
                    "attributetableconfig": Path("culvert") / "attributetableconfig" / "default.qml",
                    "constraints": Path("culvert") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("culvert") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("culvert") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("culvert") / "aliases" / "default.qml",
                    "attributetableconfig": Path("culvert") / "attributetableconfig" / "default.qml",
                    "constraints": Path("culvert") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("culvert") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("culvert") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("culvert") / "aliases" / "default.qml",
                    "attributetableconfig": Path("culvert") / "attributetableconfig" / "default.qml",
                    "constraints": Path("culvert") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("culvert") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("culvert") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("culvert") / "aliases" / "default.qml",
                    "attributetableconfig": Path("culvert") / "attributetableconfig" / "default.qml",
                    "constraints": Path("culvert") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("culvert") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("culvert") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "dem_average_area": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("dem_average_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dem_average_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dem_average_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dem_average_area") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dem_average_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("dem_average_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dem_average_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dem_average_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dem_average_area") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dem_average_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("dem_average_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dem_average_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dem_average_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dem_average_area") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dem_average_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("dem_average_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dem_average_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dem_average_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dem_average_area") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dem_average_area") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "dry_weather_flow": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("dry_weather_flow") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("dry_weather_flow") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("dry_weather_flow") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("dry_weather_flow") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "dry_weather_flow_distribution": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("dry_weather_flow_distribution") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow_distribution")
                    / "attributetableconfig"
                    / "default.qml",
                    "constraints": Path("dry_weather_flow_distribution") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow_distribution") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "dry_weather_flow_map": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("dry_weather_flow_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("dry_weather_flow_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("dry_weather_flow_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("dry_weather_flow_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("dry_weather_flow_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("dry_weather_flow_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("dry_weather_flow_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("dry_weather_flow_map") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "exchange_line": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("exchange_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("exchange_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("exchange_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("exchange_line") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("exchange_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("exchange_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("exchange_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("exchange_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("exchange_line") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("exchange_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("exchange_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("exchange_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("exchange_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("exchange_line") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("exchange_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("exchange_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("exchange_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("exchange_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("exchange_line") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("exchange_line") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "grid_refinement_area": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("grid_refinement_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_area") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_area") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("grid_refinement_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_area") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_area") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("grid_refinement_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_area") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_area") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_area") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("grid_refinement_area") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_area") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_area") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_area") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_area") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_area") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "grid_refinement_line": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("grid_refinement_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_line") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_line") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("grid_refinement_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_line") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_line") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("grid_refinement_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_line") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_line") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_line") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("grid_refinement_line") / "aliases" / "default.qml",
                    "attributetableconfig": Path("grid_refinement_line") / "attributetableconfig" / "default.qml",
                    "constraints": Path("grid_refinement_line") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("grid_refinement_line") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("grid_refinement_line") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("grid_refinement_line") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "groundwater": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("groundwater") / "aliases" / "default.qml",
                    "attributetableconfig": Path("groundwater") / "attributetableconfig" / "default.qml",
                    "constraints": Path("groundwater") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("groundwater") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("groundwater") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "initial_conditions": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("initial_conditions") / "aliases" / "default.qml",
                    "attributetableconfig": Path("initial_conditions") / "attributetableconfig" / "default.qml",
                    "constraints": Path("initial_conditions") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("initial_conditions") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("initial_conditions") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "interception": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("interception") / "aliases" / "default.qml",
                    "attributetableconfig": Path("interception") / "attributetableconfig" / "default.qml",
                    "constraints": Path("interception") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("interception") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "interflow": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("interflow") / "aliases" / "default.qml",
                    "attributetableconfig": Path("interflow") / "attributetableconfig" / "default.qml",
                    "constraints": Path("interflow") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("interflow") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("interflow") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "lateral_1d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("lateral_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("lateral_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("lateral_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("lateral_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_1d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_1d") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "lateral_2d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("lateral_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("lateral_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("lateral_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_2d") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("lateral_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("lateral_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("lateral_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("lateral_2d") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("lateral_2d") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "material": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("material") / "aliases" / "default.qml",
                    "attributetableconfig": Path("material") / "attributetableconfig" / "default.qml",
                    "constraints": Path("material") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("material") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "measure_location": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("measure_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_location") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_location") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("measure_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_location") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_location") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("measure_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_location") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_location") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_location") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("measure_location") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_location") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_location") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_location") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_location") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_location") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "measure_map": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("measure_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_map") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_map") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("measure_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_map") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_map") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("measure_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_map") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_map") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("measure_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("measure_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("measure_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("measure_map") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("measure_map") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("measure_map") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "memory_control": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("memory_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("memory_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("memory_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("memory_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("memory_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("memory_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("memory_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("memory_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("memory_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("memory_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("memory_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("memory_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("memory_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("memory_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("memory_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("memory_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("memory_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("memory_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("memory_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("memory_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("memory_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("memory_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("memory_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("memory_control") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "model_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("model_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("model_settings") / "attributetableconfig" / "default.qml",
                    "constraints": Path("model_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("model_settings") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("model_settings") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "numerical_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("numerical_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("numerical_settings") / "attributetableconfig" / "default.qml",
                    "constraints": Path("numerical_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("numerical_settings") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("numerical_settings") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "obstacle": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("obstacle") / "aliases" / "default.qml",
                    "attributetableconfig": Path("obstacle") / "attributetableconfig" / "default.qml",
                    "constraints": Path("obstacle") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("obstacle") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("obstacle") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("obstacle") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("obstacle") / "aliases" / "default.qml",
                    "attributetableconfig": Path("obstacle") / "attributetableconfig" / "default.qml",
                    "constraints": Path("obstacle") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("obstacle") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("obstacle") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("obstacle") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("obstacle") / "aliases" / "default.qml",
                    "attributetableconfig": Path("obstacle") / "attributetableconfig" / "default.qml",
                    "constraints": Path("obstacle") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("obstacle") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("obstacle") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("obstacle") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("obstacle") / "aliases" / "default.qml",
                    "attributetableconfig": Path("obstacle") / "attributetableconfig" / "default.qml",
                    "constraints": Path("obstacle") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("obstacle") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("obstacle") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("obstacle") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "orifice": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("orifice") / "aliases" / "default.qml",
                    "attributetableconfig": Path("orifice") / "attributetableconfig" / "default.qml",
                    "constraints": Path("orifice") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("orifice") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("orifice") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("orifice") / "aliases" / "default.qml",
                    "attributetableconfig": Path("orifice") / "attributetableconfig" / "default.qml",
                    "constraints": Path("orifice") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("orifice") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("orifice") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("orifice") / "aliases" / "default.qml",
                    "attributetableconfig": Path("orifice") / "attributetableconfig" / "default.qml",
                    "constraints": Path("orifice") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("orifice") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("orifice") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("orifice") / "aliases" / "default.qml",
                    "attributetableconfig": Path("orifice") / "attributetableconfig" / "default.qml",
                    "constraints": Path("orifice") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("orifice") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("orifice") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "physical_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("physical_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("physical_settings") / "attributetableconfig" / "default.qml",
                    "constraints": Path("physical_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("physical_settings") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "pipe": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("pipe") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pipe") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pipe") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pipe") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pipe") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("pipe") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pipe") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pipe") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pipe") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pipe") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("pipe") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pipe") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pipe") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pipe") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pipe") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("pipe") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pipe") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pipe") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pipe") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pipe") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "potential_breach": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("potential_breach") / "aliases" / "default.qml",
                    "attributetableconfig": Path("potential_breach") / "attributetableconfig" / "default.qml",
                    "constraints": Path("potential_breach") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("potential_breach") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("potential_breach") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("potential_breach") / "aliases" / "default.qml",
                    "attributetableconfig": Path("potential_breach") / "attributetableconfig" / "default.qml",
                    "constraints": Path("potential_breach") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("potential_breach") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("potential_breach") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("potential_breach") / "aliases" / "default.qml",
                    "attributetableconfig": Path("potential_breach") / "attributetableconfig" / "default.qml",
                    "constraints": Path("potential_breach") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("potential_breach") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("potential_breach") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("potential_breach") / "aliases" / "default.qml",
                    "attributetableconfig": Path("potential_breach") / "attributetableconfig" / "default.qml",
                    "constraints": Path("potential_breach") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("potential_breach") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("potential_breach") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "pump": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("pump") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("pump") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("pump") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("pump") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "pump_map": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("pump_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("pump_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("pump_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("pump_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("pump_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("pump_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("pump_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("pump_map") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "schema_version": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"editable"},
            "styles": {
                "default": {
                    "aliases": Path("schema_version") / "aliases" / "default.qml",
                    "attributetableconfig": Path("schema_version") / "attributetableconfig" / "default.qml",
                    "constraints": Path("schema_version") / "constraints" / "default.qml",
                    "editable": Path("schema_version") / "editable" / "default.qml",
                    "fieldConfiguration": Path("schema_version") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "simple_infiltration": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("simple_infiltration") / "aliases" / "default.qml",
                    "attributetableconfig": Path("simple_infiltration") / "attributetableconfig" / "default.qml",
                    "constraints": Path("simple_infiltration") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("simple_infiltration") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("simple_infiltration") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "simulation_template_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("simulation_template_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("simulation_template_settings")
                    / "attributetableconfig"
                    / "default.qml",
                    "constraints": Path("simulation_template_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("simulation_template_settings") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "surface": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("surface") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("surface") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("surface") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("surface") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "surface_map": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("surface_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("surface_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("surface_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface_map") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("surface_map") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface_map") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface_map") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface_map") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("surface_map") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "surface_parameters": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("surface_parameters") / "aliases" / "default.qml",
                    "attributetableconfig": Path("surface_parameters") / "attributetableconfig" / "default.qml",
                    "constraints": Path("surface_parameters") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("surface_parameters") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "table_control": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("table_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("table_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("table_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("table_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("table_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("table_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("table_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("table_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("table_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("table_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("table_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("table_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("table_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("table_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("table_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("table_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("table_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("table_control") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("table_control") / "aliases" / "default.qml",
                    "attributetableconfig": Path("table_control") / "attributetableconfig" / "default.qml",
                    "constraints": Path("table_control") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("table_control") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("table_control") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("table_control") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "tag": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("tag") / "aliases" / "default.qml",
                    "attributetableconfig": Path("tag") / "attributetableconfig" / "default.qml",
                    "constraints": Path("tag") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("tag") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "time_step_settings": {
            "style_categories": DEFAULT_STYLE_CATEGORIES | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("aggregation_settings") / "aliases" / "default.qml",
                    "attributetableconfig": Path("aggregation_settings") / "attributetableconfig" / "default.qml",
                    "constraints": Path("aggregation_settings") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("time_step_settings") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("time_step_settings") / "attributeEditorForm" / "default.qml",
                },
            },
        },
        "vegetation_drag_2d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES,
            "styles": {
                "default": {
                    "aliases": Path("vegetation_drag_2d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("vegetation_drag_2d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("vegetation_drag_2d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("vegetation_drag_2d") / "fieldConfiguration" / "default.qml",
                },
            },
        },
        "weir": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY,
            "styles": {
                "default": {
                    "aliases": Path("weir") / "aliases" / "default.qml",
                    "attributetableconfig": Path("weir") / "attributetableconfig" / "default.qml",
                    "constraints": Path("weir") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("weir") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("weir") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("weir") / "aliases" / "default.qml",
                    "attributetableconfig": Path("weir") / "attributetableconfig" / "default.qml",
                    "constraints": Path("weir") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("weir") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("weir") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("weir") / "aliases" / "default.qml",
                    "attributetableconfig": Path("weir") / "attributetableconfig" / "default.qml",
                    "constraints": Path("weir") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("weir") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("weir") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("weir") / "aliases" / "default.qml",
                    "attributetableconfig": Path("weir") / "attributetableconfig" / "default.qml",
                    "constraints": Path("weir") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("weir") / "fieldConfiguration" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("weir") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
        "windshielding_1d": {
            "style_categories": DEFAULT_STYLE_CATEGORIES_WITH_GEOMETRY | {"attributeEditorForm"},
            "styles": {
                "default": {
                    "aliases": Path("windshielding_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("windshielding_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("windshielding_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("windshielding_1d") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("windshielding_1d") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "default.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("windshielding_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "id": {
                    "aliases": Path("windshielding_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("windshielding_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("windshielding_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("windshielding_1d") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("windshielding_1d") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "id.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("windshielding_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "code": {
                    "aliases": Path("windshielding_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("windshielding_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("windshielding_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("windshielding_1d") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("windshielding_1d") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "code.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("windshielding_1d") / "renderer-v2" / "default.qml",  # symbology
                },
                "display_name": {
                    "aliases": Path("windshielding_1d") / "aliases" / "default.qml",
                    "attributetableconfig": Path("windshielding_1d") / "attributetableconfig" / "default.qml",
                    "constraints": Path("windshielding_1d") / "constraints" / "default.qml",
                    "fieldConfiguration": Path("windshielding_1d") / "fieldConfiguration" / "default.qml",
                    "attributeEditorForm": Path("windshielding_1d") / "attributeEditorForm" / "default.qml",
                    "labeling": Path("general") / "labeling" / "display_name.qml",
                    "previewExpression": Path("general") / "previewExpression" / "default.qml",  # display name
                    "renderer-v2": Path("windshielding_1d") / "renderer-v2" / "default.qml",  # symbology
                },
            },
        },
    }
)


def styles_location():
    return Path(__file__).parent / "vector"


def get_style_configurations():
    style_configs = {}
    for layer_name, layer_data in style_config_data.items():
        style_config = StyleConfig()
        style_config.style_categories = layer_data["style_categories"]
        style_config.styles = layer_data["styles"]
        style_configs[layer_name] = style_config
    return style_configs
