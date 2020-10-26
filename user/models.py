from django.db import models

class User(models.Model): 
    email           = models.EmailField()
    name            = models.CharField(max_length=200)
    password        = models.CharField(max_length=500)
    terms_service   = models.BooleanField(default=False)
    terms_privacy   = models.BooleanField(default=False)
    terms_marketing = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'