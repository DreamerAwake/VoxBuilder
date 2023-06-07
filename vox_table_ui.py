import vox
from tkinter.ttk import Frame


def init_table_pane(parent):
    table_pane = Frame(parent)
    table_pane.grid(column=0, row=2, sticky="nsew")

    return table_pane


class VoxTable:
    def __init__(self, parent, character_obj):
        self.table_pane = init_table_pane(parent)

        self.character = character_obj

        self.sorted_voxes = None
        self.sort_voxes()

        self.vox_cells = get_vox_table_cells(self.sorted_voxes)

    def sort_voxes(self):
        sorted_voxes = [
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Cerebra"]],
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Benedictum"]],
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Myomesmer"]],
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Psychoanima"]],
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Visiospatia"]],
            [x for x in self.character.voxes if x.attribute == vox.ATTR["Endopulse"]],
        ]

        self.sorted_voxes = sorted_voxes
