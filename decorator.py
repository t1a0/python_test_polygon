import time
import asyncio
from functools import wraps

def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        if asyncio.iscoroutinefunction(func):
            result = asyncio.run(func(*args, **kwargs))
        else:
            result = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Час виконання функції '{func.__name__}': {elapsed_time} секунд")

        return result

    return wrapper

@execution_time
async def async_function():
    await asyncio.sleep(2)

@execution_time
def sync_function():
    time.sleep(3)

if __name__ == "__main__":
    async_function()
    sync_function()