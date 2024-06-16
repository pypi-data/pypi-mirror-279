"""
The custom logic for the command m3 plan-terraform-template.
This logic is created to convert parameters from the Human readable format to
appropriate for M3 SDK API request.
"""
import os
import json

from m3cli.utils.utilities import handle_variables


def create_custom_request(request):
    parameters = request.parameters
    parameters['task'] = 'PLAN'
    variables = parameters.pop('variables', None)
    path_to_file = parameters.pop('variables-file', None)
    if variables and path_to_file:
        raise AssertionError(
            'Cannot use the "--variables" and "--variables-file" parameters '
            'together'
        )
    if path_to_file:
        if not os.path.isfile(path_to_file):
            raise AssertionError(f'There is no file by path: "{path_to_file}".')
        with open(path_to_file, 'r') as file:
            variables = json.load(file)
    if variables:
        parameters['variables'] = handle_variables(variables)
    return request
