from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from tcod import FOV_SYMMETRIC_SHADOWCAST

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()
      
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
            # if isinstance(action, MovementAction):
            #     # self.player.move(dx=action.dx, dy=action.dy)
            #     if self.game_map.tiles['walkable'][self.player.x + action.dx, self.player.y + action.dy]:
            #       self.player.move(dx=action.dx, dy=action.dy)

            # elif isinstance(action, EscapeAction):
            #     raise SystemExit()

            self.update_fov()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8, #should make this a variable later. flashlight/torch etc
            # algorithm=FOV_SYMMETRIC_SHADOWCAST <-- play with this value!!!
        )
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
              console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()