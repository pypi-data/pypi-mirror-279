from aws_cdk import (
    Duration,
    aws_codedeploy as codedeploy,
    RemovalPolicy,
    aws_lambda as AWS_Lambda,
    aws_cloudwatch as cloudwatch
)

from bluedac.utils.stack_utils import StackUtils as utils
from bluedac.blue_res.bluedac_apigw import Bluedac_APIGW

class Bluedac_Lambda(AWS_Lambda.Function):
    """Bluedac-adapted version of Lambda Function.
    It provides 'apply_deployment_strategy' method to comfortably
    define a specific deployment strategy for a single lambda function.
    """

    def __init__(
        self,
        lambda_id,
        file_name,
        handler_name,
        stack,
        environment,
        method_type,
        end_point
    ):
        """
        :param lambda_id: Lambda resource ID. 
        :param file_name: Local file name declaring the Lambda function.
        :param handler_name: Handler name of the function inside the 'file_name' file.
        :param stack: Stack where this resource will be deployed to.
        :param environment: Environment where this resource will be deployed to.
        :param method_type: HTTP method which will be used to access the Lambda function.
        :param end_point: End_point which the Lambda function will be binded binded to.
        """

        super().__init__(
            stack,
            lambda_id,
            runtime=AWS_Lambda.Runtime.PYTHON_3_12,
            code=AWS_Lambda.Code.from_asset("resources"),
            handler=f"{file_name}.{handler_name}"
        )

        self.stack = stack
        self.method_type = method_type
        self.end_point = end_point
        self.environment = environment

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, stack):
        self._stack = stack


    def apply_deployment_strategy(
        self,
        fun_name: str,
        apigw: Bluedac_APIGW,
        removal_policy = RemovalPolicy.RETAIN,
        alarm_config: dict = dict()
    ) -> None:
        """Applies desired release strategy to specified lambda function.
        :param fun_name: Name of the Lambda function. It must be manually specified since it can change during the deploy.
        :param apigw: API Gateway where the lambda function will be binded to.
        :param removal_policy: Specify a removal policy. Default: RemovalPolicy.RETAIN.
        :param alarm_config: Dictionary defining the alarm's parameters that will guard the deployment process.
        """

        # Dictionary containing deployment parameters: name, interval, percentage.
        release_strategy: dict = utils.get_rs_info(self.environment)

        # Switch between traffic routings based on release strategy name value.
        match release_strategy["name"]:
            case "canary":
                traffic_routing = codedeploy.TimeBasedCanaryTrafficRouting(
                    interval=Duration.minutes(release_strategy["interval"]),
                    percentage=release_strategy["percentage"]
                )

            case "linear":
                traffic_routing = codedeploy.TimeBasedLinearTrafficRouting(
                    interval=Duration.minutes(release_strategy["interval"]),
                    percentage=release_strategy["percentage"]
                )
            
            case _:
                traffic_routing = codedeploy.AllAtOnceTrafficRouting.all_at_once()


        # Apply removal policy.
        new_version = self.current_version
        new_version.apply_removal_policy(removal_policy)

        # Define an alias for this Lambda function to allow traffic shifting.
        alias = AWS_Lambda.Alias(
            self.stack,
            f"{fun_name}-alias-id",
            alias_name=f"{fun_name}-alias",
            version=new_version
        )

        # Declare an Alarm with previously provided alarm configuration.
        alarm = cloudwatch.Alarm(
            self.stack,
            f"{release_strategy["name"]}-Alarm-{fun_name}",
            metric=alias.metric(alarm_config["metric"]),
            threshold=alarm_config["threshold"],
            evaluation_periods=alarm_config["period"]
        ) if alarm_config else None

        # Apply the traffic shifting configuration.
        config = codedeploy.LambdaDeploymentConfig(
            self.stack,
            f"{release_strategy["name"]}-DeploymentConfig-{fun_name}",
            traffic_routing=traffic_routing
        )

        # Join all together.
        codedeploy.LambdaDeploymentGroup(
            self.stack,
            f"{release_strategy["name"]}-DeploymentGroup-{fun_name}",
            alias=alias,
            deployment_config=config,
            alarms=[alarm] if alarm else None
        )

        # Bind just updated alias to 'end_point' with 'method_type'
        apigw.bind_lambda(alias, self.method_type, self.end_point)