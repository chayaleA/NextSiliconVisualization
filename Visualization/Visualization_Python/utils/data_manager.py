import json
import datetime
from typing import Dict, Any, List

from entities.die import Die
from entities.host_interface import HostInterface
from entities.component import Component

import filter_factory_module
import logs_factory

from utils.filter_types import FILTER_TYPES_NAMES, CLUSTER, IO
from utils.type_names import HOST_INTERFACE, BMT, PCIE, AREAS, D2D, ECORE, EQ, HBM, MCU, QUAD, DIE
from utils.constants import TOP, DIES, ID, ENABLED_CLUSTERS, COL, DID, ROW, NUM_DIES, NUM_QUADS_PER_SIDE, READ, \
    TIMESTAMP, CLUSTER_ID, CHIP, AREA, UNIT, TID, PACKET
from utils.paths import LOGS_CSV
from utils.error_messages import ErrorMessages, WarningMessages


class DataManager:
    def __init__(self, chip_file: str, sl_file: str, log_file: str) -> None:
        self.chip_file = chip_file
        self.sl_file = sl_file
        self.log_file = log_file
        self.chip_data = self.load_json(self.chip_file)
        self.sl_data = self.load_json(self.sl_file)
        self.die_objects = {}
        self.die2die = Component(None, D2D)
        self.host_interface = self.load_host_interface()
        self.filter_factory = filter_factory_module.FilterFactory(LOGS_CSV)
        self.logs_factory = logs_factory.LogsFactory(LOGS_CSV)

    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Loads data from a JSON file and returns it as a dictionary.
        """
        try:
            with open(filename, READ) as config:
                return json.load(config)
        except FileNotFoundError:
            raise FileNotFoundError(ErrorMessages.ERROR.value,
                                    ErrorMessages.FILE_NOT_FOUND.value.format(filename=filename))
        except json.JSONDecodeError as e:
            raise ValueError(ErrorMessages.ERROR.value,
                             ErrorMessages.JSON_NOT_VALID.value.format(filename=filename, error=e))

    def load_die(self, die_index: int) -> Die:
        """
        Load a die object by index
        """
        # Validate the die_index
        dies_data = self.chip_data.get(TOP)
        if dies_data is None or DIES not in dies_data or die_index >= len(dies_data[DIES]):
            raise KeyError(WarningMessages.INVALID_DATA.value.format(component=DIE, data=die_index))

        # Retrieve or create the die object
        if die_index not in self.die_objects:
            die_data = dies_data[DIES][die_index]

            # Create a new Die object
            self.die_objects[die_index] = Die(die_data.get(ID, None), die_data)

            # Check if all dies are loaded, and if so, enable widgets and link logs
            if len(self.die_objects) == NUM_DIES:
                self.enable_widgets()
                self.link_the_logs_to_leaf_objects()

        return self.die_objects[die_index]

    def load_host_interface(self) -> HostInterface:
        """
        Load the host interface data
        """
        host_interface_data = self.chip_data.get(TOP)

        if host_interface_data is None or HOST_INTERFACE not in host_interface_data:
            raise KeyError(
                WarningMessages.INVALID_DATA.value.format(component=HOST_INTERFACE, data=host_interface_data))

        # Retrieve the host interface data
        host_interface_data = host_interface_data[HOST_INTERFACE]

        if not host_interface_data:
            raise ValueError(
                WarningMessages.INVALID_DATA.value.format(component=HOST_INTERFACE, data=host_interface_data))

        # Create the HostInterface object
        self.host_interface = HostInterface(host_interface_data)

        return self.host_interface

    def link_the_logs_to_leaf_objects(self) -> None:
        """
        Link logs to the corresponding leaf objects
        """
        try:
            self.filter_factory.start_logs()
            while not self.filter_factory.is_finished_process() or self.filter_factory.has_log():
                if self.filter_factory.has_log():
                    log = self.filter_factory.get_log()
                    print(
                        f"{TIMESTAMP}:{log.timeStamp},{CLUSTER_ID}:{CHIP}:{log.clusterId.chip},{DIE}:{log.clusterId.die},{QUAD}{log.clusterId.quad},{ROW}:{log.clusterId.row},{COL}:{log.clusterId.col},{AREA}:{log.area},{UNIT}:{log.unit},{IO}:{log.io},{TID}:{log.tid},{PACKET}:{log.packet}")
                    self.link_the_log_to_leaf_object(log)
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
        finally:
            self.filter_factory.join_thread()

    def link_the_log_to_leaf_object(self, log) -> None:
        """
        Link a single log to the corresponding leaf object
        """
        area = AREAS.get(log.area)
        # Separation sign between a unit and its number - ;
        sep_sign = ";"
        unit = list(log.unit.split(sep_sign))
        cluster_id = log.clusterId
        if (area == BMT and cluster_id.row == -1) or area == PCIE:
            self._add_log_to_host_interface(area, log)
        elif area == HOST_INTERFACE:
            self._add_log_to_host_interface_unit(unit, log)
        elif area == D2D:
            self.die2die.active_logs.append(log)
        else:
            self._add_log_to_die_area(area, unit, cluster_id, log)

    def _add_log_to_host_interface(self, area, log) -> None:
        """
        Add log to the host interface
        """
        getattr(self.host_interface, area).active_logs.append(log)

    def _add_log_to_host_interface_unit(self, unit, log) -> None:
        """
        Add log to a specific unit of the host interface
        """
        eq_count = 0
        for detail in self.host_interface.get_all_inner_details():
            if detail.type_name != unit[0]: continue
            if detail.type_name == EQ:
                eq_count += 1
                num_of_unit = int(unit[1])
                if num_of_unit != eq_count: continue
            detail.active_logs.append(log)
            break

    def _add_log_to_die_area(self, area, unit, cluster_id, log) -> None:
        """
        Add log to the die area
        """
        die = self.die_objects[cluster_id.die]
        quad = die.quads[cluster_id.quad // NUM_QUADS_PER_SIDE][cluster_id.quad % NUM_QUADS_PER_SIDE]
        if area == HBM:
            quad.hbm.active_logs.append(log)
        else:
            self._add_log_to_cluster(area, unit, quad, cluster_id, log)

    def _add_log_to_cluster(self, area, unit, quad, cluster_id, log) -> None:
        """
        Add log to a specific cluster
        """
        cluster = quad.clusters[cluster_id.row][cluster_id.col]
        if area == MCU:
            self._add_log_to_mcu(unit, cluster, log)
        else:
            self._add_log_to_ecore_or_other(unit, cluster, log)

    def _add_log_to_mcu(self, unit, cluster, log) -> None:
        """
        Add log to the MCU
        """
        eq_count = 0
        for detail in cluster.mcu.get_details():
            if detail.type_name != unit[0]: continue
            if detail.type_name == EQ:
                eq_count += 1
                num_of_unit = int(unit[1])
                if num_of_unit != eq_count: continue
            detail.active_logs.append(log)
            break

    def _add_log_to_ecore_or_other(self, unit, cluster, log) -> None:
        """
        Add log to ECORE or other types
        """
        ecore_count = 0
        for detail in cluster.get_details():
            if detail.type_name != unit[0]: continue
            if detail.type_name == ECORE:
                ecore_count += 1
                num_of_unit = int(unit[1])
                if num_of_unit != ecore_count: continue
            detail.active_logs.append(log)
            break

    def enable_widgets(self) -> None:
        """
        Enables the widgets by sl json file.
        """
        enabled_clusters = self.sl_data.get(ENABLED_CLUSTERS, [])
        if not enabled_clusters:
            raise KeyError(WarningMessages.WARNING.value,
                           WarningMessages.INVALID_DATA.value.format(component=ENABLED_CLUSTERS, data=self.sl_data))

        for id in enabled_clusters:
            if ID not in id:
                raise KeyError(WarningMessages.WARNING.value,
                               WarningMessages.INVALID_DATA.value.format(component=ID, data=enabled_clusters))
            self.enable_widget_by_id(id[ID])

        self.enable_die()

    def enable_widget_by_id(self, id: Dict[str, int]) -> None:
        """
        Enables a specific widget identified by its ID.
        """
        try:
            col, did, quad, row = id[COL], id[DID], id[QUAD], id[ROW]
        except KeyError as e:
            raise KeyError(WarningMessages.WARNING.value,
                           WarningMessages.WARNING_MISSING_DATA.value.format(component=ID))
        if did not in self.die_objects:
            raise IndexError(ErrorMessages.ERROR.value,
                             ErrorMessages.INDEX_OUT_OF_RANGE.value.format(index=str(did), object=self.die_objects))
        try:
            current_quad = self.die_objects[did].quads[quad // NUM_QUADS_PER_SIDE][quad % NUM_QUADS_PER_SIDE]
        except IndexError:
            raise IndexError(ErrorMessages.ERROR.value,
                             ErrorMessages.INDEX_OUT_OF_RANGE.value.format(index=str(quad), object=DIE))
        if row >= len(current_quad.clusters) or col >= len(current_quad.clusters[row]):
            raise IndexError(ErrorMessages.ERROR.value,
                             ErrorMessages.INDEX_OUT_OF_RANGE.value.format(index=f"{row},{col}", object=CLUSTER))
        current_quad.clusters[row][col].is_enable = True
        current_quad.is_enable = True

    def enable_die(self) -> None:
        """
        Enables the die based on its quadrants.
        """
        for die in self.die_objects.values():
            die.is_enable = any(quad and quad.is_enable for row in die.quads for quad in row)

    def get_start_time(self) -> datetime.datetime:
        """
        Returns the start time from logs as a datetime object.
        """
        try:
            start_time = self.logs_factory.get_first_log_time()
            start_time_converted = datetime.datetime.fromtimestamp(start_time)
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
        return start_time_converted

    def get_end_time(self) -> datetime.datetime:
        """
         Returns the end time from logs as a datetime object.
        """
        try:
            end_time = self.logs_factory.get_last_log_time()
            end_time_converted = datetime.datetime.fromtimestamp(end_time)  # Convert timestamp
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
        return end_time_converted

    def update_filter_in_chain(self, filter_type: str, values: List[Any]) -> None:
        """
        Changes the filter based on the filter name and values.
        """
        if filter_type in FILTER_TYPES_NAMES.values():
            try:
                if filter_type == FILTER_TYPES_NAMES[CLUSTER]:
                    cluster = filter_factory_module.Cluster(values[0], values[1], values[2], values[3], values[4])
                    self.filter_factory.update_filter_in_chain((filter_type, cluster))
                else:
                    print(filter_type, values)
                    self.filter_factory.update_filter_in_chain((filter_type, values))

                self.clean_the_prev_logs_from_leaf_objects()
                self.link_the_logs_to_leaf_objects()
            except ValueError as e:
                raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
        else:
            raise ValueError(WarningMessages.WARNING.value,
                             WarningMessages.UNKNOWN_FILTER.value.format(filter_type=filter_type))

    def change_filter(self, filter_type: str, values: List[Any]) -> None:
        """
        Changes the filter based on the filter name and values.
        """
        if filter_type in FILTER_TYPES_NAMES.values():
            try:
                if filter_type == FILTER_TYPES_NAMES[CLUSTER]:
                    cluster = filter_factory_module.Cluster(values[0], values[1], values[2], values[3], values[4])
                    self.filter_factory.add_filter_to_chain((filter_type, cluster))
                else:
                    self.filter_factory.add_filter_to_chain((filter_type, values))
                self.clean_the_prev_logs_from_leaf_objects()
                self.link_the_logs_to_leaf_objects()
            except ValueError as e:
                raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
        else:
            raise ValueError(WarningMessages.WARNING.value,
                             WarningMessages.UNKNOWN_FILTER.value.format(filter_type=filter_type))

    def clean_the_prev_logs_from_leaf_objects(self) -> None:
        """
        Cleans the previous logs from all leaf objects before connecting new logs.
        """
        # Clean logs from each leaf in the inner layers of die objects
        for die in self.die_objects.values():
            for quad in (quad for row in die.quads for quad in row if quad):
                quad.hbm.active_logs = []
                for cluster in (cluster for row in quad.clusters for cluster in row):
                    for detail in cluster.get_all_inner_details():
                        detail.active_logs = []

        # Clean logs from host interface
        for detail in self.host_interface.get_all_inner_details():
            detail.active_logs = []

        # Clean die2die logs
        self.die2die.active_logs = []

    def refresh_logs(self):
        """
        Cleaning the previous logs and linking the new logs to the leafs
        """
        self.clean_the_prev_logs_from_leaf_objects()
        self.link_the_logs_to_leaf_objects()

    def change_time(self, start_time: datetime.datetime, end_time: datetime.datetime) -> None:
        """
        Changes the start and end time for log filtering.
        """
        try:
            self.filter_factory.set_start_time(start_time)
            self.filter_factory.set_end_time(end_time)
            self.refresh_logs()
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))

    def clear_all_filters(self) -> None:
        """
        Clears all filters and resets the logs.
        """
        try:
            self.filter_factory.clear_filters()
            self.refresh_logs()
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))

    def filter_removal(self, filter_type: str) -> None:
        """
        Removes a specific filter and resets the logs.
        """
        try:
            self.filter_factory.remove_filter(filter_type)
            self.refresh_logs()
        except ValueError as e:
            raise ValueError(ErrorMessages.ERROR_OCCURRED.value.fomramt(error=str(e)))
