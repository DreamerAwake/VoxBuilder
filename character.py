class Character:
    def __init__(self, char_name, *voxes, **kwargs):
        self.name = char_name
        self.attunements = get_attunement_dict(**kwargs)
        self.voxes = voxes


def get_attunement_dict(cerebra=0, benedictum=0, myomesmer=0, psychoanima=0, visiospatia=0, endopulse=0):
    return {"Cerebra": cerebra,
            "Benedictum": benedictum,
            "Myomesmer": myomesmer,
            "Psychoanima": psychoanima,
            "Visiospatia": visiospatia,
            "Endopulse": endopulse}
