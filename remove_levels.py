import pickle
import re


class RemoveLevels:
    def __init__(self, monster):
        with open('pf2e_bestiary.pickle', 'rb') as f:
            # loads the pickle file containing the dictionary of all monsters
            self.monster_dict = pickle.load(f)
            f.close()

        if monster in self.monster_dict:
            # if the monster exists get its attributes and level, else throw a KeyError
            self.monster = self.monster_dict[monster]
            self.level = self.monster["level"]
            # print(self.monster)
        else:
            raise KeyError("Monster doesn't exist! Maybe check your spelling?")

    def modify_rituals(self, ritual_type):
        ptrn = re.compile('[0-9]+')
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
                new_dc = "DC {}".format(int(dc[0][3:]) - abs(self.level))
                spell['text'] = re.sub(dc_ptrn, new_dc, spell['text'])

            if atk:
                new_atk = atk[0][0] + str(int(atk[0][1:]) - abs(self.level))
                spell['text'] = re.sub(atk_ptrn, new_atk, spell['text'])

        return data['spells']

    def modify_skills(self):
        data = self.monster

        # splits the list containing skill names and their values into separate lists
        skill_names, skill_values = data['skills'][::2], data['skills'][1::2]

        ptrn = re.compile('[0-9]+')
        for v in range(len(skill_values)):
            num = re.search(ptrn, skill_values[v])
            if num:
                skill_values[v] = re.sub(ptrn, str(int(num.group()) - abs(self.level)), skill_values[v])

        skills = []
        for n in range(len(skill_names)):
            skills.append(skill_names[n])
            skills.append(skill_values[n])

        return skills

    def modify_actions(self):
        data = self.monster
        ptrn_dc = re.compile('DC [0-9]+')
        excl_ptrn = re.compile('DC [0-9]+ flat')

        for a in data['actions']:
            dc = re.search(ptrn_dc, a['text'])
            if dc:
                excl = re.search(excl_ptrn, a['text'])
                if excl:
                    continue
                dc_mod = dc.group()
                dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]
                dc_val = int(dc_val)
                dc_val -= abs(self.level)
                a['text'] = re.sub(ptrn_dc, dc_dc + str(dc_val), a['text'])

            if 'Effect' in a:
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

        ptrn_atk = re.compile('[+-][0-9]+')
        ptrn_dc = re.compile('DC [0-9]+')

        for a in data['attacks']:
            try:
                atk = re.search(ptrn_atk, a['text'])
                dc = re.search(ptrn_dc, a['text'])
            except KeyError:
                continue

            if atk:
                atk_mod = atk.group()
                atk_t, atk_val = str(atk_mod)[0], str(atk_mod)[1:]

                atk_val = int(atk_val)
                atk_val -= abs(self.level)

                a['text'] = re.sub(ptrn_atk, atk_t + str(atk_val), a['text'])

            if dc:
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
        rec_know = int(saves.findall(data['recallKnowledge'])[0])
        perc = int(saves.findall(data['Perception'])[0])
        ac = int(saves.findall(data['AC'])[0])
        fort = int(saves.findall(data['Fort'])[0])
        ref = int(saves.findall(data['Ref'])[0])
        will = int(saves.findall(data['Will'])[0])

        data['recallKnowledge'] = re.sub(str(rec_know), str(rec_know - abs(self.level)), data['recallKnowledge'])
        data['Perception'] = re.sub(str(perc), str(perc - abs(self.level)), data['Perception'])
        data['AC'] = re.sub(str(ac), str(ac - abs(self.level)), data['AC'])
        data['Fort'] = re.sub(str(fort), str(fort - abs(self.level)), data['Fort'])
        data['Ref'] = re.sub(str(ref), str(ref - abs(self.level)), data['Ref'])
        data['Will'] = re.sub(str(will), str(will - abs(self.level)), data['Will'])

        # spells are stored as a list of dictionaries containing spells
        # if the spell list is not blank, modify it
        if data['spells']:
            data['spells'] = self.modify_spells()

        if data['skills']:
            data['skills'] = self.modify_skills()

        if data['actions']:
            data['actions'] = self.modify_actions()

        if data['attacks']:
            data['attacks'] = self.modify_attacks()

        if 'Rituals' in data:
            data['Rituals'] = self.modify_rituals('Rituals')
        elif 'Occult Rituals' in data:
            data['Occult Rituals'] = self.modify_rituals('Occult Rituals')
        elif 'Divine Rituals' in data:
            data['Divine Rituals'] = self.modify_rituals('Divine Rituals')
        elif 'Primal Rituals' in data:
            data['Primal Rituals'] = self.modify_rituals('Primal Rituals')

        return data
