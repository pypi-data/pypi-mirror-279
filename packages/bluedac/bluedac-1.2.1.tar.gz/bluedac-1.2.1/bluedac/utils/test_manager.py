import os
import subprocess
import json
import inquirer
from bluedac.utils.generate_tests import generate_tests

def test_manager(
        argument: list
    ) -> None:

    """It allows user to choose a stack from which the resources will be scraped.
    Based on the latter, user-specified tests will be generated.
    :param argument: List of sub-commands (e.g. --generate, unit, load, ...).
    If none, pytest will be used to launch tests.
    """

    # Check if min_test_coverage is defined in the configuration.
    # If not, it will be assigned to 0.
    try:
        with open(f"{os.getcwd()}/bluedac_config.json", "r") as config:
            json_config = json.loads(config.read())
            coverage = json_config["min_test_coverage"]
    except KeyError:
        coverage = 0
        print("Coverage not specified in configuration file. It has been set to 0.")

    if argument and argument[0] == '--generate':
        # Check if user is in a Bluedac project's directory.
        if os.path.exists(f'{os.getcwd()}/cdk.json'):

            # Retrieve stacks list.
            cdk_ls_process = subprocess.run(["cdk", "ls"], capture_output=True) 
            stacks = cdk_ls_process.stdout.decode("ascii").split("\n")

            # Let user choose a stack.
            prompt_stacks = [
                inquirer.List(
                    "stack",
                    message="Select a stack from the following ones:",
                    choices=stacks,
                ),
            ]
            stack: str = inquirer.prompt(prompt_stacks)["stack"]
        else:
            print("An error occurred. You must be in your project's root directory.")
            exit()

        if len(argument) > 1:
            generate_tests(os.getcwd(), stack, argument[1])
        else:
            generate_tests(os.getcwd(), stack, "all")

    # If there's at least a parameter, user specified a type of test.
    elif argument:
        subprocess.run(["python", "-m", "pytest",
                        f"--cov-fail-under={coverage}" if argument[0] == "unit" else "", 
                        "--cov=./resources", 
                        f"tests/{argument[0]}/"])
    # Launch all tests in tests/ directory.
    else:
        subprocess.run(["python", "-m", "pytest",
                        f"--cov-fail-under={coverage}", 
                        "--cov=./resources",
                        "tests/"])