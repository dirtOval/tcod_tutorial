from enum import auto, Enum

class RenderOrder(Enum):
  CORPSE = auto()
  ITEM = auto()
  RESOURCE_WELL = auto()
  ACTOR = auto()