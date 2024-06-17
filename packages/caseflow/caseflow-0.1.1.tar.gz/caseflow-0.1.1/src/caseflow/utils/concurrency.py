import asyncio
import copy

semaphore_pool = {}

async def concurrency_manage(coroutine, concurrency_value=10):
    """并发管理，限制协程并发数

    Args:
        coroutine (coroutine): 协程任务
        concurrency_value (int, optional): 并发数. Defaults to 10.

    Returns:
        _type_: _description_
    """                     
    semaphore_key = f"{coroutine.__name__}_{concurrency_value}"
    sem = semaphore_pool.get(semaphore_key)
    if not sem:
        sem = asyncio.Semaphore(concurrency_value)
        semaphore_pool[semaphore_key] = sem

    async with sem:
        return await coroutine


async def concurrentcy_loop(coroutineFunc, funcArgs=(), concurrency_value=1, loop=1):
    """并发执行任务，指定任务循环总数及限制并发数

    Args:
        coroutine (coroutine): _协程函数.
        funcArgs (tuple, optional): _协程函数入参. Defaults to ().
        concurrency_value (int, optional): _并发数. Defaults to 1.
        loop (int, optional): _任务总循环数. Defaults to 1.

    Returns:
        _type_: _description_
    """
    tasks = [
        asyncio.create_task(concurrency_manage(coroutine=coroutineFunc(*funcArgs),
                                                concurrency_value=concurrency_value))
        for _ in range(loop)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=asyncio.ALL_COMPLETED)
    print(results)
    return results