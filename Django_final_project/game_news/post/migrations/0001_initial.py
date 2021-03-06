# Generated by Django 4.0.3 on 2022-04-02 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type_post', models.CharField(choices=[('t', 'Tanks'), ('h', 'Hils'), ('d', 'DD'), ('t', 'Traders'), ('g', 'Guildmasters'), ('q', 'Questgivers'), ('b', 'Blacksmiths'), ('l', 'Leatherworkers'), ('p', 'Potions'), ('s', 'Spell masters')], max_length=1)),
                ('text', models.TextField()),
                ('data', models.DateField(auto_now_add=True)),
                ('upload', models.FileField(upload_to='upload/')),
                ('authort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cooment', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
