import window as win
import vox
from character_pane_ui import CHARPANE
from tkinter import filedialog, messagebox, StringVar, IntVar, END
from tkinter.ttk import Button, Entry, Frame, Label, OptionMenu, Checkbutton
from PIL import Image


FILEPATH = StringVar(value="imagefiles/defaultvox.png")


def add_vox_to_character():
    add_vox = get_output_vox()

    for each_vox in CHARPANE.character.voxes:
        if add_vox.name == each_vox.name:
            do_replace = messagebox.askyesno(message=f"There is already a Vox named {add_vox.name}.\n"
                                                     f"Remove the old Vox and replace it with this one?")

            if do_replace:
                CHARPANE.character.remove_vox_with_name(add_vox.name)

            else:
                return False

    CHARPANE.character.voxes.append(add_vox)
    CHARPANE.vox_table.reset_vox_cells()


def callback_vox_table_reset(*args):
    CHARPANE.vox_table.reset_vox_cells()


def callback_table_reset_and_regenerate(*args):
    callback_vox_table_reset()
    generate_output()


def generate_output(*args, input_vox=None, unlock=False):
    """Generates the output image from the variable data and displays it."""
    if input_vox is None:
        output_vox = get_output_vox()

    else:
        output_vox = input_vox

    if unlock:
        VOXPANE.lock_generator = False

    if not VOXPANE.lock_generator:
        vox_attribute = VOXPANE.vox_attribute_variable.get()

        VOXPANE.output_full_size = output_vox.get_card_image(CHARPANE.attunement_variables[vox_attribute].get())

        VOXPANE.output_image_label, VOXPANE.output_image = win.init_displayed_image(VOXPANE.bottom_frame,
                                                                                    image=VOXPANE.output_full_size,
                                                                                    columnspan=3,
                                                                                    pady=20)

    return output_vox


def get_output_vox():
    """Generates a vox object from the current pane state."""
    actions = []
    for each_action in (VOXPANE.action_1, VOXPANE.action_2, VOXPANE.action_3):

        if len(each_action.get("1.0", END).split()) > 0:
            actions.append(each_action.get("1.0", END))

    if VOXPANE.vox_signature_variable.get() > 0:
        is_signature_vox = True
    else:
        is_signature_vox = False

    output_vox_attribute = VOXPANE.vox_attribute_variable.get()

    output_vox = vox.Vox(VOXPANE.vox_name_variable.get(),
                         vox.ATTR[output_vox_attribute],
                         VOXPANE.vox_goal.get("1.0", END),
                         VOXPANE.vox_ranks.get(), is_signature_vox,
                         *actions,
                         vox_filepath=FILEPATH.get()
                         )

    return output_vox


def init_attribute_frame(parent, vox_attribute_var, column, row):
    attribute_frame = Frame(parent)
    attribute_frame.grid(column=column, row=row, sticky="w")
    attribute_frame.columnconfigure(0, weight=1)
    attribute_frame.columnconfigure(1, weight=0)
    attribute_frame.columnconfigure(2, weight=0)
    attribute_frame.columnconfigure(3, weight=0)

    # Create the content
    init_dropdown(attribute_frame, vox_attribute_var, column=0, row=0)

    subtract_button = Button(attribute_frame, text="-", command=subtract_1_attribute, width=1)
    subtract_button.grid(column=1, row=0)

    init_attribute_entry(attribute_frame, vox_attribute_var)

    add_button = Button(attribute_frame, text="+", command=add_1_attribute, width=1)
    add_button.grid(column=3, row=0)

    return attribute_frame


def add_1_attribute():
    win.intvar_plus_1(CHARPANE.attunement_variables[VOXPANE.vox_attribute_variable.get()])


def subtract_1_attribute():
    win.intvar_minus_1(CHARPANE.attunement_variables[VOXPANE.vox_attribute_variable.get()])


def init_attribute_entry(parent, vox_attribute_var):

    attribute_value_display = Entry(parent,
                                    textvariable=CHARPANE.attunement_variables[vox_attribute_var.get()],
                                    font=win.INPUT_FONT,
                                    width=2)
    attribute_value_display.config(state="readonly")
    attribute_value_display.grid(column=2, row=0, sticky="ew")


def init_checkbox(parent, variable, text, **kwargs):
    """Creates the checkboxes in the window."""
    extend_rules_checkbox = Checkbutton(parent, text=text, variable=variable, onvalue=1, offvalue=0)
    extend_rules_checkbox.grid(**kwargs)


def init_dropdown(parent, variable, column, row):
    dropdown_menu = OptionMenu(parent, variable, "Benedictum", *vox.ATTR.keys())
    dropdown_menu.grid(column=column, row=row)


def init_entry_pane(window, vox_name_var, vox_attribute_var, vox_ranks_var, vox_signature_var):
    """Creates the entry pane in the middle of the screen that collects the user input."""
    main_frame = Frame(window)
    main_frame.grid(column=1, row=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=0)
    main_frame.columnconfigure(1, weight=1)

    # Create all the labels
    Label(main_frame, text="Vox Name:").grid(column=0, row=0)
    Label(main_frame, text="Vox Attribute:").grid(column=0, row=1)
    Label(main_frame, text="Vox Ranks:").grid(column=0, row=2)
    Label(main_frame, text="Vox Goal:").grid(column=0, row=3)
    Label(main_frame, text="Action 1:").grid(column=0, row=4)
    Label(main_frame, text="Action 2:").grid(column=0, row=5)
    Label(main_frame, text="Action 3:").grid(column=0, row=6)

    # Create frames and widgets
    win.init_entry_widget(main_frame, vox_name_var, win.INPUT_FONT, column=1, row=0, sticky="w")
    attribute_frame = init_attribute_frame(main_frame, vox_attribute_var, column=1, row=1)
    init_ranks_frame(main_frame, vox_ranks_var, vox_signature_var, column=1, row=2)
    goal_widget = win.init_text_widget(main_frame, win.INPUT_FONT, 40, 3, column=1, row=3, sticky="w")
    action_1_widget = win.init_text_widget(main_frame, win.INPUT_FONT, 60, 4, column=1, row=4, sticky="nsew", columnspan=2)
    action_2_widget = win.init_text_widget(main_frame, win.INPUT_FONT, 60, 4, column=1, row=5, sticky="nsew", columnspan=2)
    action_3_widget = win.init_text_widget(main_frame, win.INPUT_FONT, 60, 4, column=1, row=6, sticky="nsew", columnspan=2)

    clear_button = Button(main_frame, text="* New Vox", command=load_blank_vox)
    clear_button.grid(column=2, row=0)

    return main_frame, attribute_frame, goal_widget, action_1_widget, action_2_widget, action_3_widget


def init_file_select_pane(window):
    """Creates the collection of frames that display and select the vox portrait."""
    # Create the frame itself and set its weights to the correct values
    file_select_frame = Frame(window)
    file_select_frame.grid(column=0, row=0, sticky="nsew")
    file_select_frame.rowconfigure(0, weight=1)
    file_select_frame.rowconfigure(1, weight=0)
    file_select_frame.columnconfigure(0, weight=1)
    file_select_frame.columnconfigure(1, weight=0)

    # Create the display entry for the filepath selector
    file_select_entry = Entry(file_select_frame, textvariable=FILEPATH, font=win.INPUT_FONT)
    file_select_entry.config(state="readonly")
    file_select_entry.grid(column=0, row=2, sticky="ew", columnspan=2)

    # Fetch and display the image
    image_label, image = win.init_displayed_image(file_select_frame, filepath=FILEPATH.get(), image_scale=0.35, columnspan=2)

    # Create the button that searches for the filepath
    file_search_button = Button(file_select_frame, text="Load Portrait Image", command=select_new_filepath)
    file_search_button.grid(column=0, row=1)

    # Create the button that loads a vox from file
    load_vox_button = Button(file_select_frame, text="Load Vox File", command=load_vox)
    load_vox_button.grid(column=1, row=1)

    return file_select_frame, image_label, image


def init_output_pane(window):
    """Creates the output image pane."""
    output_frame = Frame(window)
    output_frame.grid(column=0, row=1, columnspan=2)
    output_frame.rowconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=0)

    image_label, image = win.init_displayed_image(output_frame, filepath="imagefiles/EXAMPLE.png", columnspan=3, pady=20)

    add_button = Button(output_frame, text="Add to character", command=add_vox_to_character)
    add_button.grid(column=0, row=1)

    save_button = Button(output_frame, text="Save to file", command=save_vox)
    save_button.grid(column=1, row=1)

    export_button = Button(output_frame, text="Export PNG", command=save_output)
    export_button.grid(column=2, row=1)

    return output_frame, image_label, image


def init_ranks_frame(parent, vox_ranks_var, vox_signature_var, column, row):
    ranks_frame = Frame(parent)
    ranks_frame.grid(column=column, row=row, sticky="w")
    ranks_frame.columnconfigure(0, weight=1)
    ranks_frame.columnconfigure(1, weight=1)
    ranks_frame.columnconfigure(2, weight=1)

    # Create the content
    subtract_button = Button(ranks_frame, text="-", command=subtract_1_rank, width=1)
    subtract_button.grid(column=1, row=0)

    attribute_value_display = Entry(ranks_frame, textvariable=vox_ranks_var, font=win.INPUT_FONT, width=2)
    attribute_value_display.config(state="readonly")
    attribute_value_display.grid(column=2, row=0, sticky="ew")

    add_button = Button(ranks_frame, text="+", command=add_1_rank, width=1)
    add_button.grid(column=3, row=0)

    init_checkbox(ranks_frame, vox_signature_var, "Signature Skill", column=4, row=0, sticky="e")


def add_1_rank():
    VOXPANE.vox_ranks.set(VOXPANE.vox_ranks.get() + 1)


def subtract_1_rank():
    current_value = VOXPANE.vox_ranks.get()
    if current_value > 1:
        VOXPANE.vox_ranks.set(current_value - 1)


def init_vox_pane(window):
    """Creates an empty parent frame for the other content frames to occupy."""
    content_frame = Frame(window, padding=20)
    content_frame.grid(column=1, row=0, sticky="nsew")

    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)
    content_frame.columnconfigure(2, weight=2)

    return content_frame


def load_from_callback(*args):
    # Value 1 indicates a full load from the right click -> edit menu
    if CHARPANE.vox_awaits_load_from_table.get() == 1:
        CHARPANE.vox_awaits_load_from_table.set(0)
        VOXPANE.read_from_vox(CHARPANE.vox_to_load)
        CHARPANE.vox_to_load = None

    # Value 2 indicates that only the generated image should be replaced, from left click inspect
    elif CHARPANE.vox_awaits_load_from_table.get() == 2:
        CHARPANE.vox_awaits_load_from_table.set(0)
        generate_output(input_vox=CHARPANE.vox_to_load)
        CHARPANE.vox_to_load = None

def load_blank_vox():
    do_reset = messagebox.askyesno(title="* New Vox",
                                   message="Are you sure you would like to discard unsaved changes and start a new Vox?")
    if do_reset:
        blank_vox = vox.Vox("", vox.ATTR["Benedictum"], "", 1, False)

        VOXPANE.read_from_vox(blank_vox)

def load_vox():
    # Load the .vox file
    load_filepath = filedialog.askopenfilename(defaultextension=".vox")
    # Exit if no file is selected
    if load_filepath == "":
        return

    # Load a vox object from the .vox
    loaded_vox = vox.load_from_json(load_filepath)

    # Set basic parameters in the window to match the loaded vox
    VOXPANE.read_from_vox(loaded_vox)


def on_text_modification(*args, **kwargs):
    """Runs when a text widget is changed."""
    VOXPANE.vox_goal.edit_modified(False)
    VOXPANE.action_1.edit_modified(False)
    VOXPANE.action_2.edit_modified(False)
    VOXPANE.action_3.edit_modified(False)
    generate_output(*args, **kwargs)


def save_output():
    """Saves the output image to a file."""
    output_filepath = filedialog.asksaveasfilename(defaultextension=".png")
    if output_filepath == "":
        return

    generate_output()

    VOXPANE.output_full_size.save(output_filepath)


def save_vox():
    save_filepath = filedialog.asksaveasfilename(defaultextension=".vox")
    if save_filepath == "":
        return

    generated_vox = generate_output()

    generated_vox.save_json(save_filepath)


def select_new_filepath():
    """Selects a new filepath for the vox portrait."""
    new_filepath = filedialog.askopenfilename(parent=win.ROOT, title="Select Vox portrait...")
    if new_filepath == "":
        return

    portrait_image = Image.open(new_filepath)

    if portrait_image.width <= 512 and portrait_image.height <= 768:
        FILEPATH.set(new_filepath)
        update_loaded_portrait()
    else:
        messagebox.showwarning(title="Wrong File Size",
                               message="The selected image is too large. Please select a Vox portrait that is no larger than 512x768 pixels.")


def set_widget_text(text_widget, value):
    """Overwrites a tkinter text widget's contents with the passed value."""
    text_widget.delete(1.0, END)
    text_widget.insert(END, value)


def update_attribute_intvar(*args):
    """Updates the intvar associated with the attribute selector via trace call."""
    try:
        init_attribute_entry(VOXPANE.attribute_frame, VOXPANE.vox_attribute_variable)
    except NameError:
        pass


def update_loaded_portrait():
    """Updates the portrait selector by loading from the FILEPATH"""

    VOXPANE.portrait_image_label, VOXPANE.portrait_image = win.init_displayed_image(VOXPANE.left_frame,
                                                                                filepath=FILEPATH.get(),
                                                                                image_scale=0.35,
                                                                                columnspan=2)


class VoxPane:
    def __init__(self):
        self.lock_generator = False  # Lock out for the image generator to prevent excess rendering
        
        self.parent_frame = init_vox_pane(win.ROOT)

        self.left_frame, self.portrait_image_label, self.portrait_image = init_file_select_pane(self.parent_frame)

        self.vox_name_variable = StringVar()
        self.vox_attribute_variable = StringVar()
        self.vox_attribute_variable.trace_add('write', update_attribute_intvar)
        self.vox_ranks = IntVar(value=1)
        self.vox_signature_variable = IntVar(value=0)
        self.right_frame, self.attribute_frame, self.vox_goal, self.action_1, self.action_2, self.action_3 = \
            init_entry_pane(self.parent_frame, self.vox_name_variable, self.vox_attribute_variable, self.vox_ranks, self.vox_signature_variable)

        self.bottom_frame, self.output_image_label, self.output_image = init_output_pane(self.parent_frame)

        self.output_full_size = None

    def read_from_vox(self, vox_obj):
        self.lock_generator = True  # Lock the image generator to prevent excess rendering

        self.vox_name_variable.set(vox_obj.name)
        self.vox_attribute_variable.set(vox_obj.attribute[0])
        set_widget_text(self.vox_goal, vox_obj.goal)
        self.vox_ranks.set(vox_obj.ranks)
        FILEPATH.set(vox_obj.image_filepath)

        # Set up the flags of the signature skill checkbox
        if vox_obj.is_signature is True:
            self.vox_signature_variable.set(1)
        else:
            self.vox_signature_variable.set(0)

        # Apply loaded actions, step 1: we need a tuple of the action text boxes from the UI
        action_widgets = self.action_1, self.action_2, self.action_3

        # Clear out the values in the text boxes
        for each_widget in action_widgets:
            each_widget.delete(1.0, END)

        # Apply the new ones
        for each_widget, each_action in zip(action_widgets, vox_obj.actions):
            set_widget_text(each_widget, each_action)

        # Re-update the generated Vox image
        generate_output(unlock=True)

        # update the vox portrait in the file selector
        update_loaded_portrait()


VOXPANE = VoxPane()
CHARPANE.vox_awaits_load_from_table.trace_add('write', load_from_callback)  # Create the trace for the open vox right click

# Create the re-generate traces for the vox variables
VOXPANE.vox_name_variable.trace('w', generate_output)
VOXPANE.vox_attribute_variable.trace('w', generate_output)
VOXPANE.vox_ranks.trace('w', generate_output)
VOXPANE.vox_signature_variable.trace('w', generate_output)
FILEPATH.trace('w', generate_output)
VOXPANE.vox_goal.bind('<<Modified>>', on_text_modification)
VOXPANE.action_1.bind('<<Modified>>', on_text_modification)
VOXPANE.action_2.bind('<<Modified>>', on_text_modification)
VOXPANE.action_3.bind('<<Modified>>', on_text_modification)


for each_value in CHARPANE.attunement_variables.values():
    each_value.trace_add('write', callback_table_reset_and_regenerate)
