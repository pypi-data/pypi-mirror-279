"""Responses"""

from typing import List, Self

from .classes import Route, Waypoint


class TripResponse:
  """OSRM Trip response object"""

  def __init__(self: Self, trips: List[Route], waypoints: List[Waypoint]) -> None:
    """
    Trip Response

    Args:
    - trips: List of trips
    - waypoints: List of waypoints
    """
    self.trips = trips
    self.waypoints = waypoints


class NearestResponse:
  """OSRM Nearest response object"""

  def __init__(self: Self, waypoints: List[Waypoint]) -> None:
    """
    Nearest Response

    Args:
    - waypoints: List of waypoints
    """
    self.waypoints = waypoints


class RouteResponse:
  """OSRM Route response object"""

  def __init__(self: Self, routes: List[Route], waypoints: List[Waypoint]) -> None:
    """
    Route Response

    Args:
    - routes: List of routes
    - waypoints: List of waypoints
    """
    self.routes = routes
    self.waypoints = waypoints


class MatchResponse:
  """OSRM Match response object"""

  def __init__(self: Self, matchings: List[Route], waypoints: List[Waypoint]) -> None:
    """
    Match Response

    Args:
    - matchings: List of matchings
    - waypoints: List of waypoints
    """
    self.matchings = matchings
    self.waypoints = waypoints
