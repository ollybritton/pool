# Generated by Django 4.1.4 on 2024-01-21 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("elo", "0002_frame_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="frame",
            name="breaking_player",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="frames_broken",
                to="elo.player",
            ),
            preserve_default=False,
        ),
    ]