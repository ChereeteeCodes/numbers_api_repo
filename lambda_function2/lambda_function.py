import json
import requests

def lambda_handler(event, context):
    # Call classify_number to handle the request and return the response
    return classify_number(event, context)
    
def classify_number(event, context):
    # Debugging: log the entire event to see its structure
    print("Received event:", json.dumps(event))  # This will log the entire event to CloudWatch

    # Get the number from query parameters
    query_params = event.get('queryStringParameters', {})
    number_str = query_params.get('number', '')
    
    # Validate if the number is a valid integer
    try:
        number = int(number_str)
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"number": number_str, "error": True})
        }
    
    # Initialize response structure
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": get_properties(number),
        "digit_sum": digit_sum(number),
    }
    
    # Fetch fun fact from Numbers API
    fun_fact = get_fun_fact(number)
    response["fun_fact"] = fun_fact

    return {
        "statusCode": 200,
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
    divisors_sum = sum(i for i in range(1, number) if number % i == 0)
    return divisors_sum == number

def get_properties(number):
    properties = []
    
    # Check if Armstrong number
    if is_armstrong(number):
        properties.append("armstrong")
    
    # Check if number is odd or even
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    return properties

def is_armstrong(number):
    num_str = str(number)
    num_digits = len(num_str)
    return sum(int(digit) ** num_digits for digit in num_str) == number

def digit_sum(number):
    return sum(int(digit) for digit in str(number))

def get_fun_fact(number):
    try:
        # Use Numbers API to fetch a fun fact
        url = f"http://numbersapi.com/{number}?json"
        response = requests.get(url)
        fact = response.json().get("text", f"No fun fact available for {number}.")
        return fact
    except Exception as e:
        return f"Error fetching fun fact: {str(e)}"

