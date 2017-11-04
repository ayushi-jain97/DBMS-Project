from django.db import models

class Merchandise(models.Model):
    itemid = models.AutoField(primary_key=True)
    image = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    price = models.IntegerField()
    text = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'merchandise'

    def __unicode__(self):
        return str(self.itemid)
