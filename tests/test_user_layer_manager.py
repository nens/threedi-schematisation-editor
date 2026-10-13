from qgis.core import QgsLayerTreeNode, QgsProject

from threedi_schematisation_editor import ThreediSchematisationEditorPlugin
from threedi_schematisation_editor.user_layer_manager import (
    SCHEMATISATION_DISPLAY_NAME_OVERRIDE_KEY,
    SCHEMATISATION_GPKG_PATH_KEY,
    SCHEMATISATION_IS_MODEL_GROUP_KEY,
    LayersManager,
)


def make_layers_manager(group_name=None):
    manager = LayersManager.__new__(LayersManager)
    manager.model_gpkg_path = "/models/test.gpkg"
    manager.group_name_override = group_name
    manager.__dict__["model_revision"] = None
    return manager


def test_find_schematisation_groups_supports_marker_and_legacy_name():
    # Build a layer tree with a marked custom name, a legacy prefixed name, and
    # an unrelated group; discovery should return only the first two.
    root = QgsProject.instance().layerTreeRoot()
    root.removeAllChildren()
    custom_group = root.addGroup("Canonical name")
    custom_group.setCustomProperty(SCHEMATISATION_IS_MODEL_GROUP_KEY, True)
    legacy_group = root.addGroup("Rana schematisation: legacy")
    unrelated_group = root.addGroup("Other group")

    groups = ThreediSchematisationEditorPlugin._find_schematisation_groups(root)

    assert groups == [custom_group, legacy_group]
    assert unrelated_group not in groups


def test_register_groups_restores_override_from_group_matching_model_path():
    # Set up an in-memory QGIS layer tree with group properties and a fresh
    # manager without an override.
    root = QgsProject.instance().layerTreeRoot()
    root.removeAllChildren()
    host_group = root.addGroup("Host")
    saved_group = host_group.addGroup("Canonical name")
    saved_group.setCustomProperty(SCHEMATISATION_GPKG_PATH_KEY, "/models/test.gpkg")
    saved_group.setCustomProperty(
        SCHEMATISATION_DISPLAY_NAME_OVERRIDE_KEY, "Canonical name"
    )
    for name in make_layers_manager().group_names:
        saved_group.addGroup(name)

    manager = make_layers_manager()
    manager.parents = []
    manager.spawned_groups = {}

    assert manager.register_groups()
    assert manager.group_name_override == "Canonical name"
    assert manager.main_group == "Canonical name"
    # Registration should bind each layer group name to its actual tree node.
    assert manager.spawned_groups == {
        group.name(): group for group in saved_group.children()
    }


def test_remove_groups_uses_persisted_identity():
    # Put two groups in the in-memory layer tree. Removal should use the target
    # group's model-path property rather than its custom display name, and leave
    # the unrelated group alone.
    root = QgsProject.instance().layerTreeRoot()
    root.removeAllChildren()
    host_group = root.addGroup("Host")
    saved_group = host_group.addGroup("Canonical name")
    saved_group.setCustomProperty(SCHEMATISATION_GPKG_PATH_KEY, "/models/test.gpkg")
    other_group = host_group.addGroup("Other schematisation")
    manager = make_layers_manager()
    manager.parents = []
    manager.model_handlers = {}
    manager.layer_handlers = {}
    manager.spawned_groups = {}

    manager.remove_groups()

    assert host_group.findGroup("Canonical name") is None
    assert host_group.findGroup("Other schematisation") == other_group


def test_create_groups_sets_model_identity_and_discovery_metadata():
    # Creating a group attaches the identity, discovery marker, and optional
    # display-name properties to its in-memory layer-tree node.
    root = QgsProject.instance().layerTreeRoot()
    root.removeAllChildren()
    manager = make_layers_manager("Canonical name")
    manager.parents = []
    manager.layer_handlers = {}
    manager.model_handlers = {}
    manager.spawned_groups = {}

    manager.create_groups()

    group = root.findGroup("Canonical name")
    assert group.customProperty(SCHEMATISATION_GPKG_PATH_KEY) == "/models/test.gpkg"
    assert group.customProperty(SCHEMATISATION_IS_MODEL_GROUP_KEY)
    assert (
        group.customProperty(SCHEMATISATION_DISPLAY_NAME_OVERRIDE_KEY)
        == "Canonical name"
    )


def test_register_groups_falls_back_to_legacy_name():
    # Set up an in-memory legacy-shaped group without custom properties.
    # Registration should use its original prefixed name and bind the expected
    # child group nodes; this does not load an old QGIS project file.
    root = QgsProject.instance().layerTreeRoot()
    root.removeAllChildren()
    manager = make_layers_manager()
    manager.parents = []
    manager.spawned_groups = {}
    legacy_group = root.addGroup(manager.main_group)
    child_groups = {}
    for name in manager.group_names:
        child_groups[name] = legacy_group.addGroup(name)

    # Confirm this fixture exercises the legacy path rather than identity lookup.
    assert manager._find_group_by_model_path() is None
    assert manager.register_groups()
    assert manager.spawned_groups == child_groups
