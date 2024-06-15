"""OSRM Classes"""

from typing import Dict, List, Self, TypeVar

from .enums import Indication, ManeuverType

T = TypeVar('T', bound='Point')


class Point:
  """Geographic point"""

  def __init__(
    self: Self,
    latitude: float,
    longitude: float,
  ) -> None:
    """
    Point definition

    Args:
    - latitude: Latitude in degrees (between -90 and 90)
    - longitude: Longitude in degrees (between -180 and 180)

    Raises:
    - ValueError: If latitude or longitude are out of bounds
    """
    if not (-90 <= latitude <= 90):
      raise ValueError('Latitude must be between -90 and 90')

    if not (-180 <= longitude <= 180):
      raise ValueError('Longitude must be between -180 and 180')

    self.latitude = latitude
    self.longitude = longitude

  def __str__(self: Self) -> str:
    return f'GeoPoint(lat={self.latitude}, lng={self.longitude})'


class StepManeuver:
  """Step Maneuver"""

  def __init__(
    self: Self,
    bearing_after: float,
    bearing_before: float,
    location: Point,
    modifier: str = '',
    maneuver_type: str = '',
  ) -> None:
    """
    Step Maneuver

    Args:
    - bearing_after: Bearing after the maneuver
    - bearing_before: Bearing before the maneuver
    - location: Location of the maneuver
    - modifier: Modifier of the maneuver
    - maneuver_type: Type of the maneuver

    Raises:
    - ValueError: If bearing_after or bearing_before are out of bounds, or if location is not a Point, also, may raise
                  a value error if modifier or maneuver_type are not valid
    """
    if not (0 <= bearing_after <= 360):
      raise ValueError('Bearing after must be between 0 and 360')
    self.bearing_after = bearing_after

    if not (0 <= bearing_before <= 360):
      raise ValueError('Bearing before must be between 0 and 360')
    self.bearing_before = bearing_before

    if not isinstance(location, Point):
      raise ValueError('Location must be an instance of GeoPoint')
    self.location = location

    if modifier == '' or modifier is None:
      self.modifier = Indication.NONE
    else:
      self.modifier = Indication(modifier)

    if maneuver_type == '' or maneuver_type is None:
      self.maneuver_type = ManeuverType.NONE
    else:
      self.maneuver_type = ManeuverType(maneuver_type)

  def __str__(self: Self) -> str:
    return f'OsrmStepManeuver(location={self.location}, modifier={self.modifier}, type={self.maneuver_type})'


class Lane:
  """Lane"""

  def __init__(
    self: Self,
    indications: List[str],
    valid: bool,
  ) -> None:
    """
    OSRM Lane

    Args:
    - indications: Indications
    - valid: Validity of the lane

    Raises:
    - ValueError: If indications is not a list, or the values are not a valid OsrmIndication
    """
    self.valid = valid
    self.indications = []
    for indication in indications:
      self.indications.append(Indication(indication))


class Intersection:
  """Instersection"""

  def __init__(
    self: Self,
    location: Point,
    bearings: List[float],
    entry: List[bool],
    out_index: int | None = None,
    in_index: int | None = None,
    lanes: List[Lane] = None,
  ) -> None:
    """
    OSRM Intersection

    Args:
    - location: The location of the turn.
    - bearings: A list of bearing values (e.g. [0,90,180,270]) that are available at the intersection.
    - entry: A list of entry flags, corresponding in a 1:1 relationship to the bearings.
    - out_index: Index into bearings/entry array. Used to calculate the bearing just before the turn.
    - in_index: Index into the bearings/entry array. Used to extract the bearing just after the turn.
    - lanes: A list of Lane objects that denote the available turn lanes at the intersection.
    """
    self.location = location
    self.bearings = bearings
    self.entry = entry
    self.out_index = out_index
    self.in_index = in_index
    self.lanes = lanes

  def __str__(self: Self) -> str:
    return (
      f'OsrmIntersection(location={self.location}, bearings={self.bearings}, entry={self.entry}, '
      f'lanes={len(self.lanes)} lanes'
    )


class RouteStep:
  """Route Step"""

  def __init__(
    self: Self,
    maneuver: StepManeuver,
    intersections: List[Intersection],
    mode: str,
    driving_side: str,
    weight: float = 0.0,
    distance: float = 0.0,
    duration: float = 0.0,
    ref: str | None = None,
    name: str | None = None,
    destinations: str | None = None,
    exits: str | None = None,
  ) -> None:
    """
    OSRM Step

    Args:
    - maneuver: Maneuver
    - intersections: A list of Intersection objects that are passed along the segment.
    - mode: The mode of transportation
    - driving_side: The side of the road the step is taking place
    - weight: The weight of the step
    - distance: The distance of the step
    - duration: The duration of the step
    - ref: A reference number or code for the way.
    - name: The name of the way along which travel proceeds.
    - destinations: The destinations of the way.
    - exits: The exit numbers or names of the way.
    """

    self.maneuver = maneuver
    self.intersections = intersections
    self.mode = mode
    self.driving_side = driving_side
    self.weight = weight
    self.distance = distance
    self.duration = duration
    self.ref = ref
    self.destinations = destinations
    self.exits = exits

    if name is None or name == '':
      self.name = 'N/A'
    else:
      self.name = name

  def __str__(self: Self) -> str:
    name = self.name
    if len(name) > 10:
      name = f'{name[:10]}...'

    return (
      f'OsrmRouteStep(name={name}, intersections={len(self.intersections)} intersecs'
      f', weight={self.weight}, distance={self.distance}, duration={self.duration})'
    )


class RouteLeg:
  """Route Leg"""

  def __init__(
    self: Self,
    summary: str,
    steps: List[RouteStep],
    weight: float = 0.0,
    distance: float = 0.0,
    duration: float = 0.0,
  ) -> None:
    """
    Route Leg

    Args:
    - summary: Summary of the leg
    - steps: Steps of the leg
    - weight: Weight of the leg
    - distance: Distance of the leg
    - duration: Duration of the leg
    """
    self.summary = summary
    self.steps = steps
    self.weight = weight
    self.distance = distance
    self.duration = duration

  def __str__(self: Self) -> str:
    summary = self.summary
    if len(self.summary) > 10:
      summary = f'{self.summary[:10]}...'

    return (
      f'OsrmRouteLeg(summary={summary}, steps={len(self.steps)} steps, weight={self.weight}, '
      f'distance={self.distance}, duration={self.duration})'
    )


class Waypoint:
  """Waypoint"""

  def __init__(
    self: Self,
    name: str,
    location: Point,
    distance: float = 0.0,
    hint: str | None = None,
    waypoint_index: int | None = None,
    matchings_index: int | None = None,
    alternatives_count: int | None = None,
  ) -> None:
    """
    Waypoint

    Args:
    - name: Name of the waypoint
    - location: Location of the waypoint
    - distance: Distance of the waypoint
    - hint: Unique internal identifier of the segment (ephemeral, not constant over data updates) This can be used on
            subsequent request to significantly speed up the query and to connect multiple services.
    - waypoint_index: Index to the route object in the matchings array.
    - matchings_index: Index of the waypoint inside the matched route.
    - alternatives_count: Number of found alternative routes. If 0 the result was matched ambiguously.
    """
    self.name = name
    self.location = location
    self.distance = distance
    self.hint = hint
    self.waypoint_index = waypoint_index
    self.matchings_index = matchings_index
    self.alternatives_count = alternatives_count

  def __str__(self: Self) -> str:
    name = self.name
    if len(self.name) > 10:
      name = f'{self.name[:10]}...'

    return f'OsrmWaypoint(name={name}, location={self.location})'


class Route:
  """Route"""

  def __init__(
    self: Self,
    geometry: str,
    legs: List[RouteLeg],
    weight_name: str,
    weight: float = 0.0,
    distance: float = 0.0,
    duration: float = 0.0,
    condifence: float = 0.0,
  ) -> None:
    """
    Trip

    Args:
    - geometry: Geometry of the trip
    - legs: Legs of the trip
    - weight_name: Weight name
    - weight: Weight of the trip
    - distance: Distance of the trip
    - duration: Duration of the trip
    - condifence: Confidence of the trip. Default is 0.0 (Only will be filled in the match service)
    """
    self.geometry = geometry
    self.legs = legs
    self.weight_name = weight_name
    self.weight = weight
    self.distance = distance
    self.duration = duration
    self.condifence = condifence

  def __str__(self: Self) -> str:
    geometry = self.geometry
    if len(self.geometry) > 5:
      geometry = f'{self.geometry[:5]}...'

    return (
      f'OsrmTrip(geometry={geometry}, legs={len(self.legs)} legs, weight={self.weight}, '
      f'distance={self.distance}, duration={self.duration})'
    )
