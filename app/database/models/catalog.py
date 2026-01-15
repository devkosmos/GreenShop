from tortoise import fields
from tortoise.models import Model

class Category(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField()
    

class Products(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField()
    description = fields.TextField()
    price = fields.IntField()
    category_id = fields.ForeignKeyField("model.Category")