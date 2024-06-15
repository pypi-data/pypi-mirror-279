"""OSRM Exceptions"""


class OsrmException(Exception):
  """Base OSRM exception"""

  def __init__(self, message: str) -> None:
    super().__init__(message)
    self.message = message

  def __str__(self) -> str:
    return 'OsrmException: ' + self.message
