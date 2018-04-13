from django.db import models

class Meeting(models.Model):
    meeting_type = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=7)
    class Meta:
        ordering = ('start_time',)

class Section(models.Model):
    _id = models.CharField(primary_key=True, max_length=13)
    crn = models.IntegerField()
    section = models.CharField(max_length=4)
    honors = models.BooleanField(default=False)
    name = models.CharField(max_length=60)
    meetings = models.ManyToManyField(Meeting)
    # TODO: Figure out how to reference courses
    # TODO: Figure out how to reference instructors
    class Meta:
        ordering = ('honors', 'section',)
