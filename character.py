import json
from vox import load_from_dict


class Character:
    def __init__(self, char_name, *voxes, **kwargs):
        self.name = char_name
        self.attunements = get_attunement_dict(**kwargs)
        self.voxes = list(voxes)

    def load_from_char_file(self, char_file):
        self.name = char_file[0]
        self.attunements = char_file[1]
        self.voxes.clear()

        for each_element in char_file[2]:
            self.voxes.append(load_from_dict(each_element))

    def remove_vox_with_name(self, vox_name):
        for each_vox in self.voxes:
            if vox_name == each_vox.name:
                self.voxes.remove(each_vox)
                break

    def reset(self):
        self.name = ""
        self.attunements = get_attunement_dict()
        self.voxes.clear()

    def save_json(self, filepath):
        vox_dicts = []
        for each_vox in self.voxes:
            vox_dicts.append(each_vox.save_dict())

        save_file = (self.name, self.attunements, vox_dicts)

        print(save_file)

        with open(filepath, 'w', encoding='utf-8') as fileobject:
            json.dump(save_file, fileobject)


def get_attunement_dict(cerebra=0, benedictum=0, myomesmer=0, psychoanima=0, visiospatia=0, endopulse=0):
    return {"Cerebra": cerebra,
            "Benedictum": benedictum,
            "Myomesmer": myomesmer,
            "Psychoanima": psychoanima,
            "Visiospatia": visiospatia,
            "Endopulse": endopulse}
