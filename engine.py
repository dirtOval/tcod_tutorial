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
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    # from entity import Entity
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
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
            
    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)
        
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

        #old HP indicator
        # console.print(
        #     x=1,
        #     y=47,
        #     string=f'HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}',
        # )

        # for entity in self.entities:
        #     if self.game_map.visible[entity.x, entity.y]:
        #       console.print(entity.x, entity.y, entity.char, fg=entity.color)

        # context.present(console)

        #now handled by main.py
        # console.clear()