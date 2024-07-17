# Concurrently breakfast
import asyncio
from time import sleep, time

<<<<<<< HEAD

=======
>>>>>>> Benz
async def make_coffee(): #1
    print("coffee: prepare ingridients")
    sleep(1)
    print("coffee: waiting...")
<<<<<<< HEAD
    await asyncio.sleep(5) 
    print("coffee: ready")

async def fry_eggs():
    print("eggs: prepare ingridients")
    sleep(1)
    print("eggs: frying...")
    await asyncio.sleep(3)
    print("eggs: ready")

async def main():
=======
    await asyncio.sleep(5) #2: pause, another tasks can be run
    print("cofee: ready")

async def fry_eggs(): #1
    print("eggs: prepare ingridiants")
    sleep(1)
    print("eggs: frying...")
    await asyncio.sleep(3)#2: pause, another tasks can be run
    print("eggs: ready")

async def main(): #1
>>>>>>> Benz
    start = time()
    await make_coffee()
    await fry_eggs()
    print(f"breakfast is ready in {time()-start} min")

<<<<<<< HEAD
asyncio.run(main())
=======
asyncio.run(main()) #run top-level function concurrently
>>>>>>> Benz
