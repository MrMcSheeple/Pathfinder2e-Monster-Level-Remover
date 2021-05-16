#!/usr/bin/env python3
from remove_levels import RemoveLevels
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Name of the monster')
parser.add_argument('--output-file', '-f', type=str, help='Optionally output to yaml file instead of console')

args = parser.parse_args()

try:
    level_remover = RemoveLevels(args.name)
    out = yaml.dump(level_remover.compose(), sort_keys=False)

    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(out)
            f.close()
    else:
        print(out)

except KeyError:
    print("Monster Does Not Exist. Check Spelling.")
