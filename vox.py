from PIL import Image
import visualizer

# Vox Attributes
ATTR = {"Intellect": ("Intellect", (60, 70, 100)),
        "Psyche": ("Psyche", (100, 95, 128)),
        "Physick": ("Physick", (130, 40, 50)),
        "Skill": ("Skill", (210, 175, 75)),
        "Animus": ("Animus", (140, 215, 150)),
        "Endopulse": ("Endopulse", (220, 80, 175))}

class Vox:
    """Gets a vox object from a set of variables."""
    def __init__(self, vox_name, vox_attribute, vox_goal, *actions, vox_filepath=None):
        self.name = vox_name
        self.attribute = vox_attribute
        self.goal = vox_goal
        self.actions = actions

        self.image_filepath = vox_filepath


    def get_card_image(self):
        """Builds and returns the image of the card."""
        card_image = visualizer.load_bg()

        if self.image_filepath is not None:
            card_image.paste(Image.open(self.image_filepath))

        y_offset = 0  # The amount to offset each new element downward to avoid overlaps

        next_element = visualizer.get_title_field_image(self.name, self.attribute[0], self.attribute[1])
        card_image.alpha_composite(next_element, (512, 0))
        y_offset += next_element.height

        next_element = visualizer.get_goal_field_image(self.goal)
        card_image.alpha_composite(next_element, (512, y_offset))
        y_offset += next_element.height

        for each_action in self.actions:
            next_element = visualizer.get_action_field_image(each_action)
            card_image.alpha_composite(next_element, (512, y_offset))
            y_offset += next_element.height

        return card_image


if __name__ == "__main__":
    new_vox = Vox("Simpatico", ATTR["Animus"], "To act as an example.",
                  "Reach into other's minds, take things out.",
                  "Find comfort in shared ideas.",
                  vox_filepath="imagefiles/examplevox.png")
    new_image = new_vox.get_card_image()

    new_image.save("imagefiles/EXAMPLE.png", "PNG")
