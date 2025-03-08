from components.ai import HostileEnemy, Miner
from components import consumable, equippable, harvestable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item, ResourceWell

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
)

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
)

#resource wells
crystal_well = ResourceWell(
  char='C',
  color=(7, 227, 247),
  name='Crystal Well',
  harvestable = harvestable.Crystal(100)
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