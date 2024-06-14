TELEMETRY_NAMESPACE_TAG_TRACER = "tracers"
TELEMETRY_NAMESPACE_TAG_APPSEC = "appsec"
TELEMETRY_NAMESPACE_TAG_IAST = "iast"

TELEMETRY_TYPE_GENERATE_METRICS = "generate-metrics"
TELEMETRY_TYPE_DISTRIBUTION = "distributions"
TELEMETRY_TYPE_LOGS = "logs"

# Configuration names must map to values supported by backend services:
# https://github.com/DataDog/dd-go/blob/f88e85d64b173e7733ac03e23576d1c9be37f32e/trace/apps/tracer-telemetry-intake/telemetry-payload/static/config_norm_rules.json
TELEMETRY_DYNAMIC_INSTRUMENTATION_ENABLED = "DD_DYNAMIC_INSTRUMENTATION_ENABLED"
TELEMETRY_EXCEPTION_DEBUGGING_ENABLED = "DD_EXCEPTION_DEBUGGING_ENABLED"


# Tracing Features

TELEMETRY_TRACE_DEBUG = "DD_TRACE_DEBUG"
TELEMETRY_ANALYTICS_ENABLED = "DD_TRACE_ANALYTICS_ENABLED"
TELEMETRY_STARTUP_LOGS_ENABLED = "DD_TRACE_STARTUP_LOGS"
TELEMETRY_CLIENT_IP_ENABLED = "DD_TRACE_CLIENT_IP_ENABLED"
TELEMETRY_128_BIT_TRACEID_GENERATION_ENABLED = "DD_TRACE_128_BIT_TRACEID_GENERATION_ENABLED"
TELEMETRY_128_BIT_TRACEID_LOGGING_ENABLED = "DD_TRACE_128_BIT_TRACEID_LOGGING_ENABLED"
TELEMETRY_TRACE_COMPUTE_STATS = "DD_TRACE_COMPUTE_STATS"
TELEMETRY_OBFUSCATION_QUERY_STRING_PATTERN = "DD_TRACE_OBFUSCATION_QUERY_STRING_REGEXP"
TELEMETRY_OTEL_ENABLED = "DD_TRACE_OTEL_ENABLED"
TELEMETRY_TRACE_HEALTH_METRICS_ENABLED = "DD_TRACE_HEALTH_METRICS_ENABLED"
TELEMETRY_ENABLED = "DD_INSTRUMENTATION_TELEMETRY_ENABLED"
TELEMETRY_RUNTIMEMETRICS_ENABLED = "DD_RUNTIME_METRICS_ENABLED"
TELEMETRY_REMOTE_CONFIGURATION_ENABLED = "DD_REMOTE_CONFIGURATION_ENABLED"
TELEMETRY_REMOTE_CONFIGURATION_INTERVAL = "DD_REMOTE_CONFIG_POLL_INTERVAL_SECONDS"
TELEMETRY_SERVICE_MAPPING = "DD_SERVICE_MAPPING"
TELEMETRY_SPAN_SAMPLING_RULES = "DD_SPAN_SAMPLING_RULES"
TELEMETRY_SPAN_SAMPLING_RULES_FILE = "DD_SPAN_SAMPLING_RULES_FILE"
TELEMETRY_PROPAGATION_STYLE_INJECT = "DD_TRACE_PROPAGATION_STYLE_INJECT"
TELEMETRY_PROPAGATION_STYLE_EXTRACT = "DD_TRACE_PROPAGATION_STYLE_EXTRACT"
TELEMETRY_TRACE_SAMPLING_RULES = "DD_TRACE_SAMPLING_RULES"
TELEMETRY_TRACE_SAMPLING_LIMIT = "DD_TRACE_RATE_LIMIT"
TELEMETRY_PRIORITY_SAMPLING = "DD_PRIORITY_SAMPLING"
TELEMETRY_PARTIAL_FLUSH_ENABLED = "DD_TRACE_PARTIAL_FLUSH_ENABLED"
TELEMETRY_PARTIAL_FLUSH_MIN_SPANS = "DD_TRACE_PARTIAL_FLUSH_MIN_SPANS"
TELEMETRY_TRACE_SPAN_ATTRIBUTE_SCHEMA = "DD_TRACE_SPAN_ATTRIBUTE_SCHEMA"
TELEMETRY_TRACE_REMOVE_INTEGRATION_SERVICE_NAMES_ENABLED = "DD_TRACE_REMOVE_INTEGRATION_SERVICE_NAMES_ENABLED"
TELEMETRY_TRACE_PEER_SERVICE_DEFAULTS_ENABLED = "DD_TRACE_PEER_SERVICE_DEFAULTS_ENABLED"
TELEMETRY_TRACE_PEER_SERVICE_MAPPING = "DD_TRACE_PEER_SERVICE_MAPPING"

TELEMETRY_TRACE_API_VERSION = "DD_TRACE_API_VERSION"
TELEMETRY_TRACE_WRITER_BUFFER_SIZE_BYTES = "DD_TRACE_WRITER_BUFFER_SIZE_BYTES"
TELEMETRY_TRACE_WRITER_MAX_PAYLOAD_SIZE_BYTES = "DD_TRACE_WRITER_MAX_PAYLOAD_SIZE_BYTES"
TELEMETRY_TRACE_WRITER_INTERVAL_SECONDS = "DD_TRACE_WRITER_INTERVAL_SECONDS"
TELEMETRY_TRACE_WRITER_REUSE_CONNECTIONS = "DD_TRACE_WRITER_REUSE_CONNECTIONS"

TELEMETRY_DOGSTATSD_PORT = "DD_DOGSTATSD_PORT"
TELEMETRY_DOGSTATSD_URL = "DD_DOGSTATSD_URL"

TELEMETRY_AGENT_HOST = "DD_AGENT_HOST"
TELEMETRY_AGENT_PORT = "DD_AGENT_PORT"
TELEMETRY_AGENT_URL = "DD_TRACE_AGENT_URL"
TELEMETRY_TRACE_AGENT_TIMEOUT_SECONDS = "DD_TRACE_AGENT_TIMEOUT_SECONDS"

# Profiling features
TELEMETRY_PROFILING_STACK_ENABLED = "DD_PROFILING_STACK_ENABLED"
TELEMETRY_PROFILING_MEMORY_ENABLED = "DD_PROFILING_MEMORY_ENABLED"
TELEMETRY_PROFILING_HEAP_ENABLED = "DD_PROFILING_HEAP_ENABLED"
TELEMETRY_PROFILING_LOCK_ENABLED = "DD_PROFILING_LOCK_ENABLED"
TELEMETRY_PROFILING_EXPORT_LIBDD_ENABLED = "DD_PROFILING_EXPORT_LIBDD_ENABLED"
TELEMETRY_PROFILING_CAPTURE_PCT = "DD_PROFILING_CAPTURE_PCT"
TELEMETRY_PROFILING_UPLOAD_INTERVAL = "DD_PROFILING_UPLOAD_INTERVAL"
TELEMETRY_PROFILING_MAX_FRAMES = "DD_PROFILING_MAX_FRAMES"

TELEMETRY_INJECT_WAS_ATTEMPTED = "DD_LIB_INJECTION_ATTEMPTED"
TELEMETRY_LIB_WAS_INJECTED = "DD_LIB_INJECTED"
TELEMETRY_LIB_INJECTION_FORCED = "DD_INJECT_FORCE"
