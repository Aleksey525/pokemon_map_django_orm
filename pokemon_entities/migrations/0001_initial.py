# Generated by Django 3.1.14 on 2024-02-14 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(max_length=200)),
                ('lon', models.FloatField(max_length=200)),
                ('appeared_at', models.DateTimeField()),
                ('disappeared_at', models.DateTimeField()),
                ('level', models.IntegerField(blank=True, null=True)),
                ('health', models.IntegerField(blank=True, null=True)),
                ('strenght', models.IntegerField(blank=True, null=True)),
                ('defence', models.IntegerField(blank=True, null=True)),
                ('stamina', models.IntegerField(blank=True, null=True)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
    ]
