import time
import asyncio


@app.get("/sync/{id}")
def sync_fun(id: int):
    print(f"sync. Начал выполнение {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил выполнение {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_fun(id: int):
    print(f"async. Начал выполнение {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил выполнение {id}: {time.time():.2f}")

import asyncio
import aiohttp

async def get_data(i: int, endpoint: str):
	url = f"http://127.0.0.1:8000/{endpoint}/{i}"
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			print(f"Закончил выполнение {i}")

asyncio.run(asyncio.get_data(1,"sync"))

asyncio.run(asyncio.gather(*[get_data(i, "async") for i in range(300)]))