from typing import Dict, Any, List, Union

from entities.cluster import Cluster
from entities.component import Component

from utils.type_names import SUBUNITS, MCU


class Cbu(Cluster):
    def __init__(self, cluster: List[Union[int, str]], data: Dict[str, Any]):
        mcu_data = data[MCU]
        super().__init__(cluster, mcu_data)
        self.data = data
        self.subunits: Dict[str, Component] = {
            subunit_type: Component(type_name=subunit_type) for subunit_type in SUBUNITS
        }

    def get_details(self) -> List[Component]:
        details = super().get_details()
        details.extend(self.subunits.values())
        return details

    def get_all_inner_details(self) -> List[Component]:
        all_inner_details = super().get_all_inner_details()
        all_inner_details.extend(self.subunits.values())
        return all_inner_details