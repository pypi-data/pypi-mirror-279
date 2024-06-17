"""Run sample project on Pollination."""
from pathlib import Path
import os
import json
import datetime

from pollination_io.api.client import ApiClient
from pollination_io.interactors import Recipe, NewJob


api_key = os.environ['QB_POLLINATION_TOKEN']
recipe_tag = os.environ['TAG']
host = os.environ['HOST']

owner = 'ladybug-tools'
project = 'two-phase-daylight-coefficient'
recipe_name = 'two-phase-daylight-coefficient'

api_client = ApiClient(host, api_key)
recipe = Recipe(owner, recipe_name, recipe_tag, client=api_client)
recipe.add_to_project(f'{owner}/{project}')

samples_path = Path(__file__).parent.resolve().joinpath('samples.json')
with open(samples_path) as samples_json:
    samples = json.load(samples_json)

for idx, sample in enumerate(samples):
    job_name = sample.get('name', f'Sample {idx}')
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auto_name = f'(Scheduled by GitHub workflow: {datetime_now})'
    job_name = ' '.join([job_name, auto_name])
    description = sample.get('description', None)
    job = NewJob(
        owner, project, recipe, name=job_name, description=description,
        client=api_client
    )

    inputs = {}
    for recipe_input, value in sample['inputs'].items():
        input_path = Path(__file__).parent.resolve().joinpath(value)
        if input_path.exists():
            artifact_path = job.upload_artifact(input_path, f'sample_{idx}')
            inputs[recipe_input] = artifact_path
        else:
            inputs[recipe_input] = value

    arguments = []
    arguments.append(inputs)
    job.arguments = arguments

    job.create()
