import logging
from typing import Self


class ExtraFormatter(logging.Formatter):
    def format(self: Self, record: logging.LogRecord) -> str:
        # Original formatted message
        msg = super().format(record)

        # Append all extra attributes
        extras = []
        for key, value in record.__dict__.items():
            if key not in [
                "message",
                "asctime",
                "levelname",
                "levelno",
                "module",
                "args",
                "msg",
                "exc_text",
                "exc_info",
                "stack_info",
                "filename",
                "funcName",
                "lineno",
                "name",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "pathname",
                "processName",
                "process",
            ]:
                extras.append(f"{key}={value}")
        if extras:
            msg = f"{msg} [{', '.join(extras)}]"
        return msg
