#!/usr/bin/env python3
from remove_levels import RemoveLevels
from os import path
import retrieve
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Name of the monster')
parser.add_argument('--output-file', '-f', type=str, help='Optionally output to yaml file instead of console')

args = parser.parse_args()

# if the pickle file was deleted, regenerate it
if not path.exists('pf2e_bestiary.pickle'):
    retrieve.write_pickle()

# calls the level remover class and sets it to an object
level_remover = RemoveLevels(args.name)
# calls the function to nerf the monster, and writes it to yaml format
# yaml keys are unsorted to prevent alphabetization
out = yaml.dump(level_remover.compose(), sort_keys=False, indent=4)

if args.output_file:
    with open(args.output_file, 'w') as f:
        f.write(out)
        f.close()
else:
    print(out)
