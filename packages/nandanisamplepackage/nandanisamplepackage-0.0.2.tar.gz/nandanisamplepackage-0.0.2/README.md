# Calculator Project

## Project Description

The **Calculator Project** is a simple yet powerful calculator application written in Python. It supports basic arithmetic operations such as addition, subtraction, multiplication, and division. The project is designed to provide an easy-to-use interface for performing quick calculations and serves as an educational tool for those learning Python programming.

## Features

- **Addition**: Add two numbers.
- **Subtraction**: Subtract one number from another.
- **Multiplication**: Multiply two numbers.
- **Division**: Divide one number by another.
- **Command-line Interface**: Perform calculations directly from the terminal.

## Installation

Requires Python 3.7 or higher.

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/calculator.git
    ```

2. **Navigate to the Project Directory**:
    ```bash
    cd calculator
    ```

3. **Install Dependencies** (if any):
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command-line Usage

You can use the calculator directly from the command line.

1. **Run the Calculator**:
    ```bash
    python calculator.py
    ```

2. **Perform Operations**:
    ```bash
    # Example: Addition
    python calculator.py add 2 3
    # Output: 5
    ```

### Example Code

You can also use the calculator functions in your Python code.

```python
from calculator import add, subtract, multiply, divide

# Perform addition
result = add(10, 5)
print(f"10 + 5 = {result}")

# Perform subtraction
result = subtract(10, 5)
print(f"10 - 5 = {result}")

# Perform multiplication
result = multiply(10, 5)
print(f"10 * 5 = {result}")

# Perform division
result = divide(10, 5)
print(f"10 / 5 = {result}")
