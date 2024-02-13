import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    time_now = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    entities = PokemonEntity.objects.filter(disappeared_at__gt=time_now, appeared_at__lt=time_now)

    for entity in entities:
        entity_photo = request.build_absolute_uri(f'/media/{entity.Pokemon.photo}')
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pok in pokemons:
        photo_pok = request.build_absolute_uri(f'/media/{pok.photo}')
        pokemons_on_page.append({
            'pokemon_id': pok.id,
            'img_url': photo_pok,
            'title_ru': pok.title,
        })


    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=int(pokemon_id))
    entities = PokemonEntity.objects.filter(Pokemon__title=pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in entities:
        entity_photo = request.build_absolute_uri(f'/media/{pokemon.photo}')
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': entity_photo,
        'title_ru': pokemon.title,
    }



    # else:
    #     return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
