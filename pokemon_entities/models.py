from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True)


    def __str__(self):
        if self.title:
            return self.title
        return f'{self.title}'


class PokemonEntity(models.Model):
    lat = models.FloatField(max_length=200)
    lon = models.FloatField(max_length=200)
