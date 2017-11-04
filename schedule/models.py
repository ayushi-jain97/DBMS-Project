from django.db import models


class Member(models.Model):
    rollnumber = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    emailID = models.CharField(db_column='emailID', max_length=50) 

    class Meta:
        managed = False
        db_table = 'members'
    def __unicode__(self):
        return str(self.rollnumber)

class Memberphone(models.Model):
    rollnumber = models.ForeignKey('Member', db_column='rollnumber', blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'memberPhone'
    def __unicode__(self):
        return self.rollnumber


class Postdesc(models.Model):
    rollnumber = models.ForeignKey(Member, db_column='rollnumber', blank=True, null=True)
    designation = models.CharField(max_length=20, blank=True, null=True)
    serviceYear = models.IntegerField(db_column='serviceYear', blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postDesc'
        unique_together = (('rollnumber', 'designation', 'serviceYear', 'category'),)


class Workshop(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=10, blank=True, null=True)
    venue = models.CharField(max_length=20, blank=True, null=True)
    topic = models.CharField(max_length=40, blank=True, null=True)
    level = models.CharField(max_length=40, blank=True, null=True)
    targetaudience = models.CharField(db_column='targetAudience', max_length=40, blank=True, null=True)  # Field name made lowercase.
    inchargeid = models.ForeignKey(Member, db_column='inchargeID', blank=True, null=True)  # Field name made lowercase.
    text = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'workshops'
        unique_together = (('date', 'time', 'venue'),)
    def __unicode__(self):
        return str(self.date)+','+self.time+','+self.venue;






