"""
A module that contains all the types used in this project
"""

import platform

python_version = list(platform.python_version_tuple())
SUPPORT_ADD_NOTES = int(python_version[0]) >= 3 and int(python_version[1]) >= 11


class ChatbotError(Exception):
    """
    Base class for all Chatbot errors in this Project
    """

    def __init__(self, *args: object) -> None:
        if SUPPORT_ADD_NOTES:
            super().add_note(
                "Please check that the input is correct, or you can resolve this issue by filing an issue",
            )
            super().add_note("Project URL: https://github.com/acheong08/ChatGPT")
        super().__init__(*args)


class ActionError(ChatbotError):
    """
    Subclass of ChatbotError

    An object that throws an error because the execution of an operation is blocked
    """

    def __init__(self, *args: object) -> None:
        if SUPPORT_ADD_NOTES:
            super().add_note(
                "The current operation is not allowed, which may be intentional",
            )
        super().__init__(*args)


class ActionNotAllowedError(ActionError):
    """
    Subclass of ActionError

    An object that throws an error because the execution of an unalloyed operation is blocked
    """


class APIConnectionError(ChatbotError):
    """
    Subclass of ChatbotError

    An exception object thrown when an API connection fails or fails to connect due to network or
    other miscellaneous reasons
    """

    def __init__(self, *args: object) -> None:
        if SUPPORT_ADD_NOTES:
            super().add_note(
                "Please check if there is a problem with your network connection",
            )
        super().__init__(*args)


class NotAllowRunning(ActionNotAllowedError):
    """
    Subclass of ActionNotAllowedError

    Direct startup is not allowed for some reason
    """


class ResponseError(APIConnectionError):
    """
    Subclass of APIConnectionError

    Error objects caused by API request errors due to network or other miscellaneous reasons
    """
