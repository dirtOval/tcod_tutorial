# from typing import Set, Iterable, Any

from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
# from tcod import FOV_SYMMETRIC_SHADOWCAST

# from actions import EscapeAction, MovementAction
# from entity import Entity
# from game_map import GameMap
from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap

class Engine:
    game_map: GameMap

    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player
        # self.game_map = game_map
        # self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            # print(f'The {entity.name} does nothing on its turn :P')
            if entity.ai:
                entity.ai.perform()
      
    # def handle_events(self, events: Iterable[Any]) -> None:
    #     for event in events:
    #         action = self.event_handler.dispatch(event)

    #         if action is None:
    #             continue
            
    #         action.perform(self, self.player)
    #         self.handle_enemy_turns()
    #         self.update_fov()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8, #should make this a variable later. flashlight/torch etc
            #fuck with FOV algorithm
        )
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        # for entity in self.entities:
        #     if self.game_map.visible[entity.x, entity.y]:
        #       console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()