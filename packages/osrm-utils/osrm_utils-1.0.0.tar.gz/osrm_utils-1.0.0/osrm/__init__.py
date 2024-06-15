"""OSRM Python API"""

import logging
from typing import Dict, List, Tuple

import requests

from .classes import (
  Intersection,
  Lane,
  Point,
  Route,
  RouteLeg,
  RouteStep,
  StepManeuver,
  Waypoint,
)
from .enums import Annotation, Gap, Indication, ManeuverType, Overview, PointFix
from .exceptions import OsrmException
from .responses import MatchResponse, NearestResponse, RouteResponse, TripResponse

log = logging.getLogger(__name__)


class Osrm:
  """
  OSRM Client
  ---
  Services:
  - trip
  - route
  - match
  - nearest

  Services not implemented:
  - table
  - tile
  """

  def __init__(
    self,
    base_url: str = 'http://router.project-osrm.org',
    timeout: float = 30,
  ) -> None:
    """
    Initialize OSRM client

    Args:
    - base_url: the base URL of the OSRM server (default: 'http://router.project-osrm.org')
    - timeout: the request timeout in seconds (default: 30)
    """
    self.base_url = base_url
    self.timeout = timeout
    log.debug('Initializing OSRM client with base URL %s', base_url)

  def nearest(
    self,
    point: Point,
    profile: str = 'driving',
    return_elements: int = 1,
  ) -> NearestResponse:
    """
    Nearest service
    Snaps a coordinate to the street network and returns the nearest {return_elements} matches.
    More info on https://project-osrm.org/docs/v5.24.0/api/#nearest-service

    Args:
    - point: the point to snap
    - profile: the profile to use (default: 'driving')
    - return_elements: the number of elements to return (default: 1)
    """
    url = f'{self.base_url}/nearest/v1/{profile}/{point.longitude},{point.latitude}.json'
    with requests.get(url, params={'number': return_elements}, timeout=self.timeout) as response:
      log.debug('Response status code: %s', response.status_code)
      if response.status_code != 200:
        raise OsrmException(f'OSRM request failed with status code {response.status_code} and message {response.text}')
      log.debug('Requested URL: %s', response.url)
      data = response.json()

    waypoints = []

    for waypoint in data.get('waypoints', []):
      waypoints.append(
        Waypoint(
          name=waypoint.get('name'),
          location=Point(
            latitude=waypoint['location'][1],
            longitude=waypoint['location'][0],
          ),
          distance=waypoint.get('distance') or 0.0,
        )
      )

    return NearestResponse(waypoints=waypoints)

  def route(
    self,
    points: List[Point],
    alternatives: int = 0,
    profile: str = 'driving',
    steps: bool = False,
    annotations: List[Annotation] = None,
    overview: Overview = Overview.SIMPLIFIED,
    continue_straight: bool = False,
  ) -> RouteResponse:
    """
    Route service
    Returns the fastest route between the given waypoints.
    More info on https://project-osrm.org/docs/v5.24.0/api/#route-service

    Args:
    - points: the waypoints to route
    - alternatives: the number of alternative routes to return (default: 0)
    - profile: the profile to use (default: 'driving')
    - steps: return route steps (default: False)
    - annotations: return annotations (default: [])
    - overview: the route overview (default: 'simplified')
    - continue_straight: continue straight at waypoints (default: False)

    Raises:
    - ValueError: if alternatives is less than 0
    """
    if alternatives < 0:
      raise ValueError('Alternatives must be greater than or equal to 0')

    base_url = f'{self.base_url}/route/v1/{profile}/'
    coordinates = ';'.join([f'{point.longitude},{point.latitude}' for point in points])
    if annotations is None:
      annotations = []

    url = f'{base_url}{coordinates}.json'
    params = {
      'alternatives': alternatives if alternatives > 0 else 'false',
      'steps': 'true' if steps else 'false',
      'annotations': ','.join([str(annotation) for annotation in annotations]) if len(annotations) > 0 else 'false',
      'overview': overview.value,
      'continue_straight': 'true' if continue_straight else 'false',
    }

    with requests.get(url, params=params, timeout=self.timeout) as response:
      log.debug('Response status code: %s', response.status_code)
      if response.status_code != 200:
        raise OsrmException(f'OSRM request failed with status code {response.status_code} and message {response.text}')
      log.debug('Requested URL: %s', response.url)
      data = response.json()

    routes, waypoints = self._process_routes_and_waypoints(
      data=data,
      route_key='routes',
      waypoint_key='waypoints',
    )
    return RouteResponse(routes=routes, waypoints=waypoints)

  def match(
    self,
    points: List[Point],
    profile: str = 'driving',
    steps: bool = False,
    annotations: List[Annotation] = None,
    overview: Overview = Overview.SIMPLIFIED,
    tidy: bool = False,
    timestmaps: List[int] = None,
    radiuses: List[int] = None,
    gaps: Gap = Gap.SPLIT,
  ) -> None:
    """
    Match service
    Snaps noisy GPS traces to the road network in the most plausible way. This can also be used to match other
    transportation networks.
    More info on https://project-osrm.org/docs/v5.24.0/api/#match-service

    Args:
    - points: the points to match
    - profile: the profile to use (default: 'driving')
    - steps: return route steps (default: False)
    - annotations: return annotations (default: [])
    - overview: the route overview (default: 'simplified')
    - tidy: remove waypoints which are not part of the route (default: False)
    - timestmaps: timestamps for the points
    - radiuses: search radiuses for each point
    - gaps: the gap between points
    """
    if annotations is None:
      annotations = []

    base_url = f'{self.base_url}/match/v1/{profile}/'
    coordinates = ';'.join([f'{point.longitude},{point.latitude}' for point in points])
    url = f'{base_url}{coordinates}.json'
    params = {
      'steps': 'true' if steps else 'false',
      'annotations': ','.join([str(annotation) for annotation in annotations]) if len(annotations) > 0 else 'false',
      'overview': overview.value,
      'tidy': 'true' if tidy else 'false',
      'gaps': gaps.value,
    }

    if timestmaps is not None and len(timestmaps) > 0:
      params['timestamps'] = ';'.join([str(timestamp) for timestamp in timestmaps])

    if radiuses is not None and len(radiuses) > 0:
      params['radiuses'] = ';'.join([str(radius) for radius in radiuses])

    with requests.get(url, params=params, timeout=self.timeout) as response:
      log.debug('Response status code: %s', response.status_code)
      if response.status_code != 200:
        raise OsrmException(f'OSRM request failed with status code {response.status_code} and message {response.text}')
      log.debug('Requested URL: %s', response.url)
      data = response.json()

    tracepoints, matchings = self._process_routes_and_waypoints(
      data=data,
      route_key='matchings',
      waypoint_key='tracepoints',
    )

    return MatchResponse(matchings=matchings, waypoints=tracepoints)

  def trip(
    self,
    points: List[Point],
    profile: str = 'driving',
    source: PointFix = PointFix.FIRST_POINT,
    destination: PointFix = PointFix.LAST_POINT,
    steps: bool = False,
    annotations: List[Annotation] = None,
    overview: Overview = Overview.SIMPLIFIED,
    roundtrip: bool = False,
  ) -> TripResponse:
    if annotations is None:
      annotations = []

    base_url = f'{self.base_url}/trip/v1/{profile}/'
    coordinates = ';'.join([f'{point.longitude},{point.latitude}' for point in points])

    params = {
      'steps': 'true' if steps else 'false',
      'annotations': ','.join([str(annotation) for annotation in annotations]) if len(annotations) > 0 else 'false',
      'overview': overview.value,
      'source': source.value,
      'destination': destination.value,
      'roundtrip': 'true' if roundtrip else 'false',
    }

    url = f'{base_url}{coordinates}.json'

    with requests.get(url, params=params, timeout=self.timeout) as response:
      log.debug('Response status code: %s', response.status_code)
      if response.status_code != 200:
        raise OsrmException(f'OSRM request failed with status code {response.status_code} and message {response.text}')
      log.debug('Requested URL: %s', response.url)
      data = response.json()

    trips, waypoints = self._process_routes_and_waypoints(
      data=data,
      route_key='trips',
      waypoint_key='waypoints',
    )
    return TripResponse(trips=trips, waypoints=waypoints)

  def _process_routes_and_waypoints(
    self,
    data: Dict,
    route_key: str,
    waypoint_key: str,
  ) -> Tuple[List[Route], List[Waypoint]]:
    """Process trips or routes"""
    trips: List[Route] = []
    for trip in data.get(route_key, []):
      legs: List[RouteStep] = []

      for leg in trip.get('legs', []):
        steps: List[RouteStep] = []

        for step in leg.get('steps', []):
          intersections: List[Intersection] = []

          for intersection in step.get('intersections', []):
            intersections.append(
              Intersection(
                location=Point(
                  latitude=intersection['location'][1],
                  longitude=intersection['location'][0],
                ),
                bearings=intersection.get('bearings'),
                entry=intersection.get('entry'),
                in_index=intersection.get('in'),
                out_index=intersection.get('out'),
                lanes=[
                  Lane(
                    indications=lane['indications'],
                    valid=lane['valid'],
                  )
                  for lane in intersection.get('lanes', [])
                ],
              )
            )

          steps.append(
            RouteStep(
              maneuver=StepManeuver(
                bearing_after=step['maneuver']['bearing_after'],
                bearing_before=step['maneuver']['bearing_before'],
                location=Point(
                  latitude=step['maneuver']['location'][1],
                  longitude=step['maneuver']['location'][0],
                ),
                modifier=step['maneuver'].get('modifier'),
                maneuver_type=step['maneuver']['type'],
              ),
              driving_side=step.get('driving_side'),
              mode=step.get('mode'),
              weight=step.get('weight') or 0.0,
              distance=step.get('distance') or 0.0,
              duration=step.get('duration') or 0.0,
              name=step.get('name'),
              ref=step.get('ref'),
              exits=step.get('exits'),
              intersections=intersections,
            )
          )

        legs.append(
          RouteLeg(
            summary=leg['summary'],
            steps=steps,
            weight=leg.get('weight') or 0.0,
            distance=leg.get('distance') or 0.0,
            duration=leg.get('duration') or 0.0,
          )
        )

      trips.append(
        Route(
          geometry=trip['geometry'],
          legs=legs,
          weight_name=trip.get('weight_name') or '',
          weight=trip.get('weight') or 0.0,
          distance=trip.get('distance') or 0.0,
          duration=trip.get('duration') or 0.0,
        )
      )

    waypoints: List[Waypoint] = []

    for waypoint in data.get(waypoint_key, []):
      waypoints.append(
        Waypoint(
          name=waypoint.get('name'),
          location=Point(
            latitude=waypoint['location'][1],
            longitude=waypoint['location'][0],
          ),
          distance=waypoint.get('distance') or 0.0,
          hint=waypoint.get('hint'),
          waypoint_index=waypoint.get('waypoint_index'),
          matchings_index=waypoint.get('matchings_index'),
          alternatives_count=waypoint.get('alternatives_count'),
        )
      )

    return trips, waypoints
