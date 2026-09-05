class PipelineError(Exception):
    """Base class for every failure raised by this project."""

class ConfigError(PipelineError):
    """Raised when the pipeline's configuration is invalid or incomplete
        (e.g. a required input directory or file is missing)."""

class ValidationError(PipelineError):
    """Raised when a record violates the data contract and must not
        reach the output tables."""