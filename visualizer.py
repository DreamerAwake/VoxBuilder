from math import floor, ceil
from PIL import Image, ImageDraw, ImageFont

# Fonts
TEXT_COLOR_DARK = (10, 10, 10, 255)
TEXT_COLOR_LIGHT = (245, 245, 245, 255)
UNDERTEXT_COLOR = (64, 64, 64, 180)
TITLE_FONT = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 60)
TITLE_FONT_REDUCED = ImageFont.truetype("C:/Windows/Fonts/times.ttf", 40)
ATTRIBUTE_FONT = ImageFont.truetype("C:/Windows/Fonts/timesi.ttf", 40)
GOAL_FONT = ImageFont.truetype("C:/Windows/Fonts/timesi.ttf", 36)
ACTION_FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 30)


def chop_into_halves(text):
    """Takes a string and breaks it into two lines at roughly the midpoint, preferring to be top-heavy.
    Returns a tuple of two strings."""
    wordlist = text.split()

    slicepoint = ceil(len(wordlist) / 2)

    line_1 = " ".join(wordlist[:slicepoint])
    line_2 = " ".join(wordlist[slicepoint:])

    return line_1, line_2


def break_into_lines(image_editor, text_sample, max_length):
    """Takes a string and breaks it into several lines of text based on length so that it can be easily rendered.
    Also requires a PIL ImageDraw object with its font settings initialized to the font to be checked."""
    # Split the text
    wordlist = text_sample.split()

    single_line = []
    final_lines = []

    # Build each line word by word
    for each_word in wordlist:

        # Respond to newline characters
        if each_word == "/n":
            final_lines.append(" ".join(single_line))
            single_line.clear()

        # If the line is short enough, add the next word
        elif image_editor.textlength(" ".join(single_line) + " " + each_word) < max_length:
            single_line.append(each_word)

        # If you have reached the end of a line, add to the final line, and go to the next line
        else:
            final_lines.append(" ".join(single_line))
            single_line.clear()
            single_line.append(each_word)

    final_lines.append(" ".join(single_line))

    return final_lines


def get_title_field_image(vox_title, vox_attribute_label, vox_color, vox_attribute_bonus, is_signature):
    """Creates the Title field image for later compositing."""
    title_field_image = Image.new("RGBA", (768, 100), (*vox_color, 180))
    label_editor = ImageDraw.Draw(title_field_image)

    # Draw the vox attribute
    label_editor.font = ATTRIBUTE_FONT
    attribute_label_string = vox_attribute_label + " • " + str(vox_attribute_bonus)
    label_editor.text((748, 70), attribute_label_string, fill=TEXT_COLOR_DARK, anchor="rs")

    # If it is a signature vox, add the icon
    if is_signature:
        icon_image = Image.open("imagefiles/signature.png")
        title_field_image.alpha_composite(icon_image, (20, 35))

    # Draw the vox title
    attribute_text_length = label_editor.textlength(attribute_label_string)
    label_editor.font = TITLE_FONT
    vox_title_length = label_editor.textlength(vox_title.upper())
    x_offset = 384 - attribute_text_length
    if is_signature:
        x_offset += 80

    if attribute_text_length + vox_title_length + 80 < 728:
        label_editor.text((x_offset, 70), vox_title.upper(), fill=TEXT_COLOR_DARK, anchor="ms")
    else:
        vox_goal_lines = chop_into_halves(vox_title)
        label_editor.font = TITLE_FONT_REDUCED
        label_editor.text((x_offset, 20), vox_goal_lines[0], fill=TEXT_COLOR_DARK, anchor="mt")
        label_editor.text((x_offset, 60), vox_goal_lines[1], fill=TEXT_COLOR_DARK, anchor="mt")

    return title_field_image


def get_goal_field_image(vox_goal):
    goal_field_image = Image.new("RGBA", (768, 72), UNDERTEXT_COLOR)
    label_editor = ImageDraw.Draw(goal_field_image)
    label_editor.font = GOAL_FONT

    vox_goal_lines = break_into_lines(label_editor, vox_goal, 728)

    # Extend field to fit lines
    if len(vox_goal_lines) > 1:
        goal_field_image = Image.new("RGBA", (768, 36 + 36 * len(vox_goal_lines)), UNDERTEXT_COLOR)
        label_editor = ImageDraw.Draw(goal_field_image)
        label_editor.font = GOAL_FONT

    for each_line_index in range(0, len(vox_goal_lines)):
        label_editor.text((384, 36 + (36 * each_line_index)),
                          vox_goal_lines[each_line_index],
                          fill=TEXT_COLOR_LIGHT, anchor="mm")

    return goal_field_image


def get_action_field_image(vox_action):
    action_field_image = Image.new("RGBA", (768, 60), UNDERTEXT_COLOR)
    label_editor = ImageDraw.Draw(action_field_image)
    label_editor.font = ACTION_FONT

    vox_action_lines = break_into_lines(label_editor, vox_action, 648)

    # Extend field to fit lines
    if len(vox_action_lines) > 1:
        action_field_image = Image.new("RGBA", (768, 30 + 30 * len(vox_action_lines)), UNDERTEXT_COLOR)
        label_editor = ImageDraw.Draw(action_field_image)
        label_editor.font = ACTION_FONT

    for each_line_index in range(0, len(vox_action_lines)):
        label_editor.text((80, 30 + (30 * each_line_index)),
                          vox_action_lines[each_line_index],
                          fill=TEXT_COLOR_LIGHT, anchor="lm")

    label_editor.rectangle(((35, floor(0.5 * action_field_image.height) - 5),
                           (45, floor(0.5 * action_field_image.height) + 5)),
                           (200, 200, 200, 255))

    return action_field_image


def get_skill_pip_image(attribute_bonus, skill_ranks, other_bonuses):
    skill_pip_image = Image.new("RGBA", (768, 100), (0, 0, 0, 0))

    skill_pip_image.paste(Image.open("imagefiles/totalbox.png"), (690, 0))

    # Prepare to place the skill rank pips
    pip_image = Image.open("imagefiles/pip.png")
    pip_line_length = (45 * skill_ranks) - 15  # Assumes 30 pix wide pips and a 15 pix gap between each
    place_at_x = floor((690 - pip_line_length) / 2)

    for iteration in range(0, skill_ranks):
        skill_pip_image.alpha_composite(pip_image, (place_at_x, 40))
        place_at_x += 45

    skill_total = attribute_bonus + skill_ranks + other_bonuses
    label_editor = ImageDraw.Draw(skill_pip_image)
    label_editor.font = TITLE_FONT
    label_editor.text((729, 80), str(skill_total), fill=TEXT_COLOR_LIGHT, anchor="ms")

    return skill_pip_image


def load_bg():
    bg_sprite = Image.open("imagefiles/bg.png").resize((1280, 768))
    bg = Image.new("RGBA", bg_sprite.size, (0, 0, 0, 0))
    bg.paste(bg_sprite)

    return bg
