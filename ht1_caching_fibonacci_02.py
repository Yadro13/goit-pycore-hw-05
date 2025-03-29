from typing import Callable

# Shorter version with a bit different logic

# Caching function
def caching_fibonacci() -> Callable[[int], int]:
    cache = [0, 1]  # Initialize for n=0 and n=1

    # Internal function to fill in th list
    def fibonacci(n: int) -> int:
        # check if n is in cache
        if n < len(cache):
            return cache[n]
        
        # Calculate and cache values up to n
        while len(cache) <= n:
            cache.append(cache[-1] + cache[-2])
        
        return cache[n]
    
    return fibonacci

if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(15)) 