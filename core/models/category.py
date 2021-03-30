from .base.time_fields_base import TimeFieldsBase 
from .base.category_tag_base import CategoryTagBase 

class Category(CategoryTagBase, TimeFieldsBase):
    class Meta:
        db_table = "categories"