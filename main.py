import tcod
# import copy
import traceback

import color
# from engine import Engine
# import entity_factories
import exceptions
import input_handlers
# from procgen import generate_dungeon
import setup_game

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
  if isinstance(handler, input_handlers.EventHandler):
    handler.engine.save_as(filename)
    print('Game saved!')

def main() -> None:
  screen_width = 80
  screen_height = 50

  # player_x = int(screen_width / 2)
  # player_y = int(screen_height / 2)

  # GAME CONST VARIABLES
  # map_width = 80
  # map_height = 43

  # room_max_size = 10
  # room_min_size = 6
  # max_rooms = 30
  
  # max_monsters_per_room = 2
  # max_items_per_room = 2

  # maybe put these in a settings file later?


  tileset = tcod.tileset.load_tilesheet(
    'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
  )

  # player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255))
  # player = copy.deepcopy(entity_factories.player)

  # engine = Engine(player=player)

  # engine.game_map = generate_dungeon(
  #   max_rooms=max_rooms,
  #   room_min_size=room_min_size,
  #   room_max_size=room_max_size,
  #   map_width=map_width,
  #   map_height=map_height,
  #   max_monsters_per_room=max_monsters_per_room,
  #   max_items_per_room=max_items_per_room,
  #   engine=engine,
  # )
  # engine.update_fov()

  # engine.message_log.add_message(
  #   'its dungeon time baybee oh YEAHHHHHHHH', color.welcome_text
  # )

  # handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)
  handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

  # engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

  with tcod.context.new_terminal(
    screen_width,
    screen_height,
    tileset=tileset,
    title="Roguelike Tutorial",
    vsync=True,
  ) as context:
    root_console = tcod.console.Console(screen_width, screen_height, order='F')
    # while True:
    #   root_console.clear()
    #   engine.event_handler.on_render(console=root_console)
    #   context.present(root_console)
    
    #   try:
    #     for event in tcod.event.wait():
    #       context.convert_event(event)
    #       engine.event_handler.handle_events(event)
    #   except Exception:
    #     traceback.print_exc()
    #     engine.message_log.add_message(traceback.format_exc(), color.error)
    try:
      while True:
        root_console.clear()
        handler.on_render(console=root_console)
        context.present(root_console)

        try:
          for event in tcod.event.wait():
            context.convert_event(event)
            handler = handler.handle_events(event)
        except Exception:
          traceback.print_exc()
          if isinstance(handler, input_handlers.EventHandler):
            handler.engine.message_log.add_message(
              traceback.format_exc(), color.error
            )
    except exceptions.QuitWithoutSaving:
      raise
    except SystemExit: #saving this time
      save_game(handler, 'savegame.sav')
      raise
    except BaseException: #save if something else breaks
      save_game(handler, 'savegame.sav')
      raise
#boilerplate to make sure main only runs when the script is called
if __name__ == "__main__":
  main()