import tcod

# from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

def main() -> None:
  screen_width = 80
  screen_height = 50

  # player_x = int(screen_width / 2)
  # player_y = int(screen_height / 2)

  map_width = 80
  map_height = 45

  tileset = tcod.tileset.load_tilesheet(
    'dejavu10x10_gs_tc.png', 32, 8, tcod.tileset.CHARMAP_TCOD
  )

  event_handler = EventHandler()

  player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255))
  npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', (255, 255, 0))
  entities = {npc, player}

  game_map = GameMap(map_width, map_height)

  # engine = Engine(entities=entities, event_handler=event_handler, player=player)
  engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

  with tcod.context.new_terminal(
    screen_width,
    screen_height,
    tileset=tileset,
    title="Roguelike Tutorial",
    vsync=True,
  ) as context:
    root_console = tcod.console.Console(screen_width, screen_height, order='F')
    while True:
      # root_console.print(x=player_x, y=player_y, string='@')
      # root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
      engine.render(console=root_console, context=context)

      # context.present(root_console)
      events = tcod.event.wait()

      engine.handle_events(events)
      # root_console.clear()

      # for event in tcod.event.wait():
      #   # if event.type == 'QUIT':
      #   #   raise SystemExit()

      #   action = event_handler.dispatch(event)

      #   if action is None:
      #     continue

      #   if isinstance(action, MovementAction):
      #     player_x += action.dx
      #     player_y += action.dy

      #   elif isinstance(action, EscapeAction):
      #     raise SystemExit()

#boilerplate to make sure main only runs when the script is called
if __name__ == "__main__":
  main()