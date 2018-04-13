# Generated by Django 2.0.4 on 2018-04-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_type', models.CharField(max_length=30)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('days', models.CharField(max_length=7)),
            ],
            options={
                'ordering': ('start_time',),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('_id', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('crn', models.IntegerField()),
                ('section', models.CharField(max_length=4)),
                ('honors', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=60)),
                ('meetings', models.ManyToManyField(to='sections.Meeting')),
            ],
            options={
                'ordering': ('honors', 'section'),
            },
        ),
    ]
