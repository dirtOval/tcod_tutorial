from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import (
  Action,
  EscapeAction,
  BumpAction,
  WaitAction
)
import color
import exceptions

#find out wtf TYPE_CHECKING is
if TYPE_CHECKING:
  from engine import Engine

MOVE_KEYS = {
  #arrow keys
  tcod.event.K_UP: (0, -1),
  tcod.event.K_DOWN: (0, 1),
  tcod.event.K_LEFT: (-1, 0),
  tcod.event.K_RIGHT: (1, 0),
  tcod.event.K_HOME: (-1, -1),
  tcod.event.K_END: (-1, 1),
  tcod.event.K_PAGEUP: (1, -1),
  tcod.event.K_PAGEDOWN: (1, 1),
  # Numpad keys.
  tcod.event.K_KP_1: (-1, 1),
  tcod.event.K_KP_2: (0, 1),
  tcod.event.K_KP_3: (1, 1),
  tcod.event.K_KP_4: (-1, 0),
  tcod.event.K_KP_6: (1, 0),
  tcod.event.K_KP_7: (-1, -1),
  tcod.event.K_KP_8: (0, -1),
  tcod.event.K_KP_9: (1, -1),
  # Vi keys.
  tcod.event.K_h: (-1, 0),
  tcod.event.K_j: (0, 1),
  tcod.event.K_k: (0, -1),
  tcod.event.K_l: (1, 0),
  tcod.event.K_y: (-1, -1),
  tcod.event.K_u: (1, -1),
  tcod.event.K_b: (-1, 1),
  tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

class EventHandler(tcod.event.EventDispatch[Action]):
  def __init__(self, engine: Engine):
    self.engine = engine

  # def handle_events(self) -> None:
  #   raise NotImplementedError()

  def handle_events(self, event: tcod.event.Event) -> None:
    self.handle_action(self.dispatch(event))
  
  def handle_action(self, action: Optional[Action]) -> bool:
    if action is None:
      return False
    
    try:
      action.perform()
    except exceptions.Impossible as exc:
      self.engine.message_log.add_message(exc.args[0], color.impossible)
      return False
    
    self.engine.handle_enemy_turns()

    self.engine.update_fov()
    return True
  
  # def handle_events(self, context: tcod.context.Context) -> None:
  #   for event in tcod.event.wait():
  #     context.convert_event(event)
  #     self.dispatch(event)

  def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
    if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
      self.engine.mouse_location = event.tile.x, event.tile.y
  
  def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
    raise SystemExit()
  
  def on_render(self, console: tcod.Console) -> None:
    self.engine.render(console)

class MainGameEventHandler(EventHandler):
  # def handle_events(self, context: tcod.context.Context) -> None:
  #   for event in tcod.event.wait():
  #     context.convert_event(event)
  #     action = self.dispatch(event)

  #     if action is None:
  #       continue

  #     action.perform()

  #     self.engine.handle_enemy_turns()
  #     self.engine.update_fov()

  # def ev_quit(self, event: tcod.event.KeyDown) -> Optional[Action]:
  #   raise SystemExit()
  
  def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
    action: Optional[Action] = None

    key = event.sym

    player = self.engine.player

    #Old input handling
    # if key == tcod.event.K_UP:
    #   action = BumpAction(player, dx=0, dy=-1)
    # elif key == tcod.event.K_DOWN:
    #   action = BumpAction(player, dx=0, dy=1)
    # elif key == tcod.event.K_LEFT:
    #   action = BumpAction(player, dx=-1, dy=0)
    # elif key == tcod.event.K_RIGHT:
    #   action = BumpAction(player, dx=1, dy=0)
    if key in MOVE_KEYS:
      dx, dy = MOVE_KEYS[key]
      action = BumpAction(player, dx, dy)
    elif key in WAIT_KEYS:
      action = WaitAction(player)

    elif key == tcod.event.K_ESCAPE:
      action = EscapeAction(player)

    elif key == tcod.event.K_v:
      self.engine.event_handler = HistoryViewer(self.engine)

    return action
  
class GameOverEventHandler(EventHandler):
  # def handle_events(self, context: tcod.context.Context) -> None:
  #   for event in tcod.event.wait():
  #     action = self.dispatch(event)

  #     if action is None:
  #       continue

  #     action.perform()

  # def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
  #   action: Optional[Action] = None

  #   key = event.sym

  #   if key == tcod.event.K_ESCAPE:
  #     action = EscapeAction(self.engine.player)

  #   return action
  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    if event.sym == tcod.event.K_ESCAPE:
      raise SystemExit()
  
CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

class HistoryViewer(EventHandler):
  def __init__(self, engine: Engine):
    super().__init__(engine)
    self.log_length = len(engine.message_log.messages)
    self.cursor = self.log_length - 1

  def on_render(self, console: tcod.Console) -> None:
    super().on_render(console) #keeps drawing main state behind

    log_console = tcod.Console(console.width - 6, console.height - 6)

    log_console.draw_frame(0, 0, log_console.width, log_console.height)
    log_console.print_box(
      0, 0, log_console.width, 1, '~|Message History|~', alignment=tcod.CENTER
    )

    self.engine.message_log.render_messages(
      log_console,
      1,
      1,
      log_console.width - 2,
      log_console.height - 2,
      self.engine.message_log.messages[: self.cursor + 1],
    )
    log_console.blit(console, 3, 3)

  def ev_keydown(self, event: tcod.event.KeyDown) -> None:
    if event.sym in CURSOR_Y_KEYS:
      adjust = CURSOR_Y_KEYS[event.sym]
      if adjust < 0 and self.cursor == 0:
        self.cursor = self.log_length - 1
      elif adjust > 0 and self.cursor == self.log_length - 1:
        self.cursor = 0
      else:
        self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
    elif event.sym == tcod.event.K_HOME:
      self.cursor = 0
    elif event.sym == tcod.event.K_END:
      self.cursor = self.log_length - 1
    else:
      self.engine.event_handler = MainGameEventHandler(self.engine)