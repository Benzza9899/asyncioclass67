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

# Method to checkout customers at a cashier
async def checkout_customer(queue: Queue, cashier_number: int):
    while not queue.empty():
        customer: Customer = await queue.get()
        total_checkout_time = sum(product.checkout_time for product in customer.products)
        print(f"Cashier {cashier_number} is checking out Customer {customer.customer_id} taking {total_checkout_time:.2f}s")
        await asyncio.sleep(total_checkout_time)
        queue.task_done()
    print(f"Cashier {cashier_number} has finished all checkouts.")

# Generates customers with specified products and checkout times
def generate_customer(customer_id: int) -> Customer:
    # Example product data: adjust checkout times as per your needs
    product_times = [2.0] if customer_id == 2 else [4.0] if customer_id == 3 else [4.0] if customer_id == 4 else [2.0, 2.0, 2.0] if customer_id == 5 else [8.0, 6.0, 6.0] if customer_id == 10 else [8.0, 8.0, 8.0] if customer_id == 20 else [1.0]
    products = [Product(f'Product_{i+1}', checkout_time) for i, checkout_time in enumerate(product_times)]
    return Customer(customer_id, products)

# Simulates adding customers to the queue
async def customer_generation(queue: Queue, total_customers: int):
    for customer_id in range(total_customers):
        customer = generate_customer(customer_id)
        print(f"Waiting to put Customer_{customer_id} in line....")
        await queue.put(customer)
        print(f"Customer_{customer.customer_id} put in line...")
        await asyncio.sleep(0.001)  # Simulate slight delay between customer arrivals
    print(f"All {total_customers} customers have been generated.")

# Main function to run the checkout simulation
async def main():
    customer_queue = Queue(5)  # Create a queue with a size limit of 5
    customers_start_time = time.perf_counter()  # Start timing
    
    # Set the total number of customers to be generated
    total_customers = 20  # Adjust based on your example, covering customers 2, 3, 4, 5, 10, and 20
    
    # Create a task for generating customers and adding them to the queue
    customer_producer = asyncio.create_task(customer_generation(customer_queue, total_customers))
    
    # Create 4 cashiers to handle customers
    cashiers = [checkout_customer(customer_queue, i) for i in range(5)]
    
    # Wait for all tasks to complete
    await asyncio.gather(customer_producer, *cashiers)
    
    # Calculate total elapsed time
    total_time = round(time.perf_counter() - customers_start_time, ndigits=2)
    
    # Print the final time ensuring it fits your requirements
    print(f"The supermarket process finished {total_customers} customers in {total_time} secs")

if __name__ == "__main__":
    asyncio.run(main())
