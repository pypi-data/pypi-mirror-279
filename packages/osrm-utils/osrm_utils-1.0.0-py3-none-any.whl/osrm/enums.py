"""Annotations"""

from enum import Enum


class Annotation(Enum):
  """annotations"""

  NODES = 'nodes'
  DISTANCE = 'distance'
  DURATION = 'duration'
  WEIGHT = 'weight'
  DATA_SOURCES = 'datasources'
  SPEED = 'speed'

  def __str__(self) -> str:
    return self.value


class Overview(Enum):
  """overview"""

  SIMPLIFIED = 'simplified'
  FULL = 'full'
  NONE = 'false'

  def __str__(self) -> str:
    return self.value


class PointFix(Enum):
  """GeoPoint fix"""

  FIRST_POINT = 'first'
  LAST_POINT = 'last'
  ANY_POINT = 'any'

  def __str__(self) -> str:
    return self.value


class Indication(Enum):
  """Indication"""

  U_TURN = 'uturn'
  SHARP_RIGHT = 'sharp right'
  RIGHT = 'right'
  SLIGHT_RIGHT = 'slight right'
  STRAIGHT = 'straight'
  SLIGHT_LEFT = 'slight left'
  LEFT = 'left'
  SHARP_LEFT = 'sharp left'
  NONE = 'none'

  def __str__(self) -> str:
    return self.value


class ManeuverType(Enum):
  """Maneuver Type"""

  DEPART = 'depart'
  ARRIVE = 'arrive'
  ROUNDABOUT = 'roundabout'
  MERGE = 'merge'
  ON_RAMP = 'on ramp'
  OFF_RAMP = 'off ramp'
  FORK = 'fork'
  END_OF_ROAD = 'end of road'
  CONTINUE = 'continue'
  ROTARY = 'rotary'
  ROUNDABOUT_TURN = 'roundabout turn'
  ROUNDABOUT_EXIT = 'exit roundabout'
  NONE = 'none'
  TURN = 'turn'
  NEW_NAME = 'new name'

  def __str__(self) -> str:
    return self.value


class Gap(Enum):
  """Gap"""

  SPLIT = 'split'
  IGNORE = 'ignore'

  def __str__(self) -> str:
    return self.value
