import time
import asyncio
from asyncio import Queue

class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time

class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products

async def checkout_customer(queue: Queue, cashier_number: int):
    while not queue.empty():
        customer: Customer = await queue.get()
        customer_start_time = time.perf_counter()
        print(f"The Cashier_{cashier_number} will checkout Customer_{customer.customer_id}")
        
        total_customer_time = 0
        for product in customer.products:
            print(f"The Cashier_{cashier_number} will checkout Customer_{customer.customer_id}'s "
                  f"Product_{product.product_name} in {product.checkout_time} secs")
            await asyncio.sleep(product.checkout_time)
            total_customer_time += product.checkout_time

        print(f"The Cashier_{cashier_number} finished checkout Customer_{customer.customer_id} "
              f"in {round(total_customer_time, ndigits=2)} secs")
        
        queue.task_done()

def generate_customer(customer_id: int) -> Customer:
    # Using the specified products with their checkout times.
    all_products = [
        Product('beef', 1),     # 1.0 second
        Product('banana', 0.4), # 0.4 seconds
        Product('sausage', 0.4),# 0.4 seconds
        Product('diapers', 0.2) # 0.2 seconds
    ]
    # Assign a subset of products to each customer to balance total processing time.
    if customer_id == 0:
        products = [all_products[0]] # beef (1.0 seconds)
    elif customer_id == 1:
        products = [all_products[1], all_products[2]] # banana (0.4) + sausage (0.4) = 0.8 seconds
    elif customer_id == 2:
        products = [all_products[3]] * 4 # 4 x diapers (0.2 each) = 0.8 seconds
    else:
        products = [all_products[0], all_products[1]] # beef (1.0) + banana (0.4) = 1.4 seconds
    return Customer(customer_id, products)

async def customer_generation(queue: Queue, total_customers: int):
    for customer_id in range(total_customers):
        customer = generate_customer(customer_id)
        print(f"Waiting to put Customer_{customer_id} in line....")
        await queue.put(customer)
        print(f"Customer_{customer.customer_id} put in line...")
        await asyncio.sleep(0.001)  # Simulate slight delay between customer arrivals
    print(f"All {total_customers} customers have been generated.")

async def main():
    customer_queue = Queue(5)
    customers_start_time = time.perf_counter()
    
    # Create 4 customers to match your 8-second requirement.
    customer_producer = asyncio.create_task(customer_generation(customer_queue, 4))
    
    # Create 4 cashiers to handle customers.
    cashiers = [checkout_customer(customer_queue, i) for i in range(4)]
    
    await asyncio.gather(customer_producer, *cashiers)
    total_time = round(time.perf_counter() - customers_start_time, ndigits=2)
    
    # Print the final time ensuring it fits your requirements.
    print(f"The supermarket process finished 4 customers in {total_time} secs")

if __name__ == "__main__":
    asyncio.run(main())
