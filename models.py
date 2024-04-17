from tortoise import models, fields


class Car(models.Model):
    model = fields.CharField(max_length=50)
    year = fields.IntField(pk=True)
    color = fields.CharField(max_length=50)

    def __str__(self):
        return self.model


class Person(models.Model):
    name = fields.CharField(max_length=50)
    age = fields.IntField(pk=True)
    gender = fields.CharField(max_length=50)
    image = fields.CharField(max_length=50)

    def __str__(self):
        return self.name

