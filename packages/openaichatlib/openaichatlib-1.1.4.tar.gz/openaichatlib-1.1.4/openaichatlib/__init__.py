# coding=utf-8
from .version import version

__version__ = version
__all__ = ()


def verify() -> None:
    # Available Python Version Verify
    from . import typings as t

    if int(__import__("platform").python_version_tuple()[0]) < 3:
        error = t.NotAllowRunning("Not available Python version")
        raise error
    if int(__import__("platform").python_version_tuple()[1]) < 9:
        error = t.NotAllowRunning(
            f"Not available Python version: {__import__('platform').python_version()}",
        )
        raise error
    if (
            int(__import__("platform").python_version_tuple()[1]) < 10
            and int(__import__("platform").python_version_tuple()[0]) == 3
    ):
        __import__("warnings").warn(
            UserWarning(
                "The current Python is not a recommended version, 3.10+ is recommended",
            ),
        )


verify()
