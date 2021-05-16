import pickle
import re


class RemoveLevels:
    def __init__(self, monster):
        with open('pf2e_bestiary.pickle', 'rb') as f:
            self.monster_dict = pickle.load(f)
            f.close()

        if monster in self.monster_dict:
            self.monster = self.monster_dict[monster]
            self.level = self.monster["level"]
            # print(self.monster)
        else:
            raise KeyError("Monster doesn't exist! Maybe check your spelling?")

    def modify_spells(self):
        data = self.monster

        # replace spell DC
        # spell[:6] -> DC xy therefore spell[4:6] -> xy
        for spell in data['spells']:
            dc = int(spell['text'][4:6])
            new_dc = " DC {}".format(dc - self.level)
            spell['text'] = new_dc + spell['text'][6:]

        # replace spell attack bonus
        for spell in data['spells']:
            try:
                # get spell attack bonus if specified
                atk = int(spell['text'][16:18])
            except ValueError:
                continue
            new_atk = "attack +{}".format(atk - self.level)
            spell['text'] = spell['text'][:8] + new_atk + spell['text'][18:]

        return data['spells']

    def modify_skills(self):
        data = self.monster

        skill_names = data['skills'][::2]
        skill_values = data['skills'][1::2]

        ptrn = re.compile('[0-9]+')

        for v in range(len(skill_values)):
            num = ''.join(skill_values[v][2:4])
            skill_values[v] = re.sub(ptrn, str(int(num) - self.level), skill_values[v])

        skills = []
        for n in range(len(skill_names)):
            skills.append(skill_names[n])
            skills.append(skill_values[n])

        return skills

    def modify_actions(self):
        data = self.monster

        ptrn_dc = re.compile('DC [0-9]+')

        for a in data['actions']:
            dc = re.search(ptrn_dc, a['text'])
            excl_ptrn = re.compile('DC [0-9]+ flat')
            excl = re.search(excl_ptrn, a['text'])

            if dc:
                if excl:
                    continue

                dc_mod = dc.group()
                dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]

                dc_val = int(dc_val)
                dc_val -= self.level

                a['text'] = re.sub(ptrn_dc, dc_dc + str(dc_val), a['text'])

        return data['actions']

    def modify_attacks(self):
        data = self.monster

        ptrn_atk = re.compile('[+-][0-9]+')
        ptrn_dc = re.compile('DC [0-9]+')

        for a in data['attacks']:
            atk = re.search(ptrn_atk, a['text'])
            dc = re.search(ptrn_dc, a['text'])

            if atk:
                atk_mod = atk.group()
                atk_t, atk_val = str(atk_mod)[0], str(atk_mod)[1:]

                atk_val = int(atk_val)
                atk_val -= self.level

                a['text'] = re.sub(ptrn_atk, atk_t + str(atk_val), a['text'])

            if dc:
                excl_ptrn = re.compile('DC [0-9]+ flat')
                excl = re.search(excl_ptrn, a['text'])
                if excl:
                    continue

                dc_mod = dc.group()
                dc_dc, dc_val = str(dc_mod)[0:3], str(dc_mod)[3:]

                dc_val = int(dc_val)
                dc_val -= self.level

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

        data['recallKnowledge'] = re.sub(str(rec_know), str(rec_know - self.level), data['recallKnowledge'])
        data['Perception'] = re.sub(str(perc), str(perc - self.level), data['Perception'])
        data['AC'] = re.sub(str(ac), str(ac - self.level), data['Fort'])
        data['Fort'] = re.sub(str(fort), str(fort - self.level), data['Fort'])
        data['Ref'] = re.sub(str(ref), str(ref - self.level), data['Ref'])
        data['Will'] = re.sub(str(will), str(will - self.level), data['Will'])

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

        return data
