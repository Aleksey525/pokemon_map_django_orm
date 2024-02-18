import folium
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
        entity_photo = request.build_absolute_uri(f'/media/{entity.pokemon.photo}')
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_photo = request.build_absolute_uri(f'/media/{pokemon.photo}')
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_photo,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_name = Pokemon.objects.get(id=int(pokemon_id))
    entities = PokemonEntity.objects.filter(pokemon__title=pokemon_name)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in entities:
        entity_photo = request.build_absolute_uri(f'/media/{pokemon_name.photo}')
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemon = {
        'pokemon_id': pokemon_name.id,
        'img_url': request.build_absolute_uri(f'/media/{pokemon_name.photo}'),
        'title_ru': pokemon_name.title,
        'title_en': pokemon_name.title_en,
        'title_jp': pokemon_name.title_jp,
        'description': pokemon_name.description,
    }

    if pokemon_name.previous_evolution:
        previous_evolution = {
            "title_ru": pokemon_name.previous_evolution.title,
            "pokemon_id": pokemon_name.previous_evolution.id,
            "img_url": request.build_absolute_uri(f'/media/{pokemon_name.previous_evolution.photo}'),
            "previous_evolution": pokemon_name.previous_evolution
        }

    else:
        previous_evolution = {}

    pokemon_get = Pokemon.objects.get(id=pokemon_id)
    child = pokemon_get.evolution.all().first()

    if child:
        next_evolution = {
            'title_ru': child.title,
            "pokemon_id": child.id,
            "img_url": request.build_absolute_uri(f'/media/{child.photo}'),
            "next_evolution": child
        }
    else:
        next_evolution = {}

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon, 'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    })