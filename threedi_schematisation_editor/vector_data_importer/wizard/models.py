from dataclasses import asdict, dataclass


@dataclass
class GenericSettingsModel:
    selected_layer: str = ""
    use_selected_features: bool = False

    def serialize(self):
        return asdict(self)


@dataclass
class ConnectionNodeSettingsModel:
    # TODO: connect with models in settings_model
    create_nodes: bool = False
    snap_enabled: bool = False
    snap_distance: float = 1.0

    def serialize(self):
        return asdict(self)
