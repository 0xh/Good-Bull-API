from django.db import models


class Meeting(models.Model):
    meeting_type = models.CharField(max_length=30)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days = models.CharField(max_length=7, null=True)

    def __repr__(self):
        return str(
            (self.meeting_type,
             self.start_time,
             self.end_time,
             self.days))

    def __str__(self):
        return str(
            (self.meeting_type,
             self.start_time,
             self.end_time,
             self.days))

    class Meta:
        ordering = ('start_time',)


class Section(models.Model):
    _id = models.CharField(primary_key=True, max_length=13)
    crn = models.IntegerField()
    section_num = models.CharField(max_length=4)
    honors = models.BooleanField(default=False)
    section_name = models.CharField(max_length=60)
    meetings = models.ManyToManyField(Meeting)
    credits = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    # TODO: Figure out how to reference courses
    # TODO: Figure out how to reference instructors

    class Meta:
        ordering = ('honors', 'section_num',)
