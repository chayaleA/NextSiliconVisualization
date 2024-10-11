from typing import Dict, Any, List

from entities.component import Component

from utils.constants import EQS, ID
from utils.type_names import EQ, IRQA


class G2h(Component):
    def __init__(self, id: int, type: str, data: Dict[str, Any]):
        super().__init__(id, type)
        self.data = data
        self.g2h_irqa = Component(None, IRQA)
        self.eqs = []

        self.init_eqs()

    def init_eqs(self) -> None:
        for eq in self.data.get(EQS, []):
            eq = Component(eq[ID], EQ)
            self.eqs.append(eq)

    def get_details(self) -> List[Component]:
        return [self.g2h_irqa, *self.eqs]

    def get_attribute_from_active_logs(self, attribute: str) -> List[Any]:
        attributes = []
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
