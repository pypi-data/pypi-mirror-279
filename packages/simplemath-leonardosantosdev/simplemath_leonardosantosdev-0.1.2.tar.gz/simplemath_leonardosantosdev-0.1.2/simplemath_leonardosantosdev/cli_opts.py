import sys
from simplemath_leonardosantosdev.arithmetic import add, subtract, multiply, divide

def main():
    args = sys.argv[1:]  # Exclude the script name (first argument)
    if len(args) != 2:
        print("Usage: simplemath_leonardosantosdev <operation> <num1> <num2>")
        sys.exit(1)
    
    operation = args[0]
    num1 = float(args[1])
    num2 = float(args[2])

    if operation == '-add':
        result = add(num1, num2)
        print(f"Result: {result}")

    elif operation == '-subtract':
        result = subtract(num1, num2)
        print(f"Result: {result}")

    elif operation == '-multiply':
        result = multiply(num1, num2)
        print(f"Result: {result}")

    elif operation == '-divide':
        result = divide(num1, num2)
        print(f"Result: {result}")
    else:
        print(f"Unsupported operation: {operation}")
        sys.exit(1)

if __name__ == '__main__':
    main()
