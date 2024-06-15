"""OSRM Exceptions"""

from typing import Self


class OsrmException(Exception):
  """Base OSRM exception"""

  def __init__(self: Self, message: str) -> None:
    super().__init__(message)
    self.message = message

  def __str__(self: Self) -> str:
    return 'OsrmException: ' + self.message
