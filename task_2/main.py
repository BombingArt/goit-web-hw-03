import multiprocessing
from multiprocessing import cpu_count
from time import time
def factorize(numbers):
    factors = []
    for num in numbers:
        factor_list = []
        for i in range(1, num + 1):
            if num % i == 0:
                factor_list.append(i)
        factors.append(factor_list)
    return factors

def factorize_async(*numbers):
    pool = multiprocessing.Pool(cpu_count())
    results = pool.map(factorize, (numbers,))
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    start_time = time()
    numbers = [128, 255, 99999, 10651060]
    results = factorize_async(*numbers)
    print(f"Async time: {time() - start_time:.2f} sec")
    
    start_time = time()
    factorize(numbers)
    print(f"Sync time: {time() - start_time:.2f} sec")
