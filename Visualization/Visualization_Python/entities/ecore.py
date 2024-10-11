from typing import Dict, Any, List, Union

from entities.cluster import Cluster
from entities.component import Component

from utils.constants import ECORES
from utils.type_names import MCU, BMT, CBUS_INJ, CBUS_CLT, NFI_INJ, NFI_CLT, ECORE


class Ecore(Cluster):
    def __init__(self, cluster: List[Union[int, str]], data: Dict[str, Any]):
        mcu_data = data.get(MCU, [])
        super().__init__(cluster, mcu_data)
        self.data = data

        self.bmt = Component(None, BMT)
        self.cbus_inj = Component(None, CBUS_INJ)
        self.cbus_clt = Component(None, CBUS_CLT)
        self.nfi_inj = Component(None, NFI_INJ)
        self.nfi_clt = Component(None, NFI_CLT)
        self.ecores = []

        self.init_ecores()

    def init_ecores(self) -> None:
        for ecore in self.data.get(ECORES, []):
            ecore_obj = Component(None, ECORE)
            self.ecores.append(ecore_obj)

    def get_details(self) -> List[Component]:
        return [self.bmt, self.cbus_inj, self.cbus_clt, self.nfi_inj,
                self.nfi_clt, *self.ecores, *super().get_details()]

    def get_all_inner_details(self) -> List[Component]:
        return [self.bmt, self.cbus_inj, self.cbus_clt, self.nfi_inj,
                self.nfi_clt, *self.ecores, *super().get_all_inner_details()]
