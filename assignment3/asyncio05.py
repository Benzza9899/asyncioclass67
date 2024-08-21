# # When a coroutine is wrapped into a Task with functions like asyncio.create_task() the coroutine is automatically scheduled to run soon
# import asyncio


# async def fibonacci(n):
#   await asyncio.sleep(1)
#   a,b = 0,1
#   if n<= 1:
#      return n
#   else:
#      for i in range(1, n):
#         c = a +b
#         a=b
#         b=c
#      return b

# async def main():
#     n = 10 
#     coros = [asyncio.create_task(fibonacci(i)) for  i in range(n)] 
#     result = await asyncio.gather(*coros)
#     print(result)

# # รันโปรแกรม
# asyncio.run(main())



import asyncio

async def fibonacci(n):
    await asyncio.sleep(1)
    a, b = 0, 1
    if n <= 1:
        return n
    else:
        for i in range(1, n):
            c = a + b
            a = b
            b = c
        return b

async def main():
    n = 10 
    coros = [asyncio.create_task(fibonacci(i)) for i in range(n)] 
    
    # ใช้ asyncio.wait แทน asyncio.gather
    done, pending = await asyncio.wait(coros)
    
    # รวบรวมผลลัพธ์จากคอร์รูทีนที่เสร็จสิ้น
    result = [task.result() for task in done]
    
    print(result)

# รันโปรแกรม
asyncio.run(main())
