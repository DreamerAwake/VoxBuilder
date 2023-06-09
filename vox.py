import json
from PIL import Image
import visualizer

# Vox Attributes
ATTR = {"Benedictum": ("Benedictum", (110, 90, 140)),
        "Cerebra": ("Cerebra", (80, 100, 192)),
        "Endopulse": ("Endopulse", (220, 80, 175)),
        "Myomesmer": ("Myomesmer", (200, 60, 40)),
        "Psychoanima": ("Psychoanima", (210, 190, 75)),
        "Visiospatia": ("Visiospatia", (140, 230, 150)),
        }


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

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

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

        # Place the skill total bar
        next_element = visualizer.get_skill_pip_image(attribute_value, self.ranks, self.get_other_bonuses())
        card_image.alpha_composite(next_element, (512, 668))

        return card_image

    def get_mini_popout_image(self, attribute_value):
        popout_image = Image.new("RGBA", (512, 768), (0, 0, 0, 0))
        popout_image.paste(Image.open(self.image_filepath))

        # Draw the skill pips
        popout_image.alpha_composite(visualizer.get_mini_title_pips_image(self.ranks), (0, 0))

        # Draw the title plaque
        popout_image.alpha_composite(visualizer.get_mini_title_field_image(self, attribute_value), (0, 668))

        return popout_image

    def get_other_bonuses(self):
        """Calculate non-attribute or rank based bonuses (Just the +1 signature bonus for now)"""
        other_bonuses = 0

        if self.is_signature:
            other_bonuses += 1

        return other_bonuses

    def is_attr(self, attribute_name):
        return attribute_name == self.attribute[0]

    def save_dict(self):
        """Returns a json compatible dict for saving."""
        save_dict = {"name": self.name,
                     "attribute": self.attribute[0],
                     "goal": self.goal,
                     "ranks": self.ranks,
                     "signature": self.is_signature,
                     "actions": self.actions,
                     "filepath": self.image_filepath}

        return save_dict

    def save_json(self, filepath):

        save_dict = self.save_dict()

        with open(filepath, 'w', encoding='utf-8') as fileobject:
            json.dump(save_dict, fileobject)


def load_from_dict(load_dict):
    loaded_vox = Vox(load_dict["name"],
                     ATTR[load_dict["attribute"]],
                     load_dict["goal"],
                     load_dict["ranks"],
                     load_dict["signature"],
                     *load_dict["actions"],
                     vox_filepath=load_dict["filepath"])

    return loaded_vox


def load_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as fileobject:
        load_dict = json.load(fileobject)

    loaded_vox = load_from_dict(load_dict)

    return loaded_vox


if __name__ == "__main__":
    new_vox = Vox("Simpatico", ATTR["Visiospatia"], "To act as an example.", 5, True,
                  "Reach into other's minds, take things out.",
                  "Find comfort in shared ideas.",
                  vox_filepath="imagefiles/defaultvox.png")

    new_image = new_vox.get_card_image(1)
    new_image.save("imagefiles/EXAMPLE.png", "PNG")

    new_image = new_vox.get_mini_popout_image(1)
    new_image.save("dev/EXAMPLEpopout.png", "PNG")
