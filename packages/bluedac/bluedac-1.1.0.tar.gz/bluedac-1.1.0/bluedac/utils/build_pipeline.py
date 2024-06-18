import json
import os
import bluedac

def print_dependencies(
        pipeline: dict,
        actual_index: int,
        stage: str
    ) -> str:
    """Defines, for each job, its dependencies (based on bluedac_config.json file)."""
    deps = pipeline[stage][:actual_index]
    deps_string = ''

    if deps:
        deps_string = f'\n{' ' * 4}needs:'
        for dep in deps:
            deps_string += f'\n{' ' * 8}- {dep}'

    return deps_string

def build_pipeline() -> None:
    """Reading bluedac_config.json file, it builds a CI/CD pipeline with Gitlab syntax."""
    
    # --------------- Rules --------------- #
    rules_line = f'\n{' ' * 4}rules:\n'

    # Whether a job has to be ran as manual, append this line.
    manual_line = f'{' ' * 4}when: manual\n\
{' ' * 4}allow_failure: False'

    # Dict of rules that have to be attached to relative job. The key is the job's name.
    rules = {
        'commit_fb': f'{' ' * 8}- if: $CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH != "main"\n',

        'merge_request': f"{' ' * 8}- if: $CI_PIPELINE_SOURCE == 'merge_request_event' \
    && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == 'main'\n",

        'commit_main': f'{' ' * 8}- if: $CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == "main"\n',

        'release': {
            'tag': f'{' ' * 8}- if: $CI_COMMIT_TAG\n',
            'branch': f'{' ' * 8}- if: $CI_COMMIT_BEFORE_SHA == "0000000000000000000000000000000000000000" \
    && $CI_MERGE_REQUEST_TARGET_BRANCH_NAME =~ "branch_regex"\n'
        }
    }

    # --------------- Reading BlueDAC configuration --------------- #
    with open(f'{os.getcwd()}/bluedac_config.json') as file:
        config = json.load(file)
        pipeline: dict = config['pipeline']
        manual_envs = config['manual_release_envs']

        # If release branch used, retrieve their regex.
        release_mode = pipeline.pop('release_mode', None)
        if release_mode == 'branch':
            branch_regex = pipeline.pop('release_branch_regex', None)

    pipeline_string = ''

    # --------------- Pipeline stages parsing --------------- #
    for stage, jobs_stage in pipeline.items():
        # If it's a release job and release branches are used,
        # replace boilerplate with 'branch_regex' value.
        if stage == 'release' and release_mode == 'branch':
            stage_rule = rules[stage][release_mode].replace('branch_regex', branch_regex)
        # If it's a release job, there's some nesting in 'rules'.
        elif stage == 'release':
            stage_rule = rules[stage][release_mode]
        # If it's not a release job.
        else:
            stage_rule = rules[stage]

        for index, job in enumerate(jobs_stage):
            with open(f'{os.path.dirname(bluedac.__file__)}/templates/{job}.yml') as file:
                # Avoid homonymous jobs.
                new_job = f'{job}_{stage}'

                # Update job's name in pipeline dict. Needed to update dependencies.
                pipeline[stage][pipeline[stage].index(job)] = new_job 

                # Composing Gitlab job.
                pipeline_string += f'{new_job}:\n' + \
                file.read() + \
                print_dependencies(pipeline, index, stage) + \
                rules_line + \
                stage_rule + \
                (manual_line if job.startswith('deploy') and job.split('_')[1] in manual_envs else '') # Split[1] greps env name.

    # Save down CI/CD pipeline in gitlab-ci.yml file.
    with open(f'{os.getcwd()}/.gitlab-ci.yml', 'w') as file:
        file.write(pipeline_string)