from typing import Tuple

import numpy as np

#dt is like a struct in C. our dt is: a 32 bit int, and 3 unsigned bytes x2
#for foreground and background color? i'm sure this will make sense later
graphic_dt = np.dtype(
  [
    ('ch', np.int32), #this corresponds to a Unicode character
    ('fg', '3B'),
    ('bg', '3B'),
  ]
)

tile_dt = np.dtype(
  [
    ('walkable', np.bool),
    ('transparent', np.bool),
    ('dark', graphic_dt),
  ]
)

def new_tile(
    *, #enforce use of keywords? find out what this means
    #oh wait i think it means arguments must be paired w/
    #keywords. sick.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
  return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
  walkable=True, transparent=True, dark=(ord(' '), (255, 255, 255), (50, 50, 150)),
)
wall = new_tile(
  walkable=False, transparent=False, dark=(ord(' '), (255, 255, 255), (0, 0, 100)),
)

#add glass? transparent, but not walkable