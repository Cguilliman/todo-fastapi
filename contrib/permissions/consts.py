from typing import *
from enum import Enum, IntEnum


class EnumLabelBuildingException(Exception):
    pass


class _EnumLabel(object):

    def __call__(self, name: str, values: Tuple):
        label_map = {}
        enumerate_fields = {}

        for item in values:
            if len(item) != 3:
                raise EnumLabelBuildingException("Invalid enum initialization data.")
            value, field_name, label = item
            enumerate_fields[field_name] = value
            label_map[value] = label

        @classmethod
        def get_label(cls, value_obj: Enum):
            # `._value_` - will return instance type result
            return label_map.get(value_obj._value_)

        _enum_class = Enum(name, enumerate_fields)
        _enum_class.get_label = get_label
        return _enum_class


EnumLabel = _EnumLabel()


MemberPermissions = EnumLabel("_MemberPermissions", (
    (3, "owner", "Owner"),
    (2, "member", "Member"),
    (1, "guest", "Guest"),
))


# Permissions
READ = 'R'
WRITE = 'W'
SUPER_WRITE = 'SW'
EDIT = 'E'
# Permissions groups
PERMISSIONS = {
    1: (READ, ),
    2: (READ, WRITE),
    3: (READ, SUPER_WRITE, EDIT),
}
