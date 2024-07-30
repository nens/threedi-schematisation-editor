# Copyright (C) 2024 by Lutra Consulting


class WorkspaceContextManager:
    def __init__(self):
        self._active_lm_gpkg = None
        self.layer_managers = {}

    def __iter__(self):
        for lm in self.layer_managers.values():
            yield lm

    def __contains__(self, layer_manager):
        return layer_manager.model_gpkg_path in self.layer_managers

    @property
    def active_layer_manager(self):
        try:
            lm = self.layer_managers[self._active_lm_gpkg]
        except KeyError:
            lm = None
        return lm

    @active_layer_manager.setter
    def active_layer_manager(self, layer_manager):
        self._active_lm_gpkg = layer_manager.model_gpkg_path

    @active_layer_manager.deleter
    def active_layer_manager(self):
        self._active_lm_gpkg = None

    @property
    def active_layer_manager_geopackage(self):
        return self._active_lm_gpkg

    def register_layer_manager(self, layer_manager, set_active=True):
        if layer_manager not in self:
            self.layer_managers[layer_manager.model_gpkg_path] = layer_manager
            if set_active:
                self.set_active_layer_manager(layer_manager)

    def unregister_layer_manager(self, layer_manager):
        if layer_manager in self:
            if layer_manager == self.active_layer_manager:
                del self.active_layer_manager
            del self.layer_managers[layer_manager.model_gpkg_path]
            if self.layer_managers:
                self.set_active_layer_manager(next(iter(self.layer_managers.values())))

    def unregister_all(self):
        del self.active_layer_manager
        self.layer_managers.clear()

    def set_active_layer_manager(self, layer_manager):
        self.active_layer_manager = layer_manager
