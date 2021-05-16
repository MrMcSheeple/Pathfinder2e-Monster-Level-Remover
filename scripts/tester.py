#!/usr/bin/env python3
# RUN FROM TERMINAL, NOT FROM IDE
# DO NOT RUN THIS UNTIL YOU'VE RUN MAIN.PY AT LEAST ONCE
import yaml
import requests
import os
from os import system as bash
from sys import path
path.append('../')
print(os.getcwd())
import remove_levels
os.chdir('..')
print(os.getcwd())


def get_data():
    url = "https://raw.githubusercontent.com/jimbarnesrtp/pf2/master/monsters-v2-pf2.json"
    raw_data = requests.get(url).json()["monsters"]

    return raw_data


data = get_data()
names = [d["name"] for d in data]

choice = int(input("0 to print test to console, 1 to print test to files:\n"))

print(os.getcwd())
if choice == 0:
    for n in names:
        try:
            print(yaml.dump(remove_levels.RemoveLevels(n).compose(), sort_keys=False, indent=4))
        except remove_levels.BrokenMonster:
            continue

elif choice == 1:
    os.chdir('scripts/')
    bash('mkdir Bestiary')
    for n in names:
        try:
            os.chdir('..')
            out = yaml.dump(remove_levels.RemoveLevels(n).compose(), sort_keys=False, indent=4)
            print(n)
            os.chdir('scripts/')
            with open(f'Bestiary/{n}.yaml', 'w') as f:
                f.write(out)
                f.close()
        except remove_levels.BrokenMonster:
            os.chdir('scripts/')
            continue

    os.chdir('Bestiary/')
    bash('tar -cf Bestiary.tar *.yaml')
    bash('mv Bestiary.tar ../')
