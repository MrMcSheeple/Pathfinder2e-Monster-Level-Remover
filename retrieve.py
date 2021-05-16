import requests
import pickle


def get_data():
    url = "https://raw.githubusercontent.com/jimbarnesrtp/pf2/master/monsters-v2-pf2.json"
    raw_data = requests.get(url).json()["monsters"]

    return raw_data


def write_pickle():
    data = get_data()

    names = [d["name"] for d in data]
    data_list = [d for d in data]

    pf2e_monsters = dict(zip(names, data_list))

    with open('pf2e_bestiary.pickle', 'wb') as f:
        pickle.dump(pf2e_monsters, f)
        f.close()
