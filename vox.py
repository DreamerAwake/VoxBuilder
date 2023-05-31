import json
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
    def __init__(self, vox_name, vox_attribute, vox_goal, vox_ranks, is_signature, *actions, vox_filepath=None):
        self.name = vox_name
        self.attribute = vox_attribute
        self.goal = vox_goal
        self.ranks = vox_ranks
        self.is_signature = is_signature
        self.actions = actions

        self.image_filepath = vox_filepath


    def get_card_image(self, attribute_value):
        """Builds and returns the image of the card."""
        card_image = visualizer.load_bg()

        if self.image_filepath is not None:
            card_image.paste(Image.open(self.image_filepath))

        y_offset = 0  # The amount to offset each new element downward to avoid overlaps

        # Place the vox title bar
        next_element = visualizer.get_title_field_image(self.name, self.attribute[0], self.attribute[1], attribute_value, self.is_signature)
        card_image.alpha_composite(next_element, (512, 0))
        y_offset += next_element.height

        # Place the goal text
        next_element = visualizer.get_goal_field_image(self.goal)
        card_image.alpha_composite(next_element, (512, y_offset))
        y_offset += next_element.height

        # Place each action
        for each_action in self.actions:
            next_element = visualizer.get_action_field_image(each_action)
            card_image.alpha_composite(next_element, (512, y_offset))
            y_offset += next_element.height

        # Calculate non-attribute or rank based bonuses (Just the +1 signature bonus for now)
        if self.is_signature:
            other_bonuses = 1
        else:
            other_bonuses = 0

        # Place the skill total bar
        next_element = visualizer.get_skill_pip_image(attribute_value, self.ranks, other_bonuses)
        card_image.alpha_composite(next_element, (512, 668))

        return card_image


    def save_json(self, filepath):
        save_dict = {"name": self.name,
                     "attribute": self.attribute[0],
                     "goal": self.goal,
                     "ranks": self.ranks,
                     "signature": self.is_signature,
                     "actions": self.actions,
                     "filepath": self.image_filepath}

        with open(filepath, 'w', encoding='utf-8') as fileobject:
            json.dump(save_dict, fileobject)


def load_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as fileobject:
        load_dict = json.load(fileobject)

    loaded_vox = Vox(load_dict["name"],
                     ATTR[load_dict["attribute"]],
                     load_dict["goal"],
                     load_dict["ranks"],
                     load_dict["signature"],
                     *load_dict["actions"],
                     vox_filepath=load_dict["filepath"])

    return loaded_vox

if __name__ == "__main__":
    new_vox = Vox("Simpatico", ATTR["Animus"], "To act as an example.", 5, True,
                  "Reach into other's minds, take things out.",
                  "Find comfort in shared ideas.",
                  vox_filepath="imagefiles/examplevox.png")

    new_image = new_vox.get_card_image(1)

    new_image.save("imagefiles/EXAMPLE.png", "PNG")
