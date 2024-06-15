"""
This file contains the definitions of the types used in the snapctl package.
"""


class ResponseType():
    """
    This class represents the response type of the Snapser API.
    """
    error: bool
    msg: str
    data: list
