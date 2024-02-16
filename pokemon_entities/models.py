from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    title_en = models.CharField(verbose_name='Название на английском', max_length=200)
    title_jp = models.CharField(verbose_name='Название на японском', max_length=200)
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    previous_evolution = models.ForeignKey('Pokemon', verbose_name='Предок', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        if self.title:
            return self.title
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='Широта', max_length=200)
    lon = models.FloatField(verbose_name='Долгота',max_length=200)
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strenght = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)
