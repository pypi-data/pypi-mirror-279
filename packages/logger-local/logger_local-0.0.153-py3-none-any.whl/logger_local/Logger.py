# backword compatibility
import inspect
import warnings
from .LoggerLocal import Logger  # noqa

# TODO: move elsewhere
printed = False
if not printed:
    warnings_message = "Please use LoggerLocal instead of Logger."
    try:
        warnings_message += " Called from: " + inspect.stack()[1].filename
    except Exception:
        pass
    warnings.warn(warnings_message, DeprecationWarning)
    printed = True
