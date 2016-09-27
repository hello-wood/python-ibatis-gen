class FieldInfo:
    field_name = None
    field_type = None
    comment = None
    is_pri_key = False

    def __init__(self, field_name, field_type, comment=None, is_pri_key=False):
        self.field_name = field_name
        self.field_type = field_type
        self.comment = comment
        self.is_pri_key = is_pri_key
