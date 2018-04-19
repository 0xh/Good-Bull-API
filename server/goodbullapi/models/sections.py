from django.db import models

class Meeting(models.Model):
    meeting_type = models.CharField(max_length=30)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days = models.CharField(max_length=7, null=True)
    # TODO: relate to buildings
    class Meta:
        ordering = ('start_time',)


class Section(models.Model):
    _id = models.CharField(primary_key=True, max_length=13)
    term_code = models.IntegerField()
    crn = models.IntegerField()
    dept = models.CharField(max_length=5)
    course_num = models.CharField(max_length=5)
    section_num = models.CharField(max_length=4)
    honors = models.BooleanField(default=False)
    section_name = models.CharField(max_length=60)
    meetings = models.ManyToManyField(Meeting)
    credits = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    course = models.ForeignKey('Course', related_name='sections', on_delete=models.CASCADE)
    #instructor = models.ForeignKey('instructors.Instructor', on_delete=models.CASCADE)

    class Meta:
        ordering = ('honors', 'section_num',)
