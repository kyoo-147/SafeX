# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import time

def addition(x, y):
    return x + y

def main():
    # Enter two numbers from the user
    num1 = int(input("Import fisrt number: "))
    num2 = int(input("Import second number: "))
    # Start counting time
    start_time = time.time()
    # Perform addition
    result = addition(num1, num2)
    # Stop the timer and calculate the execution time
    end_time = time.time()
    execution_time = end_time - start_time
    # Print results and execution time
    print("Result of plus:", result)
    print("Execution time (seconds):", execution_time)

if __name__ == "__main__":
    main()
