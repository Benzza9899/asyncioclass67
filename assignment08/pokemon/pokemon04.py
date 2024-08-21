import asyncio
import httpx
import time
import random

async def get_pokemon(client, url):
    print(f"{time.ctime()} - get {url}")
    resp = await client.get(url)
    ability = resp.json()
    return [ability['name']] + [p['pokemon']['name'] for p in ability['pokemon']]

async def get_pokemons():
    async with httpx.AsyncClient() as client:
        tasks = []
        urls = [
            'https://pokeapi.co/api/v2/ability/battle-armor',
            'https://pokeapi.co/api/v2/ability/speed-boost'
        ]
        for url in urls:
            tasks.append(asyncio.create_task(get_pokemon(client, url)))

        pokemons = await asyncio.gather(*tasks)
        return pokemons

async def index():
    start_time = time.perf_counter()
    pokemons = await get_pokemons()
    end_time = time.perf_counter()
    print(f"{time.ctime()} - Asynchronous get {len(pokemons)} pokemons. Time taken: {end_time - start_time} seconds")
    print(pokemons)

if __name__ == '__main__':
    asyncio.run(index())
