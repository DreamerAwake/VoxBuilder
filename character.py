import json
from vox import load_from_dict

SAVE_VERSIONS = ("1.0",)


def load_from_file_1_0(char_obj, character_file):
    char_obj.name = character_file[1]
    char_obj.description = character_file[2]
    char_obj.attunements = character_file[3]
    char_obj.voxes.clear()

    for each_element in character_file[4]:
        char_obj.voxes.append(load_from_dict(each_element))


def load_from_file_legacy(char_obj, character_file):
    char_obj.name = character_file[0]
    char_obj.attunements = character_file[1]
    char_obj.voxes.clear()

    for each_element in character_file[2]:
        char_obj.voxes.append(load_from_dict(each_element))


class Character:
    def __init__(self, char_name, *voxes, **kwargs):
        self.name = char_name
        self.description = ""
        self.attunements = get_attunement_dict(**kwargs)
        self.voxes = list(voxes)

    def load_from_char_file(self, char_file):
        self.reset()
        if char_file[0] not in SAVE_VERSIONS:
            load_from_file_legacy(self, char_file)
        else:
            load_from_file_1_0(self, char_file)

    def remove_vox_with_name(self, vox_name):
        for each_vox in self.voxes:
            if vox_name == each_vox.name:
                self.voxes.remove(each_vox)
                break

    def reset(self):
        self.name = ""
        self.description = ""
        self.attunements = get_attunement_dict()
        self.voxes.clear()

    def save_json(self, filepath):
        vox_dicts = []
        for each_vox in self.voxes:
            vox_dicts.append(each_vox.save_dict())

        save_file = ("1.0", self.name, self.description, self.attunements, vox_dicts)

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
