import character
import window as win
from vox_table_ui import VoxTable
from tkinter import StringVar, IntVar
from tkinter.ttk import Button, Entry, Frame, Label


def init_attunements_frame(parent, attunement_vars):
    attunements_frame = Frame(parent)
    attunements_frame.grid(column=0, row=1)

    attunement_dict_keys = sorted(attunement_vars.keys())

    place_in_column = 0

    for each_key in attunement_dict_keys:
        init_attunement_widget(attunements_frame, each_key, attunement_vars[each_key], column=place_in_column, row=0)
        place_in_column += 1

    return attunements_frame


def init_attunement_widget(parent, attribute_name, attribute_var, **kwargs):
    widget_frame = Frame(parent)
    widget_frame.grid(**kwargs)

    # Place the label
    Label(widget_frame, text=attribute_name).grid(column=0, row=0, columnspan=2)

    # Place the entry widget
    attribute_entry = Entry(widget_frame, width=2, textvariable=attribute_var, font=win.INPUT_FONT_EXPANDED, justify="center")
    attribute_entry.grid(column=0, row=1, columnspan=2)

    # Place Buttons
    subtract_button = Button(widget_frame, text="-", command=lambda: win.intvar_minus_1(attribute_var), width=1)
    subtract_button.grid(column=0, row=2)

    add_button = Button(widget_frame, text="+", command=lambda: win.intvar_plus_1(attribute_var), width=1)
    add_button.grid(column=1, row=2)


def init_character_pane(window):
    """Creates an empty parent frame for the other content frames to occupy."""
    content_frame = Frame(window, padding=20)
    content_frame.grid(column=0, row=0, sticky="nsew")

    return content_frame


def init_name_frame(parent, char_name_variable):
    name_frame = Frame(parent)
    name_frame.grid(column=0, row=0, sticky="ew")

    Label(name_frame, text="Character Name:").grid(column=0, row=0)
    win.init_entry_widget(name_frame, char_name_variable, win.INPUT_FONT, column=1, row=0, sticky="w")

    return name_frame



class CharacterPane:
    def __init__(self):
        self.parent_frame = init_character_pane(win.ROOT)

        self.char_name_variable = StringVar()
        self.name_frame = init_name_frame(self.parent_frame, self.char_name_variable)

        self.attunement_variables = {"Cerebra": IntVar(value=0),
                                     "Benedictum": IntVar(value=0),
                                     "Myomesmer": IntVar(value=0),
                                     "Psychoanima": IntVar(value=0),
                                     "Visiospatia": IntVar(value=0),
                                     "Endopulse": IntVar(value=0)}

        self.attunements_frame = init_attunements_frame(self.parent_frame, self.attunement_variables)

        self.character = character.Character(self.char_name_variable.get())

        self.vox_table = VoxTable(self.parent_frame, self.character)


CHARPANE = CharacterPane()