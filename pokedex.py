"""
Author: Uri Jared Gopar Morales
Date: 29/06/2024
Description: This script will be used to get information from the Pokedex API and save it to an HTML file.
"""
from flask import Flask, request, render_template_string
import requests
import webbrowser
import threading
import os

app = Flask(__name__)

OUTPUT_DIR = 'outputs'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    return render_template_string(open('pokedex.html').read())

def get_ability_effects(ability_url):
    response = requests.get(ability_url)
    ability_data = response.json()
    effect_entries = ability_data['effect_entries']
    effect = next(entry['effect'] for entry in effect_entries if entry['language']['name'] == 'en')
    return effect

def get_evolution(evolution_url):
    response = requests.get(evolution_url)
    evolution_data = response.json()
    chain = evolution_data['chain']
    evolutions = []
    if chain:
        chain = chain['evolves_to'][0] if chain['evolves_to'] else None
    while chain:
        evolutions.append(chain['species']['name'])
        chain = chain['evolves_to'][0] if chain['evolves_to'] else None
    return evolutions

def get_type_info(type_url):
    response = requests.get(type_url)
    type_data = response.json()
    double_damage_from = [damage['name'] for damage in type_data['damage_relations']['double_damage_from']]
    double_damage_to = [damage['name'] for damage in type_data['damage_relations']['double_damage_to']]
    return double_damage_from, double_damage_to

def get_pokemon_data(pokemon_url):
    response = requests.get(pokemon_url)
    pokemon_data = response.json()
    pokemon_name = pokemon_data['name'].capitalize()
    pokemon_abilities = [{'name': ability['ability']['name'], 'effect': get_ability_effects(ability['ability']['url'])} for ability in pokemon_data['abilities']]

    hp = pokemon_data['stats'][0]['base_stat']
    attack = pokemon_data['stats'][1]['base_stat']
    defense = pokemon_data['stats'][2]['base_stat']
    base_experience = pokemon_data['base_experience']
    image_url = pokemon_data['sprites']['front_default']

    species_url = pokemon_data['species']['url']
    species_response = requests.get(species_url)
    species_data = species_response.json()
    evolution_chain= species_data['evolution_chain']['url']
    evolutions = get_evolution(evolution_chain)

    types = [t['type']['name'] for t in pokemon_data['types']]
    type_urls = [t['type']['url'] for t in pokemon_data['types']]
    double_damage_from, double_damage_to = [], []
    for type_url in type_urls:
        dd_from, dd_to = get_type_info(type_url)
        double_damage_from.extend(dd_from)
        double_damage_to.extend(dd_to)

    return {
        'pokemon_name': pokemon_name,
        'image_url': image_url,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'base_experience': base_experience,
        'pokemon_abilities': pokemon_abilities,
        'evolutions': evolutions,
        'types': types,
        'double_damage_from': list(set(double_damage_from)),
        'double_damage_to': list(set(double_damage_to))
    }

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    choice = request.form.get('choice')
    url_map = {
        "1": "https://pokeapi.co/api/v2/pokemon/pichu",
        "2": "https://pokeapi.co/api/v2/pokemon/charmander",
        "3": "https://pokeapi.co/api/v2/pokemon/squirtle",
        "4": "https://pokeapi.co/api/v2/pokemon/bulbasaur"
    }
    pokemon_url = url_map.get(choice)
    if not pokemon_url:
        return "Invalid choice"

    pokemon_data = get_pokemon_data(pokemon_url)

    with open('pokemon_template.html') as file:
        template = file.read()

    html_content = render_template_string(template, **pokemon_data)
    filename = os.path.join(OUTPUT_DIR, f"{pokemon_data['pokemon_name']}.html")
    with open(filename, 'w') as file:
        file.write(html_content)

    webbrowser.open_new(f"file://{os.path.abspath(filename)}")
    return render_template_string(open('pokedex.html').read())

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    if threading.active_count() == 1:
        threading.Timer(1.25, open_browser).start()
    app.run(debug=False)
