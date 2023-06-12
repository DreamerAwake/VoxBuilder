from math import floor
from tkinter import Label as tkLabel
from tkinter import Text
from tkinter.ttk import Entry
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


def init_tk_window(min_size=(1521, 852)):
    """Initializes a tkinter Tk, returns it."""
    window_frame = ThemedTk(theme='yaru')
    window_frame.title("Legend of the Lamplighters: Character Builder")
    window_frame.iconbitmap("imagefiles/LotL.ico")

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=1)

    window_frame.minsize(*min_size)

    return window_frame


ROOT = init_tk_window()
INPUT_FONT = ("Arial", 10)
INPUT_FONT_EXPANDED = ("Arial", 18, "bold")


def init_displayed_image(parent, image=None, filepath=None, image_scale=0.5, column=0, row=0, **kwargs):
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

    image_label.grid(column=column, row=row, **kwargs)

    return image_label, image


def init_entry_widget(parent, variable, font, **kwargs):
    """Create an entry widget."""
    title_entry = Entry(parent, width=40, textvariable=variable, font=font)
    title_entry.grid(**kwargs)


def init_text_widget(parent, font, width, height, **kwargs):
    """Creates the flavor text input widget"""
    text_widget = Text(parent, width=width, height=height, wrap="word", font=font)
    text_widget.grid(**kwargs)

    return text_widget


def intvar_plus_1(variable):
    """Adds 1 to the given intvar."""
    variable.set(variable.get() + 1)


def intvar_minus_1(variable):
    """Subtracts 1 from the given intvar. Minimum result of 0."""
    current_value = variable.get()
    if current_value > 0:
        variable.set(current_value - 1)

