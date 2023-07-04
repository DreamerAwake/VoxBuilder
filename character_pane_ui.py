import json
import character
import window as win
from vox_table_ui import VoxTable
from tkinter import filedialog, messagebox, StringVar, IntVar, END
from tkinter.ttk import Button, Entry, Frame, Label


def get_attunement_vars_dict():
    attunement_variables = {"Cerebra": IntVar(value=0),
                                 "Benedictum": IntVar(value=0),
                                 "Myomesmer": IntVar(value=0),
                                 "Psychoanima": IntVar(value=0),
                                 "Visiospatia": IntVar(value=0),
                                 "Endopulse": IntVar(value=0)}

    return attunement_variables

def init_attunements_frame(parent, attunement_vars):
    attunements_frame = Frame(parent)
    attunements_frame.grid(column=0, row=3)

    for x in range(0, 6):
        attunements_frame.columnconfigure(x, minsize=120)


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


def init_export_buttons(parent):
    buttons_frame = Frame(parent)
    buttons_frame.grid(column=0, row=5, sticky="ew")

    png_export_button = Button(buttons_frame, text="Export Voxes to .PNG", command=save_each_vox_image)
    png_export_button.grid(column=0, row=0)

    vox_export_button = Button(buttons_frame, text="Export Voxes to .VOX", command=save_each_vox_file)
    vox_export_button.grid(column=1, row=0)


def init_file_buttons(parent):
    buttons_frame = Frame(parent)
    buttons_frame.grid(column=0, row=0, sticky="ew")

    new_char_button = Button(buttons_frame, text="* New Character", command=reset_character)
    new_char_button.grid(column=0, row=0)

    load_char_button = Button(buttons_frame, text="Load Character", command=load_character)
    load_char_button.grid(column=1, row=0)

    save_char_button = Button(buttons_frame, text="Save Character", command=save_character)
    save_char_button.grid(column=2, row=0)


def init_info_frame(parent, char_name_variable):
    info_frame = Frame(parent)
    info_frame.grid(column=0, row=1, sticky="ew", pady=20)

    Label(info_frame, text="Character Name:").grid(column=0, row=0, sticky="w")
    win.init_entry_widget(info_frame, char_name_variable, win.INPUT_FONT, column=1, row=0, sticky="w")

    Label(info_frame, text="Description:").grid(column=0, row=1, sticky="w")

    description_text_box = win.init_text_widget(info_frame, win.INPUT_FONT, width=90, height=5)
    description_text_box.grid(column=1, row=1, sticky="ew")

    return info_frame, description_text_box


def load_character():
    # Load the .lotl file
    load_filepath = filedialog.askopenfilename(defaultextension=".lotl")
    # Exit if no file is selected
    if load_filepath == "":
        return

    with open(load_filepath, 'r', encoding='utf-8') as fileobject:
        character_file = json.load(fileobject)

    # Load the character object into the program
    CHARPANE.character.load_from_char_file(character_file)

    CHARPANE.read_from_character()


def reset_character():
    do_reset = messagebox.askyesno(title="* New Character",
                                   message="Are you sure you would like to discard unsaved changes and start a new character?")
    if do_reset:
        CHARPANE.reset()


def save_character():
    save_filepath = filedialog.asksaveasfilename(defaultextension=".lotl")
    if save_filepath == "":
        return

    CHARPANE.write_to_character()

    CHARPANE.character.save_json(save_filepath)


def save_each_vox_file():
    save_filepath = filedialog.asksaveasfilename()
    if save_filepath == "":
        return

    CHARPANE.write_to_character()

    for each_vox in CHARPANE.character.voxes:
        each_vox.save_json(save_filepath + each_vox.name.lower() + ".vox")


def save_each_vox_image():
    save_filepath = filedialog.asksaveasfilename()
    if save_filepath == "":
        return

    CHARPANE.write_to_character()

    for each_vox in CHARPANE.character.voxes:
        vox_image = each_vox.get_card_image(CHARPANE.attunement_variables[each_vox.attribute[0]].get())
        vox_image.save(save_filepath + each_vox.name.lower() + ".png")


class CharacterPane:
    def __init__(self):
        self.parent_frame = init_character_pane(win.ROOT)

        init_file_buttons(self.parent_frame)

        self.char_name_variable = StringVar()
        self.info_frame, self.description = init_info_frame(self.parent_frame, self.char_name_variable)

        self.attunement_variables = get_attunement_vars_dict()

        self.attunements_frame = init_attunements_frame(self.parent_frame, self.attunement_variables)

        self.character = character.Character(self.char_name_variable.get())

        self.vox_table = VoxTable(self, self.parent_frame, self.character)

        init_export_buttons(self.parent_frame)

        # A traced variable that can be triggered from the cell level and calls to load a vox.
        self.vox_awaits_load_from_table = IntVar(value=0)
        self.vox_to_load = None

    def read_from_character(self):
        """Updates the tkinter values to match those found in the character object, usually after loading."""
        self.char_name_variable.set(self.character.name)

        win.set_widget_text(self.description, self.character.description)

        for each_key in self.attunement_variables.keys():
            self.attunement_variables[each_key].set(self.character.attunements[each_key])

    def reset(self):
        self.char_name_variable.set("")

        self.character.reset()

        self.description.delete(1.0, END)

        for each_value in self.attunement_variables.values():
            each_value.set(0)

    def write_to_character(self):
        """Write necessary data to character in preparation for saving to file."""
        self.character.name = self.char_name_variable.get()

        self.character.description = self.description.get("1.0", END)

        for each_key in self.attunement_variables.keys():
            self.character.attunements[each_key] = self.attunement_variables[each_key].get()


CHARPANE = CharacterPane()
