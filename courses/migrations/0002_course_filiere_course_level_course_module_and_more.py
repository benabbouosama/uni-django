# Generated by Django 4.2.3 on 2023-08-21 19:29

import courses.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="filiere",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.filiere",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="course",
            name="level",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.level",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="course",
            name="module",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="courses.module",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="course",
            name="pdf_file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=courses.models.Course.pdf_file_upload_path,
            ),
        ),
    ]
