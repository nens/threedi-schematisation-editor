from dataclasses import asdict, dataclass


@dataclass
class GenericSettingsModel:
    selected_layer: str = ""
    use_selected_features: bool = False

    def serialize(self):
        return asdict(self)
