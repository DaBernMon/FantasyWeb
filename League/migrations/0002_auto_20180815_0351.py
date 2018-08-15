# Generated by Django 2.1 on 2018-08-15 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('team', models.CharField(max_length=3)),
                ('number', models.CharField(max_length=3)),
                ('position', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=5)),
                ('height', models.CharField(max_length=5)),
                ('weight', models.CharField(max_length=5)),
                ('dob', models.CharField(max_length=10)),
                ('experience', models.CharField(max_length=3)),
                ('college', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('name', 'dob', 'college')},
        ),
    ]
