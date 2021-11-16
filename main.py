from typing import Any, Dict, Tuple

import httpx


def carga_de_datos(api: str) -> Dict[str, Any]:
    """
    This function loads the data
    :param api: The api from which it will retrieve the data
    :type api: str
    :return: The response of the request in Dict format
    :rtype: Dict[str, Any]
    """
    data: Dict = {}
    try:
        # Colocar timeout para evitar que se cierre la petición
        res = httpx.get(api, timeout=20.0)
        res.raise_for_status()
        data = res.json()

    except httpx.HTTPStatusError as err:
        print(
            "Error produced -> "
            f"[ERROR]: status code: {err.response.status_code} - "
            f"message: {err.response.json()}"
        )

    return data


def nombres_poke(pokedex: Dict[str, Any]) -> int:
    """
    This function shows how many pokemons have 'at' and 2 'a' on its name
    :param pokedex: The dictionary in wich we have all the pokemons data
    :type pokedex: Dict[str, Any]
    :return: The number of pokemon with 'at' and 2 'a' on its name
    :rtype: int
    """
    numero_pokemones: int = 0
    for pokemon in pokedex["results"]:
        nombre: str = pokemon["name"]

        if "at" in nombre and nombre.count("a") == 2:
            numero_pokemones += 1
    return numero_pokemones


print(str(nombres_poke(carga_de_datos("https://pokeapi.co/api/v2/pokemon?limit=10000"))))


def procrear_pokemon(pokedex: Dict[str, Any]) -> int:
    """
    This function shows how many pokemons can procreate with a 'raichu'
    :param pokedex: The dictionary in wich we have all the pokemons data
    :type pokedex: Dict[str, Any]
    :return: The number of pokemon that can procreate with a 'raichu'
    :rtype: int
    """
    lista_encontrados = []
    dict_species = carga_de_datos(pokedex["species"]["url"])
    for grupo in dict_species["egg_groups"]:
        dict_egg_group = carga_de_datos(grupo["url"])
        for pokemon in dict_egg_group["pokemon_species"]:
            # Check if the pokemon found is not yet on the list to avoid duplicates
            if pokemon["name"] not in lista_encontrados:
                lista_encontrados.append(pokemon["name"])

    return len(lista_encontrados)


print(procrear_pokemon(carga_de_datos("https://pokeapi.co/api/v2/pokemon/raichu")))


def peso_max_min(pokedex: Dict[str, Any]) -> Tuple[int]:
    """
    This function shows the minimum an the maximon weight a fighting first generation pokemon
    :param pokedex: The dictionary in wich we have all the pokemons data
    :type pokedex: Dict[str, Any]
    :return: A tuple with the minimum an the maximon weight a fighting first generation pokemon
    :rtype: Tuple[int]
    """
    lista_pesos = []
    for pokemon in pokedex["pokemon"]:
        id_pokemon = pokemon["pokemon"]["url"].split("/")[6]
        if int(id_pokemon) <= 151:
            datos_pokemon = carga_de_datos(pokemon["pokemon"]["url"])
            lista_pesos.append(datos_pokemon["weight"])
    maximo = max(lista_pesos)
    minimo = min(lista_pesos)
    return (maximo, minimo)


print(peso_max_min(carga_de_datos("https://pokeapi.co/api/v2/type/fighting/")))
