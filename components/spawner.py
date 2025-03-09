from __future__ import annotations
from typing import TYPE_CHECKING

from components.base_component import BaseComponent
import entity_factories

if TYPE_CHECKING:
  from entity import MobSpawner, Actor

class Spawner(BaseComponent):
  parent: MobSpawner

  def __init__(
      self,
      mob: Actor,
      delay: int,
  ):
    self.mob = mob
    self.delay = delay
    self.timer = delay

  def spawn_mob(self) -> None:
    dungeon = self.parent.parent
    if not any(entity is not self.parent and entity.x == self.parent.x and entity.y == self.parent.y for entity in dungeon.entities):
      self.mob.spawn(dungeon, self.parent.x, self.parent.y)

  def decrement_timer(self) -> None:
    self.timer -= 1
    print(f'{self.parent.name} timer: {self.timer}')
    if self.timer <= 0:
      self.spawn_mob()
      self.timer = self.delay

class VirusSpawner(Spawner):
  def __init__(self, delay = 5) -> None:
    super().__init__(mob=entity_factories.virus, delay=delay)