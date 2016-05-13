from UM.Qt.ListModel import ListModel

from PyQt5.QtCore import pyqtProperty, Qt

from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Settings.DefinitionContainer import DefinitionContainer


##  Model that holds definition containers. By setting the filter property the definitions held by this model can be
#   changed.
class DefinitionContainersModel(ListModel):
    NameRole = Qt.UserRole + 1          # Human readable name (string)
    ManufacturerRole = Qt.UserRole + 2  # Manufacturer of definition / machine. (string)
    IdRole = Qt.UserRole + 3            # Unique ID of Definition

    def __init__(self, parent = None):
        super().__init__(parent)
        self.addRoleName(self.NameRole, "name")
        self.addRoleName(self.ManufacturerRole, "manufacturer")
        self.addRoleName(self.IdRole, "id")

        self._definition_containers = []

        # Listen to changes
        ContainerRegistry.getInstance().containerAdded.connect(self._onContainerChanged)
        ContainerRegistry.getInstance().containerAdded.connect(self._onContainerChanged)

        self._filter_dict = {}
        self._update()

    ##  Handler for container change events from registry
    def _onContainerChanged(self, container):
        # We only need to update when the changed container is a DefinitionContainer.
        if isinstance(container, DefinitionContainer):
            self._update()

    ##  Private convenience function to reset & repopulate the model.
    def _update(self):
        self.clear()
        self._definition_containers = ContainerRegistry.getInstance().findDefinitionContainers(**self._filter_dict)
        for container in self._definition_containers:
            self.appendItem({"name": container.getName(),
                             "manufacturer": container.getMetaDataEntry("manufacturer", ""),
                             "id": container.getId()})

    ##  Set the filter of this model based on a string.
    #   \param filter_dict Dictionary to do the filtering by.
    def setFilter(self, filter_dict):
        self._filter_dict = filter_dict
        self._update()

    @pyqtProperty("QVariantMap", fset = setFilter)
    def filter(self, filter):
        pass