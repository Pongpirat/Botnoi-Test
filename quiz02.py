import requests
import json

def get_pokemon_data():
    pokemon_stat = f'https://pokeapi.co/api/v2/pokemon/1/'
    pokemon_name_prites = f'https://pokeapi.co/api/v2/pokemon-form/1/'

    pokemon_response = requests.get(pokemon_stat)
    pokemon_form_response = requests.get(pokemon_name_prites)

    pokemon_data = pokemon_response.json()
    pokemon_form_data = pokemon_form_response.json()

    result = {
        'stats': pokemon_data.get('stats')[:2],
        'name': pokemon_form_data.get('name'),
        'sprites': pokemon_form_data.get('sprites')
    }

    return result

def save_to_json(data, filename):
    with open(filename, 'w+') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    pokemon_data = get_pokemon_data()
    save_to_json(pokemon_data, 'pokemon_data.json')