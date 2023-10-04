import time
import multiprocessing

def factorize_helper(numbers, start, end, result_queue):
    result = []
    for num in numbers[start:end]:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    result_queue.put(result)

def factorize_m(numbers):
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(numbers) // num_processes

    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else len(numbers)
        process = multiprocessing.Process(target=factorize_helper, args=(numbers, start, end, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = []
    for _ in range(num_processes):
        results.extend(result_queue.get())

    return results

if __name__ == "__main__":
    a, b, c, d = factorize_m((128, 255, 99999, 10651060))

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 
                 70, 140, 76079, 152158, 304316, 
                 380395, 532553, 760790, 1065106, 
                 1521580, 2130212, 2662765, 5325530, 10651060]
