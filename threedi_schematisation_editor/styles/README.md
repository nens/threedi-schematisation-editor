# Vector styles

All vector layers (including layers without geometry) have one or multiple predefined styles. Each style consists of several categories (e.g. symbology, labelling, attribute form, etc.). QML files can contain style settings for one, several, or all of these categories.

If a layer has multiple styles, differences between these styles are usually limited to a subset of styling categories. For example, the only difference between the "default" and "code" styles of the Channel layer is the labelling. To keep this manageable, a system has been implemented that allows the sharing of style categories between styles. In our example, the "code" style will refer the  exact same .qml files as the "default" style, *except* for the labelling. If we change the symbology qml, these changes will automatically be reflected in both the "default" and the "code" style. 

The names of the styling categories are the same as the keys in the QML file.

The styling system has two components: the qml files and a configuration.

## QML files

The QML files are stored in ``vector/{layer_name}/{styling_category}``. In our example, there would be one for field aliases, ``vector/channel/aliases/default.qml``, and two files for labelling: ``vector/channel/labelling/default.qml`` and ``vector/channel/labelling/code.qml``.

Some style settings are shared among all layers. These are stored in `vector/general`. For example, `vector/general/previewExpression/default.qml`

## Configuration

The configuration is defined in `style_config.py`. All styles for a layer must have the same style categories. For example, the "default" style of the channel layer does not have any labelling, but because the "code" style of that layer does have labelling, a "labelling" qml must also be configured for the "default" style. The reason for this is that when users switch back from "code" to "default", the labelling must be reset as well.

## Field configurations
Field configurations (e.g. should it be shown to the users as a boolean/checkbox, value map, text edit etc.) are automatically chosen based on the type annotations in threedi_schematisation_editor.data_models.py. For example, to define a value map, the field type should be an Enum, such as this field in `aggregation_settings`:     

    aggregation_method: Optional[AggregationMethod]

## Defaults
Defaults for layers with layer handlers are set in `user_layer_handlers.py`.

## Validation in attribute forms
Very basic validation in the attribute forms is implemented in that required fields are colored orange when not filled in. Which fields are required is configured in `data_models.py` using type annotations. E.g. `str` indicates a required field of type `str`, while `Optional[str]` denotes a non-required field of type `str` 


