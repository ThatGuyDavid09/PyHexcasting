import re


class DropKeep:
    def __init__(self, value):
        match = re.fullmatch(r"^dk_[dk]+$", value)
        if match is None:
            raise ValueError(f"{value} is not valid drop_keep syntax")
        self.value = value

    def get_drop_order(self):
        drop_keep = self.value.replace("dk_", "")
        drop_keep = [True if i == "d" else False for i in drop_keep]
        return drop_keep

    def __str__(self):
        return f"DropKeep {self.value}"
