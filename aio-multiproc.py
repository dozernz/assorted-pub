import asyncio,aiohttp
import concurrent.futures
import time

NUM_PROCS=2
NUM_SESS=4
PER_SESS=10000

async def long_task():
    async with aiohttp.ClientSession() as session:
        for i in range(PER_SESS):
            async with session.get('http://127.0.0.1') as response:
                html = await response.text()


def cpu_bound_work(i):
    try:
        print(f"Starting run {i}")
        asyncio.run(long_task())
    except Exception as e:
        print(e)
    return

async def main():
    with concurrent.futures.ProcessPoolExecutor(NUM_PROCS) as executor:
        loop = asyncio.get_running_loop()

        # Schedule several CPU-bound tasks concurrently
        tasks = [loop.run_in_executor(executor, cpu_bound_work, i) for i in range(NUM_SESS)]

        # Wait for all tasks to complete and get their results
        results = await asyncio.gather(*tasks)

        return results

if __name__ == '__main__':
    start_time = time.time()
    results = asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
