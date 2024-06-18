import json
import boto3

class StackUtils():
    """Provides useful methods for stack management."""

    @staticmethod
    def get_rs_info(
        environment: str
    ) -> dict:
        """Retrieve informations about release strategy from configuration file.
        :param environment: Environment from which the informations will be from.
        """

        with open("bluedac_config.json", "r") as config:
            release_strategy: dict = json.loads(config.read())["release_strategy"][environment]

        return release_strategy
    
    @staticmethod
    def retrieve_apigw_endpoint(
        stack: str
    ) -> str:
        """Queries AWS CloudFormation to retrieve API Gateway endpoint.
        :param stack: Stack to query.
        """

        # Check if stack exists in AWS CloudFormation. 
        try:
            response = boto3\
                .client("cloudformation")\
                .describe_stacks(StackName=stack)
        except Exception:
            print(f"No stack found with that name. Are you sure {stack} is correct? Remember: you must have deployed it first.")
            exit()

        stack_outputs = response["Stacks"][0]["Outputs"]
        api_endpoint = [output['OutputValue'] for output in stack_outputs if output['OutputValue'].startswith('https://')][0]

        if api_endpoint:
            # Query output is in the format: "https://.../" --> need to strip whitespaces, "" and suffix "/". 
            return api_endpoint.strip().strip("\"").removesuffix("/")     
        else:
            print(f"It seems like something went wrong with {stack} retrieving. You must deploy it first.")
            return "INSERT_APIGW_BASE_URL"