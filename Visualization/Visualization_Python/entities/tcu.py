from typing import Dict, Any, List, Union

from entities.cluster import Cluster
from entities.component import Component

from utils.type_names import MCU


class Tcu(Cluster):
    def __init__(self, cluster: List[Union[int, str]], data: Dict[str, Any]):
        mcu_data = data.get(MCU)
        super().__init__(cluster, mcu_data)
        self.data = data

    def get_details(self) -> List[Component]:
        return super().get_details()

    def get_all_inner_details(self) -> List[Component]:
        return super().get_all_inner_details()
