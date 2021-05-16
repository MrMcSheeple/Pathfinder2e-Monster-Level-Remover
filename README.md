# Pathfinder2e-Monster-Level-Remover
This tool is for helping DMs power down their encounters by removing the level from Pathfinder 2e Monsters.
The data repository used here was put together by jimbarnesrtp and their conributors.
Check out their work at https://github.com/jimbarnesrtp/pf2/

A quick note: The source data has some issues due to the difficulty of parsing it in the first place.
If there is something about a generated statblock that looks wrong, make sure to verify it at
https://2e.aonprd.com/Monsters.aspx?Letter=All

**Usage**\
Show the help menu\
`./main.py -h`

Print the nerfed monster to the console\
`./main.py <name>`

Write the nerfed monster to a yaml file\
`./main.py <name> -f <filename.yaml>`

The entire bestiary can be generated using the tester, but make sure you run the program at least once, so the
pickle file exists.