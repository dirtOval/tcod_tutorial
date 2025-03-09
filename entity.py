from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from render_order import RenderOrder

if TYPE_CHECKING:
  from components.ai import BaseAI, SpawnerAI
  from components.consumable import Consumable
  from components.equipment import Equipment
  from components.equippable import Equippable
  from components.fighter import Fighter
  from components.harvestable import Harvestable
  from components.spawner import Spawner
  from components.inventory import Inventory
  from components.level import Level
  from game_map import GameMap

T = TypeVar('T', bound="Entity")

class Entity:
  """
  A generic object to represent players, enemies, items, etc.
  """

  parent: Union[GameMap, Inventory]

  def __init__(
      self,
      parent: Optional[GameMap] = None,
      x: int = 0,
      y: int = 0,
      char: str = '?',
      color: Tuple[int, int, int] = (255, 255, 255),
      name: str = '<Unnamed>',
      blocks_movement: bool = False,
      render_order: RenderOrder = RenderOrder.CORPSE
  ):
    self.x = x
    self.y = y
    self.char = char
    self.color = color
    self.name = name
    self.blocks_movement = blocks_movement
    self.render_order = render_order
    if parent: #if it comes with a gamemap, add it
      self.gamemap = parent
      parent.entities.add(self)
  @property
  def gamemap(self) -> GameMap:
    return self.parent.gamemap

  def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
    clone = copy.deepcopy(self)
    clone.x = x
    clone.y = y
    clone.parent = gamemap
    gamemap.entities.add(clone)
    return clone
  
  def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
    #move entity from one place to another, potentially
    #across gamemaps
    self.x = x
    self.y = y
    if gamemap:
      if hasattr(self, 'parent'):
        if self.parent is self.gamemap:
          self.gamemap.entities.remove(self)
          #if its already on a map, remove it
      self.parent = gamemap
      gamemap.entities.add(self)

  def distance(self, x: int, y: int) -> float:
    return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

  def move(self, dx: int, dy: int) -> None:
    self.x += dx
    self.y += dy

  def get_name(self,) -> str:
    return self.name

class Actor(Entity):
  def __init__(
      self,
      *,
      x: int = 0,
      y: int = 0,
      char: str = '?',
      color: Tuple[int, int, int] = (255, 255, 255),
      name: str = '<Unnamed>',
      blocks_movement: bool = True,
      render_order: RenderOrder = RenderOrder.ACTOR,
      ai_cls: Type[BaseAI],
      equipment: Equipment,
      fighter: Fighter,
      inventory: Inventory,
      level: Level,
      faction: str,
  ):
      super().__init__(
        x=x,
        y=y,
        char=char,
        color=color,
        name=name,
        blocks_movement=blocks_movement,
        render_order=render_order,
      )

      self.ai: Optional[BaseAI] = ai_cls(self)

      self.equipment: Optional[Equipment] = equipment
      if self.equipment:
        self.equipment.parent = self
    
      self.fighter = fighter
      self.fighter.parent = self

      self.inventory: Optional[Inventory] = inventory
      if self.inventory:
        self.inventory.parent = self

      self.level = level
      self.level.parent = self

      self.faction = Optional[faction]

  @property
  def is_alive(self) -> bool:
    return bool(self.ai)

class MobSpawner(Actor):
  def __init__(
      self,
      *,
      x: int = 0,
      y: int = 0,
      char: str = 'O',
      color: Tuple[int, int, int] = (255, 255, 255),
      name: str = '<Unnamed>',
      fighter: Fighter,
      level: Level,
      ai_cls: Type[SpawnerAI],
      spawner: Type[Spawner],
      faction: str,
  ):
    super().__init__(
      x=x,
      y=y,
      char=char,
      color=color,
      name=name,
      ai_cls=ai_cls,
      equipment=None,
      fighter=fighter,
      inventory=None,
      level=level,
      blocks_movement=False,
      render_order=RenderOrder.STRUCTURE,
      faction=faction,
    )

    self.ai: Optional[BaseAI] = ai_cls(self)
    
    self.spawner: Optional[Spawner] = spawner
    self.spawner.parent = self

class Item(Entity):
  def __init__(
      self,
      *,
      x: int = 0,
      y: int = 0,
      char: str = '?',
      color: Tuple[int, int, int] = (255, 255, 255),
      name: str = '<Unnamed>',
      consumable: Optional[Consumable] = None,
      equippable: Optional[Equippable] = None,
  ):
    super().__init__(
      x=x,
      y=y,
      char=char,
      color=color,
      name=name,
      blocks_movement=False,
      render_order=RenderOrder.ITEM,
    )

    self.consumable = consumable
    # self.consumable.parent = self

    if self.consumable:
      self.consumable.parent = self

    self.equippable = equippable

    if self.equippable:
      self.equippable.parent = self

class ResourceWell(Entity):
  #resources can be gathered here by workers
  def __init__(
    self,
    *,
    x: int = 0,
    y: int = 0,
    char: str = '?',
    color: Tuple[int, int, int] = (255, 255, 255),
    name: str = '<Unnamed>',
    harvestable: Harvestable
  ):
    super().__init__(
      x=x,
      y=y,
      char=char,
      color=color,
      name=name,
      blocks_movement=True,
      render_order=RenderOrder.STRUCTURE
    )

    self.harvestable = harvestable

  def get_name(self) -> str:
    return f'{self.name} [{self.harvestable.capacity}]'
  