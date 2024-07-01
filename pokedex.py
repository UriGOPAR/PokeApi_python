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

@app.route('/')
def index():
    return render_template_string(open('pokedex.html').read())

def get_ability_effects(ability_url):
    response = requests.get(ability_url)
    ability_data = response.json()
    # Filtrar los efectos en inglés
    effect_entries = ability_data['effect_entries']
    effect_in_english = next(entry['effect'] for entry in effect_entries if entry['language']['name'] == 'en')
    return effect_in_english

# Función para obtener la información de las evoluciones
def get_evolution_chain(evolution_url):
    response = requests.get(evolution_url)
    evolution_data = response.json()
    chain = evolution_data['chain']
    evolutions = []
    while chain:
        evolutions.append(chain['species']['name'])
        chain = chain['evolves_to'][0] if chain['evolves_to'] else None
    return evolutions

# Función para obtener la información de los tipos
def get_type_info(type_url):
    response = requests.get(type_url)
    type_data = response.json()
    double_damage_from = [damage['name'] for damage in type_data['damage_relations']['double_damage_from']]
    double_damage_to = [damage['name'] for damage in type_data['damage_relations']['double_damage_to']]
    return double_damage_from, double_damage_to

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    choice = request.form.get('choice')
    if choice == "1":
        url = "https://pokeapi.co/api/v2/pokemon/pichu"
        response = requests.get(url)
        pokemon_data = response.json()
        pokemon_name = pokemon_data['name'].capitalize()
        pokemon_abilities = []
        for ability in pokemon_data['abilities']:
            ability_name = ability['ability']['name']
            ability_url = ability['ability']['url']
            ability_effect = get_ability_effects(ability_url)
            pokemon_abilities.append({'name': ability_name, 'effect': ability_effect})

        # Obtener estadísticas y otros datos
        hp = pokemon_data['stats'][0]['base_stat']
        attack = pokemon_data['stats'][1]['base_stat']
        defense = pokemon_data['stats'][2]['base_stat']
        base_experience = pokemon_data['base_experience']
        image_url = pokemon_data['sprites']['front_default']

        # Obtener evoluciones
        species_url = pokemon_data['species']['url']
        species_response = requests.get(species_url)
        species_data = species_response.json()
        evolution_chain_url = species_data['evolution_chain']['url']
        evolutions = get_evolution_chain(evolution_chain_url)

        # Obtener información de tipos
        type_url = pokemon_data['types'][0]['type']['url']
        double_damage_from, double_damage_to = get_type_info(type_url)
        print(pokemon_name)  # Imprime la información en la consola

        # Renderizar el contenido HTML usando la plantilla
        with open('pokemon_template.html') as file:
            template = file.read()
        html_content = render_template_string(template,pokemon_name=pokemon_name,
                                              image_url=image_url,
                                              hp=hp,attack=attack, 
                                              defense=defense,base_experience=base_experience,pokemon_abilities=pokemon_abilities,evolutions=evolutions,
                                              double_damage_from=double_damage_from,
                                              double_damage_to=double_damage_to)
    if choice == "2":
        url = "https://pokeapi.co/api/v2/pokemon/charmander"
        response = requests.get(url)
        pokemon_data = response.json()
        pokemon_name = pokemon_data['name'].capitalize()
        pokemon_abilities = []
        for ability in pokemon_data['abilities']:
            ability_name = ability['ability']['name']
            ability_url = ability['ability']['url']
            ability_effect = get_ability_effects(ability_url)
            pokemon_abilities.append({'name': ability_name, 'effect': ability_effect})

        # Obtener estadísticas y otros datos
        hp = pokemon_data['stats'][0]['base_stat']
        attack = pokemon_data['stats'][1]['base_stat']
        defense = pokemon_data['stats'][2]['base_stat']
        base_experience = pokemon_data['base_experience']
        image_url = pokemon_data['sprites']['front_default']

        # Obtener evoluciones
        species_url = pokemon_data['species']['url']
        species_response = requests.get(species_url)
        species_data = species_response.json()
        evolution_chain_url = species_data['evolution_chain']['url']
        evolutions = get_evolution_chain(evolution_chain_url)

        # Obtener información de tipos
        type_url = pokemon_data['types'][0]['type']['url']
        double_damage_from, double_damage_to = get_type_info(type_url)
        print(pokemon_name)  # Imprime la información en la consola

        # Renderizar el contenido HTML usando la plantilla
        with open('pokemon_template.html') as file:
            template = file.read()
        html_content = render_template_string(template,pokemon_name=pokemon_name,
                                              image_url=image_url,
                                              hp=hp,attack=attack, 
                                              defense=defense,base_experience=base_experience,pokemon_abilities=pokemon_abilities,evolutions=evolutions,
                                              double_damage_from=double_damage_from,
                                              double_damage_to=double_damage_to)
        
        # Guardar el contenido HTML en un archivo
        filename = f"{pokemon_name}.html"
        with open(filename, 'w') as file:
            file.write(html_content)
        webbrowser.open_new(f"file://{os.path.abspath(filename)}")
    return "Check your console for the Pokémon data."



def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()  # Abre el navegador después de 1.25 segundos
    app.run(debug=True)
