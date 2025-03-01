from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
  from engine import Engine
  from entity import Entity

class Action:
  def __init__(self, entity: Entity) -> None:
    super().__init__()
    self.entity = entity
  
  @property
  def engine(self) -> Engine:
    return self.entity.gamemap.engine #get the engine

  def perform(self) -> None:
    #lmao this has to be overridden by subclass, action is an abstract class
    #hence the error
    raise NotImplementedError()

class EscapeAction(Action):
  def perform(self) -> None:
    raise SystemExit()
  
class ActionWithDirection(Action):
  def __init__(self, entity: Entity, dx: int, dy: int):
    super().__init__(entity)

    self.dx = dx
    self.dy = dy

  @property
  def dest_xy(self) -> Tuple[int, int]:
    return self.entity.x + self.dx, self.entity.y + self.dy
  
  @property
  def blocking_entity(self) -> Optional[Entity]:
    return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

  def perform(self) -> None:
    raise NotImplementedError()
  
class MeleeAction(ActionWithDirection):
  def perform(self) -> None:
    target = self.blocking_entity
    if not target:
      return
    
    print(f'You kick the {target.name}, dealing 1,000,000 damage')

class MovementAction(ActionWithDirection):
  def perform(self) -> None:
    dest_x, dest_y = self.dest_xy

    if not self.engine.game_map.in_bounds(dest_x, dest_y):
      return #cant leave the map
    
    if not self.engine.game_map.tiles['walkable'][dest_x, dest_y]:
      return #cant walk thru walls
    
    if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
      return
    
    self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
  def perform(self) -> None:
    # dest_x = entity.x + self.dx
    # dest_y = entity.y + self.dy

    # if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
    #   return MeleeAction(self.dx, self.dy).perform(engine, entity)
    if self.blocking_entity:
      return MeleeAction(self.entity, self.dx, self.dy).perform()
    else:
      return MovementAction(self.entity, self.dx, self.dy).perform()