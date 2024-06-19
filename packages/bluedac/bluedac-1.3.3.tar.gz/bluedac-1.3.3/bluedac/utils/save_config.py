import json
import os
import bluedac

def save_config(
        repo_name: str,
        language: str,
        branching_strategy: str
    ) -> None:
    """Initialize configuration and saves it to bluedac_config.json file.
    :param: repo_name: Name of the project.
    :param: stack: Stack from which the resources will be taken.
    :param branching_strategy: Branching strategy previously selected.
    """

    # Asking user to insert list of environments that will be used.
    envs = [env for env in input("Declare the environments you want in \
your project (separate them with a single space): ").split(' ')]

    # For each environment, a deployment configuration will be created.
    release_strategy = {env: {'name': '', 'interval': 0, 'percentage': 0} for env in envs}

    # Initial configuration.
    config = {
        'project_name': repo_name,
        'programming_language': language,
        'branching_strategy': branching_strategy,
        'envs': envs,
        'manual_release_envs': [],
        'min_test_coverage': 0,
        'release_strategy': release_strategy
    }

    # Reading starting pipeline, based on specified branching strategy, from Bluedac library.
    with open(f"{os.path.dirname(bluedac.__file__)}/templates/{branching_strategy}_pipeline.json") as file:
        config['pipeline'] = json.loads(file.read())

    # Convert to JSON and write config dictionary to bluedac_config.json file.
    with open("bluedac_config.json", "w") as json_output:
        json_output.write(json.dumps(config, indent = 4))
