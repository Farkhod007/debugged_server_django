from .base.time_fields_base import TimeFieldsBase 
from .base.category_tag_base import CategoryTagBase 

class Tag(CategoryTagBase, TimeFieldsBase):
    class Meta:
        db_table = "tags"