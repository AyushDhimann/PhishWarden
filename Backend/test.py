import concurrent.futures
import time

def square(number): # simulate a long-running task
    return number ** 2

if __name__ == '__main__':
    # Create a thread pool with 4 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the square function to the thread pool for each number
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        futures = [executor.submit(square, number) for number in numbers]
        # Wait for all tasks to complete and print the results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        print(results)
