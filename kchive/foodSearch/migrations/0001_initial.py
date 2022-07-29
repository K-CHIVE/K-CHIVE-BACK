# Generated by Django 3.2 on 2022-07-29 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='그룹이름')),
                ('tag1', models.CharField(blank=True, max_length=100, verbose_name='그룹태그1')),
                ('tag2', models.CharField(blank=True, max_length=100, verbose_name='그룹태그2')),
                ('tag3', models.CharField(blank=True, max_length=100, verbose_name='그룹태그3')),
                ('tag4', models.CharField(blank=True, max_length=100, verbose_name='그룹태그4')),
                ('tag5', models.CharField(blank=True, max_length=100, verbose_name='그룹태그5')),
            ],
            options={
                'verbose_name': '그룹',
                'verbose_name_plural': '그룹',
                'db_table': 'Group_table',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='멤버이름')),
                ('tag1', models.CharField(blank=True, max_length=100, verbose_name='멤버태그1')),
                ('tag2', models.CharField(blank=True, max_length=100, verbose_name='멤버태그2')),
                ('tag3', models.CharField(blank=True, max_length=100, verbose_name='멤버태그3')),
                ('tag4', models.CharField(blank=True, max_length=100, verbose_name='멤버태그4')),
                ('tag5', models.CharField(blank=True, max_length=100, verbose_name='멤버태그5')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodSearch.group')),
            ],
            options={
                'verbose_name': '멤버',
                'verbose_name_plural': '멤버',
                'db_table': 'Member_table',
            },
        ),
    ]
