from components.ai import HostileEnemy, Miner, SpawnerAI
from components import consumable, equippable, harvestable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.spawner import VirusSpawner
from entity import Actor, Item, MobSpawner, ResourceWell

# player = Entity(char='@', color=(255, 255, 255), name='Player', blocks_movement=True)
player = Actor(
  char='@',
  color=(255, 255, 255),
  name='Player',
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=30, base_defense=1, base_power=2),
  inventory=Inventory(capacity=26),
  level=Level(level_up_base=200),
  faction='player',
)

#allied mobs
# guard = Actor(
#   char='g',
#   color=(0, 0, 200),
#   name='Guard',
#   ai_cls=AlliedCombatant,
#   equipment=Equipment(),
#   fighter=Fighter(hp=10, base_defense=0, base_power=4),
#   inventory=Inventory(capacity=1),
#   level=Level(xp_given=0),
#   faction='ally'
# )
#neutral mobs
miner = Actor(
  char='m',
  color=(0, 0, 200),
  name='Miner',
  ai_cls=Miner,
  equipment=Equipment(),
  fighter=Fighter(hp=5, base_defense=0, base_power=1),
  inventory=Inventory(capacity=1),
  level=Level(xp_given=0),
  faction='neutral',
)

#hostile mobs
virus = Actor(
  char='v',
  color=(0, 150, 150),
  name='Virus',
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=10, base_defense=0, base_power=4),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=35),
  faction='hostile',
)


#mob spawners
virus_spawner = MobSpawner(
  char='O',
  color=(0, 150, 150),
  name='Virus Spawner',
  fighter=Fighter(hp=20, base_defense=3, base_power=0),
  level=Level(xp_given=50),
  ai_cls=SpawnerAI,
  spawner=VirusSpawner(),
  faction='hostile',
)

#resource wells
crystal_well = ResourceWell(
  char='C',
  color=(7, 227, 247),
  name='Crystal Well',
  harvestable = harvestable.Crystal(100)
)

#TUTORIAL STUFF-------------------------------------------
orc = Actor(
  char='o',
  color=(63, 127, 63),
  name='Orc',
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=10, base_defense=0, base_power=4),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=35),
  faction='hostile',
)
troll = Actor(
  char='T',
  color=(0, 127, 0),
  name='Troll',
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=16, base_defense=1, base_power=8),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=100),
  faction='hostile',
)

#ITEMS -- TUTORIAL
confusion_scroll = Item(
  char='~',
  color=(207, 63, 255),
  name='Confusion Scroll',
  consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
  char='~',
  color=(255, 0, 0),
  name='Fireball Scroll',
  consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
  char='!',
  color=(127, 0, 255),
  name='Health Potion',
  consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
  char='~',
  color= (255, 255, 0),
  name='Lightning Scroll',
  consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

#equipment -- tutorial

dagger = Item(
  char='/', color=(0, 191, 255), name='Dagger', equippable=equippable.Dagger()
)

sword = Item(
  char='/', color=(0, 191, 255), name='Sword', equippable=equippable.Sword()
)

leather_armor = Item(
  char='[',
  color=(139, 69, 19),
  name='Leather Armor',
  equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
  char='[',
  color=(139, 69, 19),
  name='Chain Mail',
  equippable=equippable.ChainMail(),
)