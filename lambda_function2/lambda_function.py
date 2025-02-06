import json
import requests

def lambda_handler(event, context):
    return classify_number(event, context)

def classify_number(event, context):
    # Debugging: log the received event
    print("Received event:", json.dumps(event))

    # Get the number from query parameters
    query_params = event.get('queryStringParameters', {})
    number_str = str(query_params.get('number', '')).strip()  # Ensure it's always a string

    print(f"Extracted number string: '{number_str}'")  # Debugging output

    # Validate if the input is a valid number (int or float)
    try:
        if not number_str or number_str in ['.', '-', '+']:  # Prevent invalid inputs
            raise ValueError("Invalid number format.")

        number = float(number_str)  # Allow both integers and floating-point numbers
    except ValueError as e:
        print(f"Conversion error: {str(e)}")  # Debugging output
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"number": number_str, "error": True, "message": "Invalid number format."})
        }

    # Initialize response structure
    response = {
        "number": number,
        "is_prime": is_prime(int(number)) if number.is_integer() else False,  
        "is_perfect": is_perfect(int(number)) if number.is_integer() else False,  
        "properties": get_properties(int(number)) if number.is_integer() else [],  
        "digit_sum": digit_sum(int(number)) if number.is_integer() else None,  
    }

    response["fun_fact"] = get_fun_fact(int(number)) if number.is_integer() else "Fun facts are only available for integers."

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(response)
    }

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    if number <= 0:  
        return False
    divisors_sum = sum(i for i in range(1, number) if number % i == 0)
    return divisors_sum == number

def get_properties(number):
    properties = []
    
    if is_armstrong(number):
        properties.append("armstrong")

    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return properties

def is_armstrong(number):
    num_str = str(abs(number))  
    num_digits = len(num_str)
    
    try:
        return sum(int(digit) ** num_digits for digit in num_str) == number
    except ValueError:
        return False  

def digit_sum(number):
    return sum(int(digit) for digit in str(abs(number)))  

def get_fun_fact(number):
    try:
        url = f"http://numbersapi.com/{number}?json"
        response = requests.get(url)
        return response.json().get("text", f"No fun fact available for {number}.")
    except Exception as e:
        return f"Error fetching fun fact: {str(e)}"
