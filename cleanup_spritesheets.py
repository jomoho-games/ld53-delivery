
from game import *

sheets = [
  "assets/sheets/sheet01.json",
  "assets/sheets/sheet02.json",
  "assets/sheets/sheet03.json",
  "assets/sheets/sheet_nice.json",
  "assets/sheets/sheet_clumps.json",
]

spritesheet_manager = SpritesheetManager()
for i,s in enumerate(sheets):
  SpritesheetManager.remove_duplicate_sprites(s)