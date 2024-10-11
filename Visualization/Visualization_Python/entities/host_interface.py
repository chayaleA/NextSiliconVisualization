from typing import Dict, Any, List

from entities.component import Component
from entities.h2g import H2g
from entities.g2h import G2h

from utils.type_names import HOST_INTERFACE, BMT, H2G, G2H, PCIE


class HostInterface(Component):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(None, HOST_INTERFACE)
        self.bmt = Component(None, BMT)
        self.h2g = H2g(None, H2G)
        self.g2h = G2h(None, G2H, data.get(G2H, {}))
        self.pcie = Component(None, PCIE)

    def get_details(self) -> List[Component]:
        return [self.bmt, self.h2g, self.g2h, self.pcie]

    def get_all_inner_details(self) -> List[Component]:
        return [self.bmt, self.pcie, *self.h2g.get_details(), *self.g2h.get_details()]

    def get_attribute_from_active_logs(self, attribute: str) -> List[Any]:
        attributes = []
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
