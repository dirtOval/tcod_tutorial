import tcod
import copy

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon

def main() -> None:
  screen_width = 80
  screen_height = 50

  # player_x = int(screen_width / 2)
  # player_y = int(screen_height / 2)

  # GAME CONST VARIABLES
  map_width = 80
  map_height = 43

  room_max_size = 10
  room_min_size = 6
  max_rooms = 30
  
  max_monsters_per_room = 2

  # maybe put these in a settings file later?


  tileset = tcod.tileset.load_tilesheet(
    'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
  )

  # player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255))
  player = copy.deepcopy(entity_factories.player)

  engine = Engine(player=player)

  engine.game_map = generate_dungeon(
    max_rooms=max_rooms,
    room_min_size=room_min_size,
    room_max_size=room_max_size,
    map_width=map_width,
    map_height=map_height,
    max_monsters_per_room=max_monsters_per_room,
    engine=engine,
  )
  engine.update_fov()

  engine.message_log.add_message(
    'its dungeon time baybee oh YEAHHHHHHHH', color.welcome_text
  )

  # engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

  with tcod.context.new_terminal(
    screen_width,
    screen_height,
    tileset=tileset,
    title="Roguelike Tutorial",
    vsync=True,
  ) as context:
    root_console = tcod.console.Console(screen_width, screen_height, order='F')
    while True:
      root_console.clear()
      engine.event_handler.on_render(console=root_console)
      context.present(root_console)
      # engine.render(console=root_console, context=context)
      engine.event_handler.handle_events(context)
      # engine.event_handler.handle_events()

#boilerplate to make sure main only runs when the script is called
if __name__ == "__main__":
  main()