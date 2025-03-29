import re
from typing import Callable

# Create pattern to match float and integer in text
pattern = re.compile(r'^-?\d+(\.\d+)?$')

# Generator to split text to words, then find and return numbers by pattern
def generator_numbers(text: str):
    words_list = text.split(" ") # Text split into the list
    for word in words_list:
        if pattern.match(word): # Matching pattern
            yield float(word) # return number as float

# Total amount calculation
def sum_profit(text: str, func: Callable) -> float:
    amount = 0.00 # Amount init
    for next in func(text):
        amount += next # Accumulating all numbers from generator
    return amount



TEXT = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, " \
"доповнений додатковими надходженнями 27.45 і 324.00 доларів. " \
"And US grant of 1000.00 plus bonus of 2500.01"

if __name__=="__main__":
    # Assing total amount calc function to variable while sending generator as input
    total_income = sum_profit(TEXT, generator_numbers)
    print(f"Загальний дохід: {total_income}")