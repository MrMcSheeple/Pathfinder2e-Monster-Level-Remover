import pickle
import re


class BrokenMonster(Exception):
    def __init__(self):
        self.message = ("This monster is broken, and therefore not supported.\n"
                        "It is either missing too much information to be useable or it is garbled in some way"
                        "that makes it incompatible with the parsers that work on the rest of the monsters.")

    def __str__(self):
        return self.message


class RemoveLevels:
    def __init__(self, monster):
        with open('pf2e_bestiary.pickle', 'rb') as f:
            # loads the pickle file containing the dictionary of all monsters
            self.monster_dict = pickle.load(f)
            f.close()

        # This list is for statblocks that are missing too much information to be useful
        # and break the program due to that missing information
        broken_list = ["Graveknight"]
        if monster in broken_list:
            raise BrokenMonster

        if monster in self.monster_dict:
            # if the monster exists get its attributes and level, else throw a KeyError
            self.monster = self.monster_dict[monster]
            self.level = self.monster["level"]
            # print(self.monster)
        else:
            raise KeyError("Monster doesn't exist! Maybe check your spelling?")

    def modify_rituals(self, ritual_type):
        ptrn = re.compile('[0-9]+')
        # modifies the DC of a ritual. Type only matters for what key it needs to refer to
        # set this to a variable as all the checking is done in the compose function
        if self.monster[ritual_type]:
            data = self.monster[ritual_type]
            rituals = int(ptrn.findall(data)[0])
            data = re.sub(str(rituals), str(rituals - abs(self.level)), data)
            return data

    def modify_spells(self):
        data = self.monster
        atk_ptrn = re.compile('[+-][0-9]+')
        dc_ptrn = re.compile('DC [0-9]+')

        for spell in data['spells']:
            dc = dc_ptrn.findall(spell['text'])
            atk = atk_ptrn.findall(spell['text'])

            if dc:
                # builds the new DC and rebuilds the string
                new_dc = "DC {}".format(int(dc[0][3:]) - abs(self.level))
                spell['text'] = re.sub(dc_ptrn, new_dc, spell['text'])

            if atk:
                # builds the new attack mod and rebuilds the string
                new_atk = atk[0][0] + str(int(atk[0][1:]) - abs(self.level))
                spell['text'] = re.sub(atk_ptrn, new_atk, spell['text'])

        return data['spells']

    def modify_skills(self):
        data = self.monster

        # splits the list containing skill names and their values into separate lists
        skill_names, skill_values = data['skills'][::2], data['skills'][1::2]

        ptrn = re.compile('[0-9]+')
        for v in range(len(skill_values)):
            # loops through and searches for a match. If found, replace the value and rebuild the string
            num = re.search(ptrn, skill_values[v])
            if num:
                skill_values[v] = re.sub(ptrn, str(int(num.group()) - abs(self.level)), skill_values[v])

        skills = []
        for n in range(len(skill_names)):
            # rebuild the list from the separate lists containing the names and values
            skills.append(skill_names[n])
            skills.append(skill_values[n])

        return skills

    def modify_actions(self):
        data = self.monster
        ptrn_dc = re.compile('DC [0-9]+')
        excl_ptrn = re.compile('DC [0-9]+ flat')

        for a in data['actions']:
            if 'text' in a:
                # searches for a match
                dc = re.search(ptrn_dc, a['text'])
                if dc:
                    # excludes flat DCs as they're not to be modified
                    # if a flat DC is found, skip to the next iteration
                    excl = re.search(excl_ptrn, a['text'])
                    if excl:
                        continue
                    dc_mod = dc.group()
                    dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]
                    dc_val = int(dc_val)
                    dc_val -= abs(self.level)
                    a['text'] = re.sub(ptrn_dc, dc_dc + str(dc_val), a['text'])

            if 'Effect' in a:
                # same as above, but for the Effect key
                eff_dc = re.search(ptrn_dc, a['Effect'])
                excl = re.search(excl_ptrn, a['Effect'])
                if eff_dc:
                    if excl:
                        continue
                    print()
                    dc_mod = eff_dc.group()
                    dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]
                    dc_val = int(dc_val)
                    dc_val -= abs(self.level)
                    a['Effect'] = re.sub(ptrn_dc, dc_dc + str(dc_val), a['Effect'])

        return data['actions']

    def modify_attacks(self):
        data = self.monster

        # compiles separate searches for DCs and Attack Bonuses
        ptrn_atk = re.compile('[+-][0-9]+')
        ptrn_dc = re.compile('DC [0-9]+')

        for a in data['attacks']:
            try:
                # searches for matches. If an error is thrown skip to the next iteration
                atk = re.search(ptrn_atk, a['text'])
                dc = re.search(ptrn_dc, a['text'])
            except KeyError:
                continue

            if atk:
                # separates the +- from the number, modifies the number, the rebuilds the string
                atk_mod = atk.group()
                atk_t, atk_val = str(atk_mod)[0], str(atk_mod)[1:]

                atk_val = int(atk_val)
                atk_val -= abs(self.level)

                a['text'] = re.sub(ptrn_atk, atk_t + str(atk_val), a['text'])

            if dc:
                # same as above, but for DCs
                excl_ptrn = re.compile('DC [0-9]+ flat')
                excl = re.search(excl_ptrn, a['text'])

                if excl:
                    continue

                dc_mod = dc.group()
                dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]

                dc_val = int(dc_val)
                dc_val -= abs(self.level)

                a['text'] = re.sub(ptrn_dc, dc_dc + str(dc_val), a['text'])

        return data['attacks']

    def compose(self):
        data = self.monster

        saves = re.compile('[0-9]+')

        # checks to see if recallKnowledge exists. It does for most monsters but there are some exceptions
        if 'recallKnowledge' in data:
            rec_know = int(saves.findall(data['recallKnowledge'])[0])
            data['recallKnowledge'] = re.sub(str(rec_know), str(rec_know - abs(self.level)), data['recallKnowledge'])

        # grabs the first match, modifies it, and reinserts it.
        perc = int(saves.findall(data['Perception'])[0])
        data['Perception'] = re.sub(str(perc), str(perc - abs(self.level)), data['Perception'])
        ac = int(saves.findall(data['AC'])[0])
        data['AC'] = re.sub(str(ac), str(ac - abs(self.level)), data['AC'])

        # searches to see if the string exists. If it does, modify the number and reinsert
        fort = saves.search(data['Fort'])
        if fort:
            data['Fort'] = re.sub(str(fort.group()), str(int(fort.group()) - abs(self.level)), data['Fort'])
        ref = saves.search(data['Ref'])
        if ref:
            data['Ref'] = re.sub(str(ref.group()), str(int(ref.group()) - abs(self.level)), data['Ref'])
        will = saves.search(data['Will'])
        if will:
            data['Will'] = re.sub(str(int(will.group())), str(int(will.group()) - abs(self.level)), data['Will'])
        # The following keys point to a list or dictionary
        # The functions called will modify the structure before the data is changed here.
        if data['spells']:
            data['spells'] = self.modify_spells()

        if data['skills']:
            data['skills'] = self.modify_skills()

        if data['actions']:
            data['actions'] = self.modify_actions()

        if data['attacks']:
            data['attacks'] = self.modify_attacks()

        # checks to see if any of the ritual key exists. Using elif is marginally more efficient here.
        if 'Rituals' in data:
            data['Rituals'] = self.modify_rituals('Rituals')
        elif 'Occult Rituals' in data:
            data['Occult Rituals'] = self.modify_rituals('Occult Rituals')
        elif 'Divine Rituals' in data:
            data['Divine Rituals'] = self.modify_rituals('Divine Rituals')
        elif 'Primal Rituals' in data:
            data['Primal Rituals'] = self.modify_rituals('Primal Rituals')

        return data
