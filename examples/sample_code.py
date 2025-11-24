# Sample Python Code: Fibonacci Calculator

def fibonacci(n):
    """
    Calculate the nth Fibonacci number using dynamic programming.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    # Use dynamic programming to calculate
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib[n]


def fibonacci_recursive(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


# Example usage
if __name__ == "__main__":
    print("Fibonacci sequence (first 10 numbers):")
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")
