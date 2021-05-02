import pickle


class RemoveLevels:
    def __init__(self, monster):
        self.monster = monster
        with open('pf2e_bestiary.pickle', 'rb') as f:
            self.monster_dict = pickle.load(f)
            f.close()

        if monster in self.monster_dict:
            self.level = self.monster_dict[monster]["level"]
        else:
            raise KeyError

    def modded_monster(self):
        data = self.monster_dict[self.monster]
        # TODO regex the scores to modify them properly

    def __str__(self):
        print("")


level_remover = RemoveLevels("Adult Bronze Dragon")
