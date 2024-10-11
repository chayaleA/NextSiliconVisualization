import filter_factory_module
filter_types = filter_factory_module.FilterType

TIME = "Time"
THREADID = "ThreadId"
CLUSTER = "Cluster"
TIMERANGE = "TimeRange"
IO = "Io"
QUAD = "Quad"
UNIT = "Unit"
AREA = "Area"

FILTER_TYPES_NAMES = {
    TIME: filter_types.Time.name,
    TIMERANGE: filter_types.TimeRange.name,
    QUAD: filter_types.Quad.name,
    CLUSTER: filter_types.Cluster.name,
    THREADID: filter_types.ThreadId.name,
    AREA: filter_types.Area.name,
    UNIT: filter_types.Unit.name,
    IO: filter_types.Io.name
}