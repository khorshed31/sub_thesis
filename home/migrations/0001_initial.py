# Generated by Django 4.2.3 on 2023-08-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('courseCode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=100)),
                ('courseTeacher', models.CharField(max_length=50)),
                ('courseSeason', models.CharField(max_length=10)),
                ('courseKey', models.CharField(max_length=10)),
            ],
        ),
    ]
