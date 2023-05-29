import vox
from math import floor
from tkinter import filedialog, StringVar, Text, END
from tkinter import Label as tkLabel
from tkinter.ttk import Button, Entry, Frame, Label, OptionMenu
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


def init_tk_window(min_size=(1100, 600)):
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


def generate_output():
    """Generates the output image from the variable data and displays it."""
    actions = []
    for each_action in (TKWINDOW.action_1, TKWINDOW.action_2, TKWINDOW.action_3):

        if len(each_action.get("1.0", END).split()) > 0:
            actions.append(each_action.get("1.0", END))


    output_vox = vox.Vox(TKWINDOW.vox_name_variable.get(),
                         vox.ATTR[TKWINDOW.vox_attribute_variable.get()],
                         TKWINDOW.vox_goal.get("1.0", END),
                         *actions,
                         vox_filepath=FILEPATH.get()
                         )

    image = output_vox.get_card_image()

    TKWINDOW.output_image_label, TKWINDOW.output_image = init_displayed_image(TKWINDOW.right_frame, image=image, columnspan=2)


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


def init_entry_pane(window, vox_name_var, vox_attribute_var):
    """Creates the entry pane in the middle of the screen that collects the user input."""
    main_frame = Frame(window)
    main_frame.grid(column=1, row=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=0)
    main_frame.columnconfigure(1, weight=1)

    # Create all the labels
    Label(main_frame, text="Vox Name:").grid(column=0, row=0)
    Label(main_frame, text="Vox Attribute:").grid(column=0, row=1)
    Label(main_frame, text="Vox Goal:").grid(column=0, row=2)
    Label(main_frame, text="Action 1:").grid(column=0, row=3)
    Label(main_frame, text="Action 2:").grid(column=0, row=4)
    Label(main_frame, text="Action 3:").grid(column=0, row=5)

    init_entry_widget(main_frame, vox_name_var, INPUT_FONT, column=1, row=0)
    init_dropdown(main_frame, vox_attribute_var, column=1, row=1)
    goal_widget = init_text_widget(main_frame, INPUT_FONT, column=1, row=2)
    action_1_widget = init_text_widget(main_frame, INPUT_FONT, column=1, row=3)
    action_2_widget = init_text_widget(main_frame, INPUT_FONT, column=1, row=4)
    action_3_widget = init_text_widget(main_frame, INPUT_FONT, column=1, row=5)

    return main_frame, goal_widget, action_1_widget, action_2_widget, action_3_widget


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
    image_label, image = init_displayed_image(file_select_frame, filepath=FILEPATH.get())

    # Create the button that searches for the filepath
    file_search_button = Button(file_select_frame, text="Browse", command=select_new_filepath)
    file_search_button.grid(column=1, row=1)

    return file_select_frame, image_label, image


def init_output_pane(window):
    """Creates the output image pane."""
    output_frame = Frame(window)
    output_frame.grid(column=2, row=0)
    output_frame.rowconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=0)

    image_label, image = init_displayed_image(output_frame, filepath="imagefiles/EXAMPLE.png", columnspan=2)

    output_button = Button(output_frame, text="Generate", command=generate_output)
    output_button.grid(column=0, row=1)

    save_button = Button(output_frame, text="Save", command=save_output)
    save_button.grid(column=1, row=1)

    return output_frame, image_label, image


def init_parent_frame(window):
    """Creates an empty parent frame for the other content frames to occupy."""
    content_frame = Frame(window, padding=20)
    content_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)
    content_frame.columnconfigure(2, weight=2)

    return content_frame


def init_text_widget(parent, font, **kwargs):
    """Creates the flavor text input widget"""
    text_widget = Text(parent, width=40, height=6, wrap="word", font=font)
    text_widget.grid(**kwargs)

    return text_widget


def save_output():
    """Saves the output image to a file."""
    generate_output()

    output_filepath = filedialog.asksaveasfilename(defaultextension=".png")
    output_image = ImageTk.getimage(TKWINDOW.output_image)

    output_image.save(output_filepath)


def select_new_filepath():
    """Selects a new filepath for the vox portrait."""
    new_filepath = filedialog.askopenfilename(parent=TKWINDOW.window, title="Select Vox portrait...", initialdir="imagefiles")
    FILEPATH.set(new_filepath)
    TKWINDOW.portrait_image_label, TKWINDOW.portrait_image = init_displayed_image(TKWINDOW.left_frame, filepath=new_filepath)


class TkWindow:
    def __init__(self):
        self.window = ROOT
        self.parent_frame = init_parent_frame(self.window)

        self.left_frame, self.portrait_image_label, self.portrait_image = init_file_select_pane(self.parent_frame)

        self.vox_name_variable = StringVar()
        self.vox_attribute_variable = StringVar()
        self.middle_frame, self.vox_goal, self.action_1, self.action_2, self.action_3 = \
            init_entry_pane(self.parent_frame, self.vox_name_variable, self.vox_attribute_variable)

        self.right_frame, self.output_image_label, self.output_image = init_output_pane(self.parent_frame)


TKWINDOW = TkWindow()


if __name__ == "__main__":
    TKWINDOW.window.mainloop()
