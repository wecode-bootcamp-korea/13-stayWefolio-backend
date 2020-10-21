from django.db import models


class User(models.Model):
    email=models.EmailField()
    name=models.CharField(max_length=200)
    password=models.CharField(max_length=500)

    class Meta:
        db_table='users'