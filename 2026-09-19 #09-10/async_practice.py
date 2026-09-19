# Для работы с асинхронностью нужна библиотека asyncio
import asyncio
import time

# # Корутина это функция, которая объявлена асинхронной
# async def async_function():
#     print("Начали")
#     await asyncio.sleep(2)
#     print("Закончили")
#     return "Все!"

# # Если вызвать, то получим объект корутины
# # Чтобы вызвать, перед корутиной надо написать await
# async def main():
#     result = await async_function()
#     print(result)


# asyncio.run(main())

# async def task(name, delay):
#     await asyncio.sleep(delay)
#     return f"Задача {name} выполнена за {delay} с"

# async def main():
#     start = time.perf_counter()
#     task1 = asyncio.create_task(task("A", 4))
#     task2 = asyncio.create_task(task("B", 2))
#     print(await task1)
#     print(await task2)
#     end = time.perf_counter()
#     print(f"{end - start: .2f} с")
#     # Суммарно должно получиться 4 секунды

# asyncio.run(main())

# asyncio.run -- запуск корутины на выполнение
# asyncio.create_task -- добавляет задачу в очередь на выполнение

# async def task(name, delay):
#     await asyncio.sleep(delay)
#     print(f"Задача {name} выполнена за {delay} с")

# async def main():
#     start = time.perf_counter()
#     task1 = asyncio.create_task(task("A", 4))
#     task2 = asyncio.create_task(task("B", 2))
#     await task1
#     await task2
#     end = time.perf_counter()
#     print(f"{end - start: .2f} с")
#     # Суммарно должно получиться 4 секунды

# asyncio.run(main())

# asyncio.gather объединяет создание очереди задач и вызов

async def task(name, delay):
    await asyncio.sleep(delay)
    return f"Задача {name} выполнена за {delay} с"

async def main():
    start = time.perf_counter()

    result1, result2 = await asyncio.gather(task("A", 4), task("B", 2))

    print(result1)
    print(result2)
    
    end = time.perf_counter()
    print(f"{end - start: .2f} с")
    # Суммарно должно получиться 4 секунды

asyncio.run(main())