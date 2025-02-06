# The Numbers API Application
This repo stores the lambda function code written in Python that takes a number from the user, and returns the following details about said number: 
- number_is_prime: True or False
- is_perfect: True or False
- properties: armstrong or not, even or odd
- digit_sum: sum of its digits
- fun_fact: Something fun about the number

## Reources
The code gets the details about these numbers entered through two public apis: 
- Fun fact API:  http://numbersapi.com/#42
- Mathematics API:  https://en.wikipedia.org/wiki/Parity_(mathematics)
In deploying the code, I used AWS Lambda and API Gateway, cloudwatch for monitoring and logging helped with debugging.

## API Endpoint Displays Result
API endpoint: https://65onllvr9l.execute-api.us-east-1.amazonaws.com/api/classify-number?number=81
Result sample: {"number": 81, "is_prime": false, "is_perfect": false, "properties": ["odd"], "digit_sum": 9, "fun_fact": "81 is the number of squares on a shogi playing board."}


