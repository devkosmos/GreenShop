from tortoise import fields
from tortoise.models import Model

class Users(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=18)
    balance = fields.IntField()
