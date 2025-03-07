# from typing import Set, Iterable, Any

from __future__ import annotations

import lzma
import pickle

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
# from tcod import FOV_SYMMETRIC_SHADOWCAST

import exceptions
# from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    # from entity import Entity
    from entity import Actor
    from game_map import GameMap
    # from input_handlers import EventHandler

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        # self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        # self.game_map = game_map
        # self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            # print(f'The {entity.name} does nothing on its turn :P')
            if entity.ai:
                try:
                  entity.ai.perform()
                except exceptions.Impossible:
                    pass #plays dont need to know every time AI fails attempt

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
    
    def save_as(self, filename: str) -> None:
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, 'wb') as f:
            f.write(save_data)