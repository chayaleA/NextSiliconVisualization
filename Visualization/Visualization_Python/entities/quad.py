from typing import Dict, Any, List, Union

from entities.component import Component
from entities.ecore import Ecore
from entities.cbu import Cbu
from entities.tcu import Tcu

from utils.constants import CBUS, TCUS, ROW, COL, CLUSTER_ID, NUM_CLUSTERS_PER_SIDE
from utils.type_names import QUAD, HBM, ECORE, CBU, TCU
from utils.error_messages import WarningMessages


class Quad(Component):

    def __init__(self, id: int, name: str, data: Dict[str, Any]):
        super().__init__(id, QUAD)
        self.name = name
        self.data = data
        self.clusters = [[None for _ in range(NUM_CLUSTERS_PER_SIDE)] for _ in range(NUM_CLUSTERS_PER_SIDE)]
        self.is_enable = False
        self.hbm = Component(None, HBM)

        self.init_clusters()

    def init_clusters(self) -> None:
        self.init_ecore()
        self.init_cbus()
        self.init_tcus()

    def init_ecore(self) -> None:
        ecore_json = self.data.get(ECORE)
        if not ecore_json:
            raise ValueError(WarningMessages.WARNING_MISSING_DATA.value.format(component=ECORE))
        cluster = self.init_cluster(ecore_json, ECORE)
        ecore = Ecore(cluster, ecore_json)
        self.clusters[ecore.row][ecore.col] = ecore

    def init_cbus(self) -> None:
        cbus = self.data.get(CBUS, [])
        for cbu_json in cbus:
            if not isinstance(cbu_json, dict):
                raise ValueError(WarningMessages.INVALID_DATA.value.format(component=CBU, data=cbu_json))
            cluster = self.init_cluster(cbu_json, CBU)
            cbu = Cbu(cluster, cbu_json)
            self.clusters[cbu.row][cbu.col] = cbu

    def init_tcus(self) -> None:
        tcus = self.data.get(TCUS, [])
        for tcu_json in tcus:
            if not isinstance(tcu_json, dict):
                raise ValueError(WarningMessages.INVALID_DATA.value.format(component=TCU, data=tcu_json))
            cluster = self.init_cluster(tcu_json, TCU)
            tcu = Tcu(cluster, tcu_json)
            self.clusters[tcu.row][tcu.col] = tcu

    def init_cluster(self, cluster_json: Dict[str, Any], type: str) -> List[Union[int, str]]:
        cluster = [
            int(cluster_json.get(ROW)),
            int(cluster_json.get(COL)),
            int(cluster_json.get(CLUSTER_ID)),
            type
        ]
        return cluster

    def get_attribute_from_active_logs(self, attribute: str) -> List[Any]:
        attributes = []
        for row in self.clusters:
            for cluster in row:
                if cluster is None:
                    continue
                attributes.extend(cluster.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
