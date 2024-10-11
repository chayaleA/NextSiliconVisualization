from typing import Dict, Any, List

from entities.component import Component
from entities.quad import Quad

from utils.constants import GRID, QUADS, NAME, ID, NUM_QUADS_PER_SIDE
from utils.type_names import DIE


class Die(Component):

    def __init__(self, id: int, data: Dict[str, Any]):
        super().__init__(id, DIE)
        self.quads: List[List[Quad]] = [[None for _ in range(NUM_QUADS_PER_SIDE)] for _ in
                                        range(NUM_QUADS_PER_SIDE)]
        self.data = data
        self.init_quads()
        self.is_enable = False

    def init_quads(self) -> None:
        quads = self.data.get(GRID, {}).get(QUADS, [])
        positions = [(row, col) for row in range(NUM_QUADS_PER_SIDE) for col in range(NUM_QUADS_PER_SIDE)]

        for index, quad_data in enumerate(quads):
            pos = positions[index % len(positions)]
            row, col = pos

            new_quad = Quad(quad_data.get(ID), quad_data.get(NAME), quad_data)
            self.quads[row][col] = new_quad

    def get_attribute_from_active_logs(self, attribute: str) -> List[Any]:
        attributes = []
        for row in self.quads:
            for quad in row:
                attributes.extend(quad.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
