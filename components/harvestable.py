from __future__ import annotations
from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from resource_types import ResourceType

if TYPE_CHECKING:
  from entity import Resource

class Harvestable(BaseComponent):
  parent: Resource

  def __init__(
      self,
      resource_type: ResourceType,
      capacity: int = 100
  ):
    self.resource_type = resource_type
    self.capacity = capacity

class Crystal(Harvestable):
  def __init__(self, capacity = 100) -> None:
    super().__init__(resource_type=ResourceType.CRYSTAL, capacity=capacity)