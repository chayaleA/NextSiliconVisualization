from typing import Optional, List, Any

from utils.error_messages import ErrorMessages


class Component:
    _id_counter = 0  # Static variable to keep track of IDs

    def __init__(self, id: Optional[int] = None, type_name: Optional[str] = None):
        if id is None:
            Component._id_counter += 1
            self.id = Component._id_counter
        else:
            self.id = id
        self.type_name = type_name
        self.active_logs: List[Any] = []  # List to hold active logs

    def get_attribute_from_active_logs(self, attribute: str) -> List[Any]:
        """
        Retrieve the specified attribute from all active logs present in the inner layers
        for the derived classes. The active logs are specific to this component and can
        include various details about its state or configuration.

        :param attribute: The attribute to retrieve from the active logs.
        :return: A list of values for the specified attribute from all inner components.
        """
        try:
            attributes = [getattr(log, attribute) for log in self.active_logs] if self.active_logs else []
        except AttributeError as e:
            print(ErrorMessages.FAILED_TO_RETIEVE_ATTRIBUTE.value.format(attribute=attribute, error=str(e)))
            return []
        return attributes
