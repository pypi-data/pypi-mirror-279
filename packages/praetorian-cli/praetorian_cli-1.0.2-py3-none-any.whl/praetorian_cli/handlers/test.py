import os

import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler


@chariot.command('test')
@cli_handler
@click.option('-suite', '--suite', type=click.Choice(["coherence"]), help="Run a specific test suite")
@click.argument('key', required=False)
def trigger_all_tests(controller, key, suite):
    """ Run integration test suite """
    try:
        import pytest
    except ModuleNotFoundError:
        print("Install pytest using 'pip install pytest' to run this command")
    test_directory = os.path.relpath("praetorian_cli/sdk/test", os.getcwd())
    os.environ['CHARIOT_PROFILE'] = controller.keychain.profile
    command = [test_directory]
    if key:
        command.extend(['-k', key])
    if suite:
        command.extend(['-m', suite])
    pytest.main(command)
