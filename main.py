from remove_levels import RemoveLevels
import json

level_remover = RemoveLevels("Adult Red Dragon")
unmod_out = json.dumps(level_remover.monster, indent=4)
out = json.dumps(level_remover.compose(), indent=4)
