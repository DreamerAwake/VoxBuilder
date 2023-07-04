import window as win
from tkinter import messagebox, Menu
from tkextensions import tkscrollableframe as tkscroll


def get_vox_table_cells(char_pane, table_pane, sorted_voxes):
    table_cells = []
    current_row = 0
    current_column = 0

    for each_list in sorted_voxes:
        for each_vox in each_list:
            table_cells.append(VoxCell(table_pane,
                                       current_column,
                                       current_row,
                                       each_vox,
                                       char_pane))
            current_row += 1
        current_row = 0
        current_column += 1

    return table_cells


def get_voxes_of_attribute(vox_list, attribute_name):
    non_sig_list = [x for x in vox_list if x.is_attr(attribute_name) and not x.is_signature]
    non_sig_list.sort()

    sig_list = [x for x in vox_list if x.is_attr(attribute_name) and x.is_signature]
    sig_list.sort()

    return sig_list + non_sig_list


def init_table_pane(parent):
    scroll_canvas = tkscroll.ScrollFrame(parent)
    parent.rowconfigure(4, minsize=500)
    parent.columnconfigure(0, minsize=738)
    scroll_canvas.grid(column=0, row=4, sticky="nsew", pady=10)

    for x in range(0, 6):
        scroll_canvas.viewPort.columnconfigure(x, minsize=120)

    return scroll_canvas.viewPort


def open_right_click_menu(*args):
    rclick_menu = Menu(win.ROOT, tearoff=0)

    rclick_menu.add_command(label="Open", command=lambda: set_await_vox_load(*args))
    rclick_menu.add_command(label="Delete", command=lambda: remove_vox_dialog(*args))

    rclick_menu.tk_popup(args[2].x_root, args[2].y_root)


def remove_vox_dialog(*args):
    """Opens a dialog that asks if the user would like to remove the clicked vox, if yes, does so."""
    vox_obj = args[0]
    char_pane = args[1]

    do_remove = messagebox.askyesno(message=f"Remove the Vox {vox_obj.name} from the character?")

    if do_remove:
        char_pane.character.remove_vox_with_name(vox_obj.name)
        char_pane.vox_table.reset_vox_cells()
    else:
        pass


def set_await_vox_load(*args):
    args[1].vox_to_load = args[0]
    args[1].vox_awaits_load_from_table.set(1)


def view_fullsize_vox(*args):
    args[1].vox_to_load = args[0]
    args[1].vox_awaits_load_from_table.set(2)


class VoxTable:
    def __init__(self, char_pane_obj, parent, character_obj):
        self.char_pane = char_pane_obj
        self.parent = parent
        self.table_pane = init_table_pane(parent)

        self.character = character_obj

        self.sorted_voxes = None
        self.vox_cells = None

        self.reset_vox_cells()

    def reset_vox_cells(self):
        self.sort()

        self.table_pane = init_table_pane(self.parent)

        self.vox_cells = get_vox_table_cells(self.char_pane,
                                             self.table_pane,
                                             self.sorted_voxes)


    def sort(self):

        # Create lists for each attribute, exclude signature skills for now
        sorted_voxes = [
            get_voxes_of_attribute(self.character.voxes, "Benedictum"),
            get_voxes_of_attribute(self.character.voxes, "Cerebra"),
            get_voxes_of_attribute(self.character.voxes, "Endopulse"),
            get_voxes_of_attribute(self.character.voxes, "Myomesmer"),
            get_voxes_of_attribute(self.character.voxes, "Psychoanima"),
            get_voxes_of_attribute(self.character.voxes, "Visiospatia"),
        ]

        self.sorted_voxes = sorted_voxes


class VoxCell:
    """A single cell in the vox table, containing the vox mini image."""
    def __init__(self, table_pane, column, row, vox_obj, char_pane):
        self.vox = vox_obj

        self.cell_label, self.image = win.init_displayed_image(table_pane,
                                                               vox_obj.get_mini_popout_image(char_pane.attunement_variables[self.vox.attribute[0]].get()),
                                                               image_scale=0.20,
                                                               column=column,
                                                               row=row)

        self.cell_label.bind("<Button-3>", lambda event: open_right_click_menu(self.vox, char_pane, event))
        self.cell_label.bind("<Button-1>", lambda event: view_fullsize_vox(self.vox, char_pane, event))

