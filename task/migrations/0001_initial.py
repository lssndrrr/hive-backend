# Generated by Django 5.2 on 2025-05-02 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('due_date', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
