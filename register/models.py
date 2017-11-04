from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'participants'


