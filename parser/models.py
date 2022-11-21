from django.db import models

# Create your models here.
from django.db import models
import uuid


class Type(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    description = models.CharField(max_length=128)
    nature = models.CharField(max_length=128)


class Transaction(models.Model):
    type = models.ForeignKey(
        "parser.Type", on_delete=models.DO_NOTHING, related_name="transactions"
    )
    date = models.DateField()
    value = models.FloatField()
    cpf = models.CharField(max_length=128)
    cardNum = models.CharField(max_length=128)
    hour = models.TimeField()
    owner = models.CharField(max_length=128)
    store = models.CharField(max_length=128)
