# Standard Library Imports
from dataclasses import dataclass


@dataclass
class MessageException(Exception):
    message: str

    def __str__(self):
        return self.message


@dataclass
class CapicheException(Exception):
    pass


class QueueFullException(CapicheException, MessageException):
    message = "Queue is full. Please try again later"
