import folium
from django.shortcuts import render,get_object_or_404
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
        entity_photo = request.build_absolute_uri(entity.pokemon.photo.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_photo = request.build_absolute_uri(pokemon.photo.url)
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
    get_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    entities = PokemonEntity.objects.filter(pokemon__title=get_pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in entities:
        entity_photo = request.build_absolute_uri(get_pokemon.photo.url)
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            entity_photo
        )

    pokemon = {
        'pokemon_id': get_pokemon.id,
        'img_url': request.build_absolute_uri(get_pokemon.photo.url),
        'title_ru': get_pokemon.title,
        'title_en': get_pokemon.title_en,
        'title_jp': get_pokemon.title_jp,
        'description': get_pokemon.description,
    }

    previous_evolution = {}
    if get_pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": get_pokemon.previous_evolution.title,
            "pokemon_id": get_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(get_pokemon.previous_evolution.photo.url),
            "previous_evolution": get_pokemon.previous_evolution
        }

    child = get_pokemon.next_evolution.first()

    next_evolution = {}
    if child:
        next_evolution = {
            'title_ru': child.title,
            "pokemon_id": child.id,
            "img_url": request.build_absolute_uri(child.photo.url),
            "next_evolution": child
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon, 'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    })