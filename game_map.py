from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor, Item, Resource
import tile_types

if TYPE_CHECKING:
  from engine import Engine
  from entity import Entity

class GameMap:
  def __init__(
      self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
  ):
    self.engine = engine
    self.width, self.height = width, height
    self.entities = set(entities)
    self.tiles = np.full((width, height), fill_value=tile_types.wall, order='F')
    
    self.visible = np.full(
      (width, height), fill_value=False, order='F'
    )
    self.explored = np.full(
      (width, height), fill_value=False, order='F'
    )

    self.downstairs_location = (0, 0)

  @property
  def gamemap(self) -> GameMap:
    return self

  @property
  def actors(self) -> Iterator[Actor]:
    yield from (
      entity
      for entity in self.entities
      if isinstance(entity, Actor) and entity.is_alive
    )

  @property
  def items(self) -> Iterator[Item]:
    yield from (entity for entity in self.entities if isinstance(entity, Item))

  @property
  def resources(self) -> Iterator[Resource]:
    yield from (entity for entity in self.entities if isinstance(entity, Resource))

  def get_blocking_entity_at_location(
      self, location_x: int, location_y: int
  ) -> Optional[Entity]:
    for entity in self.entities:
      if (
        entity.blocks_movement
        and entity.x == location_x
        and entity.y == location_y
      ):
        return entity
      
    return None
  
  #type lets you filter by subclass. lets see if this breaks shit lmao
  def get_actor_at_location(self, x: int, y: int, type: Actor = Actor) -> Optional[Actor]:
    for actor in self.actors:
      if actor.x == x and actor.y == y and isinstance(actor, type):
        return actor
      
    return None
  
  def get_resource_at_location(self, x: int, y: int) -> Optional[Resource]:
    for resource in self.resources:
      if resource.x == x and resource.y == y:
        return resource

  def in_bounds(self, x: int, y: int) -> bool:
    return 0 <= x < self.width and 0 <= y < self.height
  
  def render(self, console: Console) -> None:
    #old rendering, no FOV
    # console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['dark']
    console.rgb[0 : self.width, 0 : self.height] = np.select(
      condlist=[self.visible, self.explored],
      choicelist=[self.tiles['light'], self.tiles['dark']],
      default=tile_types.SHROUD,
    )
    
    entities_sorted_for_rendering = sorted(
      self.entities, key=lambda x: x.render_order.value
    )

    # for entity in self.entities:
    for entity in entities_sorted_for_rendering:
      if self.visible[entity.x, entity.y]:
        console.print(
          x=entity.x, y=entity.y, string=entity.char, fg=entity.color
        )
class GameWorld:
  def __init__(
      self,
      *,
      engine: Engine,
      map_width: int,
      map_height: int,
      max_rooms: int,
      room_min_size: int,
      room_max_size: int,
      # max_monsters_per_room: int,
      # max_items_per_room: int,
      current_floor: int = 0
  ):
    self.engine = engine

    self.map_width = map_width
    self.map_height = map_height

    self.max_rooms = max_rooms

    self.room_min_size = room_min_size
    self.room_max_size = room_max_size

    # self.max_monsters_per_room = max_monsters_per_room
    # self.max_items_per_room = max_items_per_room

    self.current_floor = current_floor

  def generate_test_level(self) -> None:
    from procgen import test_level

    self.engine.game_map = test_level(
      map_width=self.map_width,
      map_height=self.map_height,
      engine=self.engine,
    )

  #tutorial dungeon maps
  def generate_floor(self) -> None:
    from procgen import generate_dungeon

    self.current_floor += 1

    self.engine.game_map = generate_dungeon(
      max_rooms=self.max_rooms,
      room_min_size=self.room_min_size,
      room_max_size=self.room_max_size,
      map_width=self.map_width,
      map_height=self.map_height,
      # max_monsters_per_room=self.max_monsters_per_room,
      # max_items_per_room=self.max_items_per_room,
      engine=self.engine,
    )