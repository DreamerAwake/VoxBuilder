import vox
from math import floor
from tkinter import filedialog, StringVar, IntVar, Text, END
from tkinter import Label as tkLabel
from tkinter.ttk import Button, Entry, Frame, Label, OptionMenu, Checkbutton
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


def init_tk_window(min_size=(800, 900)):
    """Initializes a tkinter Tk, returns it."""
    window_frame = ThemedTk(theme='yaru')
    window_frame.title("LotLVoxBuilder")

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=1)

    window_frame.minsize(*min_size)

    return window_frame

ROOT = init_tk_window()
INPUT_FONT = ("Arial", 10)
FILEPATH = StringVar(value="imagefiles/defaultvox.png")
ATTRVAR = IntVar(value=1)

def generate_output():
    """Generates the output image from the variable data and displays it."""
    actions = []
    for each_action in (TKWINDOW.action_1, TKWINDOW.action_2, TKWINDOW.action_3):

        if len(each_action.get("1.0", END).split()) > 0:
            actions.append(each_action.get("1.0", END))

    if TKWINDOW.vox_signature_variable.get() > 0:
        is_signature_vox = True
    else:
        is_signature_vox = False

    output_vox = vox.Vox(TKWINDOW.vox_name_variable.get(),
                         vox.ATTR[TKWINDOW.vox_attribute_variable.get()],
                         TKWINDOW.vox_goal.get("1.0", END),
                         TKWINDOW.vox_ranks.get(), is_signature_vox,
                         *actions,
                         vox_filepath=FILEPATH.get()
                         )

    TKWINDOW.output_full_size = output_vox.get_card_image(ATTRVAR.get())

    TKWINDOW.output_image_label, TKWINDOW.output_image = init_displayed_image(TKWINDOW.bottom_frame,
                                                                              image=TKWINDOW.output_full_size,
                                                                              columnspan=3)

    return output_vox


def init_displayed_image(parent, image=None, filepath=None, image_scale=0.5, column=0, row=0, columnspan=0):
    """Creates the displayed image label and returns it with a basic placeholder image inside.
    May accept an ImageTK for display."""
    if image is None:
        if filepath is None:
            image = Image.open("imagefiles/defaultvox.png")
        else:
            image = Image.open(filepath)

    image = image.resize((floor(image.width * image_scale), floor(image.height * image_scale)))
    image = ImageTk.PhotoImage(image)
    image_label = tkLabel(parent, image=image)

    if columnspan > 1:
        image_label.grid(column=column, row=row, columnspan=columnspan)
    else:
        image_label.grid(column=column, row=row)

    return image_label, image


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
    init_entry_widget(main_frame, vox_name_var, INPUT_FONT, column=1, row=0, sticky="w")
    init_attribute_frame(main_frame, vox_attribute_var, column=1, row=1)
    init_ranks_frame(main_frame, vox_ranks_var, vox_signature_var, column=1, row=2)
    goal_widget = init_text_widget(main_frame, INPUT_FONT, 40, 3, column=1, row=3, sticky="w")
    action_1_widget = init_text_widget(main_frame, INPUT_FONT, 60, 4, column=1, row=4, sticky="nsew")
    action_2_widget = init_text_widget(main_frame, INPUT_FONT, 60, 4, column=1, row=5, sticky="nsew")
    action_3_widget = init_text_widget(main_frame, INPUT_FONT, 60, 4, column=1, row=6, sticky="nsew")


    return main_frame, goal_widget, action_1_widget, action_2_widget, action_3_widget


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

    attribute_value_display = Entry(attribute_frame, textvariable=ATTRVAR, font=('Arial', 10), width=2)
    attribute_value_display.config(state="readonly")
    attribute_value_display.grid(column=2, row=0, sticky="ew")

    add_button = Button(attribute_frame, text="+", command=add_1_attribute, width=1)
    add_button.grid(column=3, row=0)


def init_ranks_frame(parent, vox_ranks_var, vox_signature_var, column, row):
    ranks_frame = Frame(parent)
    ranks_frame.grid(column=column, row=row, sticky="w")
    ranks_frame.columnconfigure(0, weight=1)
    ranks_frame.columnconfigure(1, weight=1)
    ranks_frame.columnconfigure(2, weight=1)

    # Create the content
    subtract_button = Button(ranks_frame, text="-", command=subtract_1_rank, width=1)
    subtract_button.grid(column=1, row=0)

    attribute_value_display = Entry(ranks_frame, textvariable=vox_ranks_var, font=('Arial', 10), width=2)
    attribute_value_display.config(state="readonly")
    attribute_value_display.grid(column=2, row=0, sticky="ew")

    add_button = Button(ranks_frame, text="+", command=add_1_rank, width=1)
    add_button.grid(column=3, row=0)

    init_checkbox(ranks_frame, vox_signature_var, "Signature Skill", column=4, row=0, sticky="e")


def init_checkbox(parent, variable, text, **kwargs):
    """Creates the checkboxes in the window."""
    extend_rules_checkbox = Checkbutton(parent, text=text, variable=variable, onvalue=1, offvalue=0)
    extend_rules_checkbox.grid(**kwargs)


def init_dropdown(parent, variable, column, row):
    dropdown_menu = OptionMenu(parent, variable, "Intellect", *vox.ATTR.keys())
    dropdown_menu.grid(column=column, row=row)


def init_entry_widget(parent, variable, font, **kwargs):
    """Create an entry widget."""
    title_entry = Entry(parent, width=40, textvariable=variable, font=font)
    title_entry.grid(**kwargs)


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

    file_select_entry = Entry(file_select_frame, textvariable=FILEPATH, font=('Arial', 10))
    file_select_entry.config(state="readonly")
    file_select_entry.grid(column=0, row=1, sticky="ew")

    # Fetch and display the image
    image_label, image = init_displayed_image(file_select_frame, filepath=FILEPATH.get(), columnspan=2)

    # Create the button that searches for the filepath
    file_search_button = Button(file_select_frame, text="Browse", command=select_new_filepath)
    file_search_button.grid(column=1, row=1)

    # Create the button that loads a vox from file
    load_vox_button = Button(file_select_frame, text="Load .vox file", command=load_vox)
    load_vox_button.grid(column=1, row=2)

    return file_select_frame, image_label, image


def init_output_pane(window):
    """Creates the output image pane."""
    output_frame = Frame(window)
    output_frame.grid(column=0, row=1, columnspan=2)
    output_frame.rowconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=0)

    image_label, image = init_displayed_image(output_frame, filepath="imagefiles/EXAMPLE.png", columnspan=3)

    output_button = Button(output_frame, text="Generate", command=generate_output)
    output_button.grid(column=0, row=1)

    save_button = Button(output_frame, text="Save Vox", command=save_vox)
    save_button.grid(column=1, row=1)

    export_button = Button(output_frame, text="Export PNG", command=save_output)
    export_button.grid(column=2, row=1)



    return output_frame, image_label, image


def init_parent_frame(window):
    """Creates an empty parent frame for the other content frames to occupy."""
    content_frame = Frame(window, padding=20)
    content_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)
    content_frame.columnconfigure(2, weight=2)

    return content_frame


def init_text_widget(parent, font, width, height, **kwargs):
    """Creates the flavor text input widget"""
    text_widget = Text(parent, width=width, height=height, wrap="word", font=font)
    text_widget.grid(**kwargs)

    return text_widget


def save_output():
    """Saves the output image to a file."""
    generate_output()

    output_filepath = filedialog.asksaveasfilename(defaultextension=".png")

    TKWINDOW.output_full_size.save(output_filepath)


def save_vox():
    generated_vox = generate_output()

    save_filepath = filedialog.asksaveasfilename(defaultextension=".vox")

    generated_vox.save_json(save_filepath)


def load_vox():
    load_filepath = filedialog.askopenfilename(defaultextension=".vox")

    loaded_vox = vox.load_from_json(load_filepath)

    TKWINDOW.vox_name_variable.set(loaded_vox.name)
    TKWINDOW.vox_attribute_variable.set(loaded_vox.attribute[0])
    set_widget_text(TKWINDOW.vox_goal, loaded_vox.goal)
    TKWINDOW.vox_ranks.set(loaded_vox.ranks)
    FILEPATH.set(loaded_vox.image_filepath)

    if loaded_vox.is_signature is True:
        TKWINDOW.vox_signature_variable.set(1)
    else:
        TKWINDOW.vox_signature_variable.set(0)

    action_widgets = TKWINDOW.action_1, TKWINDOW.action_2, TKWINDOW.action_3

    for each_widget in action_widgets:
        each_widget.delete(1.0, END)

    for each_widget, each_action in zip(action_widgets, loaded_vox.actions):
        set_widget_text(each_widget, each_action)


def select_new_filepath():
    """Selects a new filepath for the vox portrait."""
    new_filepath = filedialog.askopenfilename(parent=TKWINDOW.window, title="Select Vox portrait...", initialdir="imagefiles")
    FILEPATH.set(new_filepath)
    TKWINDOW.portrait_image_label, TKWINDOW.portrait_image = init_displayed_image(TKWINDOW.left_frame, filepath=new_filepath, columnspan=2)


def add_1_attribute():
    ATTRVAR.set(ATTRVAR.get() + 1)


def subtract_1_attribute():
    current_value = ATTRVAR.get()
    if current_value > 0:
        ATTRVAR.set(current_value - 1)


def add_1_rank():
    TKWINDOW.vox_ranks.set(TKWINDOW.vox_ranks.get() + 1)


def subtract_1_rank():
    current_value = TKWINDOW.vox_ranks.get()
    if current_value > 1:
        TKWINDOW.vox_ranks.set(current_value - 1)


def set_widget_text(text_widget, value):
    """Overwrites a tkinter text widget's contents with the passed value."""
    text_widget.delete(1.0, END)
    text_widget.insert(END, value)


class TkWindow:
    def __init__(self):
        self.window = ROOT
        self.parent_frame = init_parent_frame(self.window)

        self.left_frame, self.portrait_image_label, self.portrait_image = init_file_select_pane(self.parent_frame)

        self.vox_name_variable = StringVar()
        self.vox_attribute_variable = StringVar()
        self.vox_ranks = IntVar(value=1)
        self.vox_signature_variable = IntVar(value=0)
        self.right_frame, self.vox_goal, self.action_1, self.action_2, self.action_3 = \
            init_entry_pane(self.parent_frame, self.vox_name_variable, self.vox_attribute_variable, self.vox_ranks, self.vox_signature_variable)

        self.bottom_frame, self.output_image_label, self.output_image = init_output_pane(self.parent_frame)

        self.output_full_size = None


TKWINDOW = TkWindow()

if __name__ == "__main__":
    TKWINDOW.window.mainloop()
