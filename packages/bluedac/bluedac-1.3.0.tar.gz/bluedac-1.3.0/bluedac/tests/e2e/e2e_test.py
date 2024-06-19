import boto3
import requests

# Before running the test, ensure to have set stack_name (use 'cdk ls' to list stacks).
stack_name = "INSERT_STACK_NAME"

# Change the lambda function API path accordingly.
lambda_api_path = "example"

# Here, use 'client' to scrape stack resources and get API-GW endpoint URL.
client = boto3.client("cloudformation")

try:
    response = client.describe_stacks(StackName=stack_name)
except Exception:
    print(f'No stack found with that name. Are you sure {stack_name} is deployed?')
    exit()

stack_outputs = response["Stacks"][0]["Outputs"]

# OutputValue parameter contains API Gateway endpoint URL.
api_endpoint = [output['OutputValue'] for output in stack_outputs if output['OutputValue'].startswith('https://')][0]

# Use requests library to make calls and retrieve responses.
response = requests.post(api_endpoint + lambda_api_path)

# Define here your assertions.
assert response.text == 'expected_param'
assert response.status_code == '200'