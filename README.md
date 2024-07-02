# PokeApi_python
En este repositorio conecte la API PokeApi en Python. El usuario puede elegir un número del 1 al 4 para mostrar la información del pokemon seleccionado (tipo, HP, ataque, evoluciones, habilidades, defensa, etc.).

![](https://github.com/UriGOPAR/PokeApi_python/blob/main/Pokemon_img.jpg)

## Instrucciones para Ejecutar

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/UriGOPAR/PokeApi_python.git
2. **Instalar las siguientes librerías en python**
   ```bash
   pip install requests flask
3. **Para ejecutar este proyecto debes de correrlo con el siguiente comando**
     ```bash
    python pokedex.py
4. Al momento de ejecutar este comando se te abrira en el navegador la ruta http://127.0.0.1:5000/, el cual es la ruta del servidor local.
5. Selecciona cualquier número de la lista, te abrira una pestaña con el pokemon que seleccionaste con su información
6. Estos html se guardaran en la carpeta de outputs.
7. **Para detener el este programa en tu terminal teclear**
    ```bash
    ctrl+c

## Librerrías Utilizadas
- Flask
- Requests
- webbrowser
- threading
- os
## Estructura de este proyecto
- `pokedex.py`: Script principal que ejecuta el programa.
- `outputs/`: Directorio donde se guardan los archivos HTML generados.
- `static`: Carpeta en donde se guardaron los archivos css o imagenes.
- `pokemon_template.html`: Es la template de como se van a acomodar la información de los pokemons
- `README.md`: Documentación del proyecto en Markdown.

