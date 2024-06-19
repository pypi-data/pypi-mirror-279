# backword compatibility
from .LoggerLocal import Logger  # noqa
import warnings

printed = False
if not printed:
    warnings.warn("Please use LoggerLocal instead of Logger", DeprecationWarning)
    printed = True
