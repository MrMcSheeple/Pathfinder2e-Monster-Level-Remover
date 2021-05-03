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
        else:
            raise KeyError("Monster doesn't exist! Maybe check your spelling?")

    def modify_spells(self):
        data = self.monster

        # replace spell DC
        # spell[:6] -> DC xy therefore spell[4:6] -> xy
        for spell in data['spells']:
            dc = int(spell['text'][4:6])
            new_dc = " DC {}".format(dc-self.level)
            spell['text'] = new_dc + spell['text'][6:]

        # replace spell attack bonus
        for spell in data['spells']:
            try:
                # get spell attack bonus if specified
                atk = int(spell['text'][16:18])
            except ValueError:
                continue
            new_atk = "attack +{}".format(atk-self.level)
            spell['text'] = spell['text'][:8] + new_atk + spell['text'][18:]

        return data['spells']

    def modify_stats(self):
        data = self.monster

        saves = re.compile('[0-9]+')
        ac = int(saves.findall(data['AC'])[0])
        fort = int(saves.findall(data['Fort'])[0])
        ref = int(saves.findall(data['Ref'])[0])
        will = int(saves.findall(data['Will'])[0])

        data['AC'] = re.sub(str(ac), str(ac - self.level), data['Fort'])
        data['Fort'] = re.sub(str(fort), str(fort - self.level), data['Fort'])
        data['Ref'] = re.sub(str(ref), str(ref - self.level), data['Ref'])
        data['Will'] = re.sub(str(will), str(will - self.level), data['Will'])

        # spells are stored as a list of dictionaries containing spells
        # if the spell list is not blank, modify it
        if data['spells']:
            data['spells'] = self.modify_spells()

        if data['skills']:
            pass


level_remover = RemoveLevels("Adult Bronze Dragon")
level_remover.modify_stats()
