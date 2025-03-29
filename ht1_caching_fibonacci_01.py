from typing import Callable

# Caching function
def caching_fibonacci() -> Callable[[int], int]:
    # init empty cache
    cache = []

    # Internal function to fill in th list
    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        
        # Expand the cache list if it's too short to avoid empty list error
        while len(cache) <= n:
            cache.append(None)
        
        # Check if n is in the list or first values are existing
        if (cache[n] is not None) or (n in cache):
            return cache[n]

        # Filling the list
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    
    return fibonacci

if __name__ == "__main__":
    fib = caching_fibonacci() # Assign cahcing function to a variable

    print(fib(15)) # Calling internal function through variable
